function output = processJupyterKernelRequest(request_type, varargin)
% PROCESSJUPYTERKERNELREQUEST An entrypoint function for various Jupyter Kernel
% features such as code execution, code completion etc.
%   Inputs:
%       request_type - string     - identifier to differentiate multiple features.
%                                   Supported values are "execute" and "complete"
%       varargin     - cell array - additional inputs which vary in number based
%                                   on value of input request_type
%                                   - "execute"
%                                      - string - MATLAB code to be executed
%                                   - "complete"
%                                      - string - MATLAB code
%                                      - number - cursor position
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

% Lock the function on the first use to prevent it from being cleared from the memory
mlock;

% Delegate feature work based on request type
switch(request_type)
    case 'execute'
        code = varargin{1};
        output = jupyter.execute(code);
    case 'complete'
        code = varargin{1};
        cursorPosition = varargin{2};
        output = jupyter.complete(code, cursorPosition);
end
