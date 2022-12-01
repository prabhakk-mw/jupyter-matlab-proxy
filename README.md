# MATLAB Integration for Jupyter

The MATLAB Integration for Jupyter allows you to develop and execute MATLAB code in a Jupyter notebook.

This integration is comprised of a Jupyter kernel, a Jupyterlab labextension, and a proxy.
For MATLAB code written in JupyterLab, this integration enables certain features.
* [Kernel](src/jupyter_matlab_kernel/README.md)
  * execute MATLAB code
  * write code using tab completion
* [Labextension](src/jupyter_matlab_labextension/README.md)
  * write code with syntax highlighting and autoindentation
* [Proxy](src/jupyter_matlab_proxy/README.md)
  * access MATLAB in a browser from your Jupyter environment 

<p align="center">
  <img width="600" src="img/jupyterlab_cell_example.png">
</p>

For more detail, on how to use these features see [Usage](#usage).
For more information on the features associated with each component, see
the [kernel README](src/jupyter_matlab_kernel/README.md),
the [labextension README](src/jupyter_matlab_labextension/README.md),
and the [proxy README](src/jupyter_matlab_proxy/README.md).

To report any issues or suggestions, see the [Feedback](#feedback) section.

----
## Requirements [TO CHECK]

* MATLAB® R2020b or later is installed and on the system PATH.
  ```bash
  # Confirm MATLAB is on the PATH
  which matlab
  ```  
* The dependencies required to run MATLAB.
  Refer to the Dockerfiles in the [matlab-deps](https://github.com/mathworks-ref-arch/container-images/tree/master/matlab-deps) repository for the desired version of MATLAB.

* JupyterLab version: **3** [TO CHECK]

* Python versions: **3.7** | **3.8** | **3.9**  | **3.10**
  
* X Virtual Frame Buffer (Xvfb) : (only for Linux® based systems)

  [** TO CHECK: This should be automatically installed as a dependency?**]

  Install it on your linux machine using:
  ```bash
  # On a Debian/Ubuntu based system:
  $ sudo apt install xvfb
  ```
  ```bash
  # On a RHEL based system:
  $ yum search Xvfb
  xorg-x11-server-Xvfb.x86_64 : A X Windows System virtual framebuffer X server.
  $ sudo yum install xorg-x11-server-Xvfb
  ```
* Python versions: **3.7** | **3.8** | **3.9**  | **3.10**
* [Browser Requirements](https://www.mathworks.com/support/requirements/browser-requirements.html)

* Supported Operating Systems:
    * Linux®
    * Windows® Operating System ( starting v0.4.0 of matlab-proxy )
    * MacOS (starting v0.5.0 of matlab-proxy )

## Installation

### PyPI
This repository can be installed directly from the Python Package Index.
```bash
python -m pip install jupyter-matlab-proxy
```

Installing this package will also install [JupyterLab](https://jupyterlab.readthedocs.io/en/stable/) and [Jupyter Server Proxy](https://jupyter-server-proxy.readthedocs.io/en/latest/) on your machine, if they are not installed already.

You must have [MATLAB](https://www.mathworks.com/help/install/install-products.html) installed to execute MATLAB code through Jupyter.

### Building From Sources
```bash
git clone https://github.com/mathworks/jupyter-matlab-proxy.git

cd jupyter-matlab-proxy

python -m pip install .
```

## Usage

## Starting JupyterLab

Upon successful installation of `jupyter-matlab-proxy`, your Jupyter environment should present options to launch a
Jupyter notebook with a MATLAB kernel, and to access MATLAB in a browser.

* Open your Jupyter environment by starting jupyter notebook or lab
  ```bash
  # For Jupyter Notebook
  jupyter notebook

  # For Jupyter Lab
  jupyter lab 
  ```

### JupyterLab options

* **TODO: Add screenshots once kernel is integrated and icons are finalised.**

<p align="center">
  <img width="600" src="img/jupyterlab_icons.png">
</p>

  | Icon |  Description |
  | ---- | ---- |
  | A | Access MATLAB in a browser. |
  | B | Open a notebook with a MATLAB kernel. |
  | C | Open a console with a MATLAB session. |
  | D | Open a new MATLAB file. You can also open a MATLAB file using the command palette **TODO: expand/move** |

* The first time you execute code in a MATLAB notebook you will be asked to log in,
or use a network license manager. Follow the [licensing](#licensing) instructions below.
* Wait for the MATLAB session to start. This can take several minutes.
* Each MATLAB notebook is backed by the same MATLAB session, and therefore allows access to the same state.

## Licensing

* If prompted to do so, enter credentials for a MathWorks account associated with a MATLAB license. If you are using a network license manager, change to the _Network License Manager_ tab and enter the license server address instead. To determine the appropriate method for your license type, consult [MATLAB Licensing Info](https://github.com/mathworks/jupyter-matlab-proxy/blob/main/MATLAB-Licensing-Info.md).

<p align="center">
  <img width="400" src="https://github.com/mathworks/jupyter-matlab-proxy/raw/main/img/licensing_GUI.png">
</p>

## Limitations
This package supports the same subset of MATLAB features and commands as MATLAB® Online, except there is no support for Simulink® Online.
[Click here for a full list of Specifications and Limitations for MATLAB Online](https://www.mathworks.com/products/matlab-online/limitations.html). 

If you need to use functionality that is not yet supported, or for versions of MATLAB earlier than R2020b, you can use the alternative [MATLAB Integration for Jupyter using VNC](https://github.com/mathworks/jupyter-matlab-vnc-proxy).

## Integration with JupyterHub

To use this integration with JupyterHub®, you must install the `jupyter-matlab-proxy` Python package in the Jupyter environment launched by your JupyterHub platform. 

For example, if your JupyterHub platform launches Docker containers, then install this package in the Docker image used to launch them.

A reference architecture that installs `jupyter-matlab-proxy` in a Docker image is available at: [Use MATLAB Integration for Jupyter in a Docker Container](https://github.com/mathworks-ref-arch/matlab-integration-for-jupyter/tree/main/matlab).

## Troubleshooting
For a guide to troubleshooting issues with MATLAB proxy, see [Troubleshooting](src/jupyter_matlab_proxy/README.md#troubleshooting).

## Feedback

We encourage you to try this repository with your environment and provide feedback.
If you encounter a technical issue or have an enhancement request, create an issue [here](https://github.com/mathworks/jupyter-matlab-proxy/issues) or send an email to `jupyter-support@mathworks.com`

----

Copyright (c) 2021-2022 The MathWorks, Inc. All rights reserved.

----
