# MATLAB Kernel for Jupyter

This module is a part of the `jupyter-matlab-proxy` package and it provides a MATLAB language kernel for Jupyter.

## Usage

Upon successful installation of `jupyter-matlab-proxy`, your Jupyter environment should present options to launch MATLAB.

* Open your Jupyter environment by starting jupyter notebook or lab
  ```bash
  # For Jupyter Notebook
  jupyter notebook

  # For Jupyter Lab
  jupyter lab 
  ```

Launch the kernel using the `MATLAB Kernel` option on your Jupyter environment:
|Classic Jupyter | JupyterLab |
|--|--|
|<p align="center"><img width="600" src="../../img/classic-jupyter.png"></p> | <p align="center"><img width="600" src="../../img/jupyterlab-notebook-section.png"></p> |

Please note that a single MATLAB process is used to back all MATLAB notebooks in a given Juptyer session. This implies that all notebooks access the same MATLAB workspace, and explicit care must be taken by notebook authors to avoid 


## Supported Features
* Execution of MATLAB code
* Tab completion
* Inline static plot images
* LaTeX representation for symbolic expressions
* Function definition within notebooks. Functions can only be accessed in the cells that they are defined in.

## Limitations
* Executing MATLAB code which requires user input such as `input`, `keyboard` are not supported.
* Kernels cannot restart MATLAB automatically when users explicitly shut MATLAB down using the `exit` command or through the web desktop interface.

## Feedback

We encourage you to try this repository with your environment and provide feedback.
If you encounter a technical issue or have an enhancement request, create an issue [here](https://github.com/mathworks/jupyter-matlab-proxy/issues) or send an email to `jupyter-support@mathworks.com`

----

Copyright (c) 2022 The MathWorks, Inc. All rights reserved.

----
