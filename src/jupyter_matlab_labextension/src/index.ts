import {
    JupyterFrontEnd,
    JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { ToolbarButton, ICommandPalette } from '@jupyterlab/apputils';
import { ICodeMirror } from '@jupyterlab/codemirror';
import { PageConfig } from '@jupyterlab/coreutils';
import { DocumentRegistry } from '@jupyterlab/docregistry';
import { ILauncher } from '@jupyterlab/launcher';
import { INotebookModel, NotebookPanel } from '@jupyterlab/notebook';

import { ReadonlyPartialJSONObject } from '@lumino/coreutils';
import { IDisposable } from '@lumino/disposable';

import { matlabIcon } from './icons';
import { defineMATLABMode } from './matlab';

namespace CommandIDs {
  export const newMatlabFile = 'matlab:new-matlab-file';
}
const FACTORY = 'Editor';
const PALETTE_CATEGORY = 'Other';

const insertButton = async (panel: NotebookPanel, matlabInBrowserButton: ToolbarButton): Promise<void> => {
    await panel.sessionContext.ready;
    if (panel.sessionContext.kernelDisplayName === 'MATLAB Kernel') {
        panel.toolbar.insertItem(10, 'matlabInBrowserButton', matlabInBrowserButton);
    }
};

export class MatlabInBrowserButtonExtension implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel> {
    createNew (panel: NotebookPanel, context: DocumentRegistry.IContext<INotebookModel>): IDisposable {
        // Create the toolbar button to open the MATLAB desktop in-browser.
        const matlabInBrowserButton = new ToolbarButton({
            className: 'openMATLABButton',
            icon: matlabIcon,
            label: 'Open MATLAB',
            tooltip: 'Open MATLAB',
            onClick: (): void => {
                const baseUrl = PageConfig.getBaseUrl();
                window.open(baseUrl + 'matlab', '_blank');
            }
        });
        insertButton(panel, matlabInBrowserButton);
        return matlabInBrowserButton;
    }
}

/** Registers the MATLAB in-browser desktop button, which will
 * appear in the notebook toolbar.
 */
const matlabInBrowserButtonPlugin: JupyterFrontEndPlugin<void> = {
    id: '@mathworks/matlabInBrowserButtonPlugin',
    autoStart: true,
    activate: (app: JupyterFrontEnd) => {
        const matlabInBrowserButton = new MatlabInBrowserButtonExtension();
        app.docRegistry.addWidgetExtension('Notebook', matlabInBrowserButton);
    }
};

/** Creates a command to open a new .m file.
 * Adds this command to the Launcher (under "other"),
 * as well as to the command palette (which is opened via ctrl+shift+c).
 * Also associates .m files with the MATLAB icon.
 */
const matlabMFilesPlugin: JupyterFrontEndPlugin<void> = {
    id: '@mathworks/matlabMFilesPlugin',
    autoStart: true,
    requires: [],
    optional: [ILauncher, ICommandPalette],
    activate: (
        app: JupyterFrontEnd,
        launcher: ILauncher | null,
        palette: ICommandPalette | null
    ) => {
        const { commands } = app;
        const createNewMatlabFile = async (args: ReadonlyPartialJSONObject) => {
            // Get the directory in which the MATLAB file must be created;
            // otherwise take the current filebrowser directory
            const cwd = args.cwd;

            // Create a new untitled MATLAB file
            const model = await commands.execute('docmanager:new-untitled', {
                path: cwd,
                type: 'file',
                ext: '.m'
            });

            // Open the newly created file with the 'Editor'
            return commands.execute('docmanager:open', {
                path: model.path,
                factory: FACTORY
            });
        }
        const command = CommandIDs.newMatlabFile;
        // Create a new MATLAB file by adding a command to the JupyterFrontEnd
        commands.addCommand(command, {
            label: (args) => (args.isPalette ? 'New MATLAB File' : 'MATLAB File'),
            caption: 'Create a new MATLAB file',
            icon: (args) => (args.isPalette ? '' : matlabIcon),
            execute: createNewMatlabFile
        });

        // Add the command to the launcher
        if (launcher) {
            launcher.add({
                command,
                category: 'Other',
                rank: 1
            });
        }

        // Add the command to the palette
        if (palette) {
            palette.addItem({
                command,
                args: { isPalette: true },
                category: PALETTE_CATEGORY
            });
        }
        // Associates file type with icon
        app.docRegistry.addFileType({
            name: 'MATLAB',
            displayName: 'MATLAB File',
            extensions: ['.m'],
            mimeTypes: ['text/x-matlab', 'matlab'],
            icon: matlabIcon
        });
    }
};

/** Adds the MATLAB mode to CodeMirror.
 * app is required, even if it is not used.
 */
const matlabCodeMirrorPlugin: JupyterFrontEndPlugin<void> = {
    id: '@mathworks/matlabCodeMirrorPlugin',
    autoStart: true,
    requires: [ICodeMirror],
    optional: [ILauncher, ICommandPalette],
    activate: (
        app: JupyterFrontEnd,
        codeMirror: ICodeMirror,
    ) => {
        defineMATLABMode(codeMirror);
    }
};

const plugins: JupyterFrontEndPlugin<any>[] = [matlabInBrowserButtonPlugin, matlabMFilesPlugin, matlabCodeMirrorPlugin];
export default plugins;
