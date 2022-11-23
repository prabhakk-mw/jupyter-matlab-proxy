# Jupyter MATLAB Kernel

This package provides a MATLAB language kernel for Jupyter. It is provided as an
part of [MATLAB Integration for Jupyter](../../README.md).

## Supported Features
* Execution of MATLAB code
* Inline static plot images
* LaTeX representation for symbolic expressions
* Function definition within .ipynb file

## Known Issues
* Executing MATLAB code which requires user input such as `input`, `keyboard`
will result in undefined behavior.
