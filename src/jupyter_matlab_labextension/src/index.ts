// Copyright 2022 The MathWorks, Inc.

import { JupyterFrontEndPlugin } from '@jupyterlab/application';
import { matlabInBrowserButtonPlugin } from './matlab_browser_button';
import { matlabMFilesPlugin } from './matlab_files';
import { matlabCodeMirrorPlugin } from './matlab_cm_mode';

/** matlabInBrowserButtonPlugin
 * Registers the MATLAB-in-browser desktop button, which will
 * appear in the notebook toolbar.
 */

/** matlabMFilesPlugin
 * Create a command to open a new .m file.
 * Add this command to the Launcher (under "other"),
 * as well as to the command palette (which is opened via ctrl+shift+c).
 * Also associate .m files with the MATLAB mFile icon.
 */

/** matlabCodeMirrorPlugin
 * Add the MATLAB mode to CodeMirror.
 * The parameter app is required, even if it is not used.
 */

const plugins: JupyterFrontEndPlugin<any>[] = [matlabInBrowserButtonPlugin, matlabMFilesPlugin, matlabCodeMirrorPlugin];
export default plugins;
