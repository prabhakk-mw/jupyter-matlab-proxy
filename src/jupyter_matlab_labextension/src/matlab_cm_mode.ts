// Copyright 2022 The MathWorks, Inc.

import {
    JupyterFrontEnd,
    JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { ICodeMirror } from '@jupyterlab/codemirror';
/** TODO Button appear when changing to MATLAB kernel, disappear when changing away.
 * TODO highlighting after "format"
 * TODO methods and properties inside classdefs
 * TODO arguments and mustBeNumeric in function definition */

/** Of the default codemirror tokens, "keyword" matches MATLAB comment style best,
 * and variable-2 matches MATLAB keyword style best. These tokens are only used for
 * display and not for execution. */
export const token_to_matlab_style = new Map<string, string>([
    ["comment", "keyword"],
    ["string", "string-2"],
    ["keyword", "variable-2"]
]);

const baseRegex = [
    /** The boolean "sol" is needed as the ^ regexp marker doesn't
     * work as you'd expect in this context because of limitations in JavaScript's RegExp API.
     * See https://codemirror.net/5/demo/simplemode.html. */
    { regex: /([\s]*)(%\{)[^\S\n]*$/, token: token_to_matlab_style.get("comment"), next: 'comment', sol: true },
    { regex: /%.*$/, token: token_to_matlab_style.get("comment") },
    { regex: /".*?("|$)/, token: token_to_matlab_style.get("string") },
    { regex: /'.*?('|$)/, token: token_to_matlab_style.get("string") },
    { regex: /\b(break|case|classdef|continue|global|otherwise|persistent|return|spmd)\b/, token: token_to_matlab_style.get("keyword") },
    { regex: /(\bimport\b)(.*)(?=;|%|$)/, token: ['variable', 'meta', 'variable'] },
    { regex: /\b(arguments|enumeration|events|for|function|if|methods|parfor|properties|try|while)\b/, indent: true, token: token_to_matlab_style.get("keyword") },
    { regex: /\b(switch)\b/, indent: true, token: token_to_matlab_style.get("keyword") }, //, next: "switch"},
    { regex: /\b(catch|else|elseif)\b/, indent: true, dedent: true, token: token_to_matlab_style.get("keyword") },
    { regex: /\b(?:end)\b/, dedent: true, token: token_to_matlab_style.get("keyword") },
    /** Removing (or adding \s* around) this line breaks tab completion. */
    { regex: /[a-zA-Z_]\w*/, token: "variable" }
];

/** "Case" needs to be dedented, unless it's after switch;
 * this can be handled using a special state.
 * Keyword "end" after switch needs two dedents.
 * Going to skip case for the moment (which means leaving out "otherwise" too).
 * User will have to manually indent code inside case sections,
 * less pain than being stuck with too many indents. */
const startRegex = baseRegex;// [{regex: /\b(case)\b/, indent:true, dedent: true, token: "keyword"}, ...baseRegex]
// let switchRegex = [{regex: /\b(case)\b/, indent:true, token: "keyword", next: "start"}, ...baseRegex]
const multilineCommentRegex = [
    { regex: /([\s]*)(%\})[^\S\n]*(?:$)/, token: token_to_matlab_style.get("comment"), next: 'start', sol: true },
    { regex: /.*/, token: token_to_matlab_style.get("comment") }
];

/** Install mode in CodeMirror */
export function defineMATLABMode ({ CodeMirror }: ICodeMirror) {
    CodeMirror.defineSimpleMode('matlab', {
        start: startRegex,
        comment: multilineCommentRegex,
        // switch: switchRegex,
        meta: {
            lineComment: '%',
            electricInput: /^\s*(?:catch|else|elseif|end|otherwise)$/,
            dontIndentStates: ['comment']
        }
    });

    CodeMirror.defineMIME('text/x-matlab', 'matlab');

    CodeMirror.modeInfo.push({
        name: 'MATLAB',
        mime: 'text/x-matlab',
        mode: 'matlab',
        ext: ['m'],
        file: /^[a-zA-Z][a-zA-Z0-9_]*\.m$/
    });
}

export const matlabCodeMirrorPlugin: JupyterFrontEndPlugin<void> = {
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
