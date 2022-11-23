% processJupyterKernelRequest acts as an entrypoint for various Jupyter Kernel
% features such as code execution, code completion etc.
%   Inputs:
%       request_type - string     - identifier to differentiate multiple features.
%                                   Supported values are "execute" and "complete"
%       varargin     - cell array - additional inputs which vary in number based
%                                   on value of input request_type
%        - "execute"
%           - string - MATLAB code to be executed
%        - "complete"
%           - string - MATLAB code
%           - number - cursor position
%   Outputs:
%       - cell array on struct
%           - type      - string - jupyter output type. Supported values are
%                                  "execute_result" and "stream"
%           - mimetype  - cell array - mimetypes of the outputs. Usually these are
%                                      different representations for the same output.
%           - value     - cell array - Output value corresponding to the representation
%                                      of mimetype at its index.
%           - content   - struct - Used only for 'stream' type
%               - name  - string - name of the stream. Supported values are 'stdout'
%                                  and 'stderr'.
%               - value - string - content of the stream
%
% Copyright 2022 The MathWorks, Inc.

function output = processJupyterKernelRequest(request_type, varargin)
    % Lock the function on the first use to prevent it from being cleared from the memory
    mlock;

    persistent webwindow;
    persistent idler;

    % Open MATLAB JSD and wait for it to completely load to ensure all services
    % are initialized. This is a one-time task and does not impact subsequent
    % calls to this function.
    if isempty(webwindow)
        url = 'ui/webgui/src/index-jsd-cr.html';
        % MATLAB versions R2020b and R2021a requires specifying the base url.
        % Not doing so results in the URL not being loaded with the error
        % "Not found. Request outside of context root".
        if any(strcmp(matlabRelease.Release, {'R2020b','R2021a'}))
            url = strcat(getenv("MWI_BASE_URL"), '/', url);
        end
        webwindow = matlab.internal.webwindow(connector.getUrl(url));
        idler = mlreportgen.utils.internal.Idler;
        webwindow.PageLoadFinishedCallback = @(a,b) pageLoadCallback(a,b,idler);
        show(webwindow);
    end

    % This will block the thread until stop loading is called or else hits time-out.
    %The values are logical
    pageLoaded = idler.startIdling(10);

    % If page is not loaded succesfully, return an error output and reset the
    % webwindow to retry rendering MATLAB UI on the next call.
    if ~pageLoaded
        output = {processStream('stderr','MATLAB UI not loaded. Click on "Open MATLAB Desktop" button to open MATLAB UI.')};
        webwindow = [];
        return
    else
        hide(webwindow);
    end

    % Delegate feature work based on request type
    switch(request_type)
        case 'execute'
            code = varargin{1};
            output = executionImpl(code);
        case 'complete'
            code = varargin{1};
            cursorPosition = varargin{2};
            output = completionImpl(code, cursorPosition);
    end
end

function result = completionImpl(code, cursorPosition)
    % TODO: Implement Tab completion
end

% Helper function for handling execution of MATLAB code and post-processing the
% outputs to conform to Jupyter API. We use the Live Editor API for for majority
% of the work.
%
% The entire MATLAB code given by user is treated as code within a single cell
% of unique Live Script. Hence, each execution request  can be considered as
%creating and running a new Live Script file.
function result = executionImpl(code)
    % Value that needs to be shown in the error message when a particular error
    % displays the file name. The kernel does not have access to the file name
    % of the IPYNB file. Hence, we use a generic name 'Notebook' for the time being.
    fileToShowErrors = 'Notebook';

    % Prepare the input for the Live Editor API.
    jsonedRegionList = jsonencode(struct(...
        'regionLineNumber',1,...
        'regionString',code,...
        'regionNumber',0,...
        'endOfSection',true,...
        'sectionNumber',1));
    request = struct('requestId', 'jupyter_matlab_kernel', 'regionArray', jsonedRegionList, 'fullText', code, 'fullFilePath', fileToShowErrors);

    % Disable Hotlinks in the output captured. The hotlinks do not have a purpose
    % in Jupyter notebooks.
    previousState = feature('hotlinks','off');

    % Use the Live editor API for execution of MATLAB code and capturing the outputs
    resp = jsondecode(matlab.internal.editor.evaluateSynchronousRequest(request));

    % Reset the hotlinks feature.
    feature('hotlinks',previousState);

    % Post-process the outputs to conform to Jupyter API.
    result = processOutputs(resp.outputs);
end

