// Copyright 2022 The MathWorks, Inc.

import {
    JupyterFrontEnd,
    JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { ICommandPalette } from '@jupyterlab/apputils';
import { ICodeMirror } from '@jupyterlab/codemirror';
import { ILauncher } from '@jupyterlab/launcher';

import { defineMATLABMode } from './matlab_cm_mode';
import { registerMFiles } from './matlab_files';
import { MatlabInBrowserButtonExtension } from './matlab_browser_button';

/** Register the MATLAB-in-browser desktop button, which will
 * appear in the notebook toolbar.
 */
const matlabInBrowserButtonPlugin: JupyterFrontEndPlugin<void> = {
    id: '@mathworks/matlabInBrowserButtonPlugin',
    autoStart: true,
    activate: (
        app: JupyterFrontEnd
    ) => {
        const matlabInBrowserButton = new MatlabInBrowserButtonExtension();
        app.docRegistry.addWidgetExtension('Notebook', matlabInBrowserButton);
    }
};

/** Create a command to open a new .m file.
 * Add this command to the Launcher (under "other"),
 * as well as to the command palette (which is opened via ctrl+shift+c).
 * Also associate .m files with the MATLAB mFile icon.
 */
const matlabMFilesPlugin: JupyterFrontEndPlugin<void> = {
    id: '@mathworks/matlabMFilesPlugin',
    autoStart: true,
    optional: [ILauncher, ICommandPalette],
    activate: (
        app: JupyterFrontEnd,
        launcher: ILauncher | null,
        palette: ICommandPalette | null
    ) => {
        registerMFiles(app, launcher, palette);
    }
};

/** Add the MATLAB mode to CodeMirror.
 * The parameter app is required, even if it is not used.
 */
const matlabCodeMirrorPlugin: JupyterFrontEndPlugin<void> = {
    id: '@mathworks/matlabCodeMirrorPlugin',
    autoStart: true,
    requires: [ICodeMirror],
    activate: (
        app: JupyterFrontEnd,
        codeMirror: ICodeMirror,
    ) => {
        defineMATLABMode(codeMirror);
    }
};

const plugins: JupyterFrontEndPlugin<any>[] = [matlabInBrowserButtonPlugin, matlabMFilesPlugin, matlabCodeMirrorPlugin];
export default plugins;
