// Copyright 2022 The MathWorks, Inc.

import { LabIcon } from '@jupyterlab/ui-components';

import membraneSvgStr from '../style/icons/membrane.svg';
import mFileSvgStr from '../style/icons/mFile.svg';

export const matlabIcon = new LabIcon({
    name: 'matlabIcon',
    svgstr: membraneSvgStr
});

export const mFileIcon = new LabIcon({
    name: 'mFileIcon',
    svgstr: mFileSvgStr
});
