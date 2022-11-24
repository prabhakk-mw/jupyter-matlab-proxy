// Copyright 2022 The MathWorks, Inc.

import { ToolbarButton } from '@jupyterlab/apputils';
import { PageConfig } from '@jupyterlab/coreutils';
import { DocumentRegistry } from '@jupyterlab/docregistry';
import { INotebookModel, NotebookPanel } from '@jupyterlab/notebook';

import { IDisposable } from '@lumino/disposable';

import { matlabIcon } from './icons';

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