function result = processOutputs(outputs)
    result =cell(1,length(outputs));

    % For a given execution request, even though many figures are present,
    % only the final output of the figure window is captured. Hence we need
    % to keep track of the last figure type output in the list of outputs
    % for maintaining order of outputs displayed.
    figureLastIndex = 0;

    % Post process each captured output based on its type.
    for ii = 1:length(outputs)
        out = outputs(ii);
        outputData = out.outputData;
        switch out.type
            case 'matrix'
                result{ii} = processMatrix(outputData);
            case 'variable'
                result{ii} = processVariable(outputData);
            case 'variableString'
                result{ii} = processVariable(outputData);
            case 'symbolic'
                result{ii} = processSymbolic(outputData);
            case 'error'
                result{ii} = processStream('stderr', outputData.text);
            case 'warning'
                result{ii} = processStream('stderr', outputData.text);
            case 'text'
                result{ii} = processStream('stdout', outputData.text);
            case 'stderr'
                result{ii} = processStream('stderr', outputData.text);
            case 'figure'
                % After all outputs are captured, the final snapshot of figure
                % window is taken and is added to the end of list of outputs. This
                % output contains the actual figure data. We post process this
                % data and store it in the result at the index where the last figure was captured.
                if isfield(outputData, 'figureImage')
                    result{figureLastIndex} = processFigure(outputData.figureImage);
                else
                    figureLastIndex = ii;
                end
        end
    end
end

% Helper function to post process output of type 'matrix', 'variable' and
% 'variableString'. These outputs are of HTML type due to various HTML tags
% used in MATLAB outputs such as the <strong> tag in tables.
function result = processText(text)
    result.type = 'execute_result';
    result.mimetype = {"text/html", "text/plain"};
    result.value = [sprintf("<html><body><pre>%s</pre></body></html>",text), text];
end

function result = processMatrix(output)
    text = sprintf("%s = %s %s\n%s", output.name, output.header, output.type, output.value);
    result = processText(text);
end

function result = processVariable(output)
    text = sprintf("%s = %s\n   %s", output.name, output.header, output.value);
    result = processText(text);
end

% Helper function for post-processing symbolic outputs. The captured output
% contains MathML representation of symbolic expressions. Since Jupyter and
% GitHub have native support for LaTeX, we use EquationRenderer JS API to
% convert the MathML to LaTeX values.
function result = processSymbolic(output)
    % Use persistent variables to avoid loading multiple webwindows.
    persistent webwindow;
    persistent idler;

    if isempty(webwindow)
        url = 'toolbox/matlab/codetools/liveeditor/index.html';

        % MATLAB versions R2020b and R2021a requires specifying the base url.
        % Not doing so results in the URL not being loaded with the error
        %"Not found. Request outside of context root".
        if any(strcmp(matlabRelease.Release, {'R2020b','R2021a'}))
            url = strcat(getenv("MWI_BASE_URL"), '/', url);
        end
        webwindow = matlab.internal.cef.webwindow(connector.getUrl(url));
        idler = mlreportgen.utils.internal.Idler;
        webwindow.PageLoadFinishedCallback = @(a,b) pageLoadCallback(a,b,idler);
    end

    % This will block the thread until stop loading is called. The values are logical
    pageLoaded = idler.startIdling(10);

    % If page is not loaded succesfully. We fallback to embedding MathML inside HTML.
    % This will render the symbolic output in JupyterLab and Classic Notebook but not
    % in GitHub.
    if ~pageLoaded
        disp('Browser page load error')
        result = processText(output.value);
        return
    end

    %  Use the EquationRenderer JS API to convert MathML to LaTeX.
    webwindow.executeJS('eq = require("equationrenderercore/EquationRenderer")');
    latexcode = jsondecode(webwindow.executeJS(sprintf('eq.convertMathMLToLaTeX(%s)', jsonencode(output.value))));
    if isempty(output.name)
        % If there is not variable name captured, then we only display the symbolic equation.
        % This happens in cases such as "disp(exp(b))".
        latexcode = strcat('$',latexcode,'$');
    else
        latexcode = strcat('$',output.name,' = ',latexcode,'$');
    end

    result.type = 'execute_result';
    result.mimetype = {"text/latex"};
    result.value = {latexcode};
end

% Helper function for processing outputs of stream type such as 'stdout' and 'stderr'
function result = processStream(stream, text)
    result.type = 'stream';
    result.content.name = stream;
    result.content.text = text;
end

% Helper function for processing figure outputs.
% base64Data will be "data:image/png;base64,<base64_value>"
function result = processFigure(base64Data)
    result.type = 'execute_result';
    base64DataSplit = split(base64Data,";");
    result.mimetype = {extractAfter(base64DataSplit{1},5)};
    result.value = {extractAfter(base64DataSplit{2},7)};
end

% Helper function to notify browser page load finished
function pageLoadCallback(~,~,idler)
    idler.stopIdling();
end
