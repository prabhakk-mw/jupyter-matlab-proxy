# Jupyter MATLAB Proxy
----
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/mathworks/jupyter-matlab-proxy/MATLAB%20Jupyter%20Integration?logo=github)](https://github.com/mathworks/jupyter-matlab-proxy/actions) [![PyPI badge](https://img.shields.io/pypi/v/jupyter-matlab-proxy.svg?logo=pypi)](https://pypi.python.org/pypi/jupyter-matlab-proxy) [![codecov](https://codecov.io/gh/mathworks/jupyter-matlab-proxy/branch/main/graph/badge.svg?token=ZW3SESKCSS)](https://codecov.io/gh/mathworks/jupyter-matlab-proxy)

---

The Jupyter MATLAB Proxy enables you to access MATLAB in a web browser from your Jupyter environment.
It is provided as part of the [MATLAB Integration for Jupyter](../../README.md).

`jupyter-matlab-proxy` is a Python® package based on the following packages.
| Package | Description |
|----|----|
| [matlab-proxy](https://github.com/mathworks/matlab-proxy) | Provides infrastructure to launch MATLAB and connect to it from a web browser.|
| [jupyter-server-proxy](https://github.com/jupyterhub/jupyter-server-proxy) | Extends Jupyter environments to launch MATLAB as an external process alongside the notebook server. For more information see [GUI Launchers](https://jupyter-server-proxy.readthedocs.io/en/latest/launchers.html#jupyterlab-launcher-extension).|

To report any issues or suggestions, see the [Feedback](#feedback) section.

----
## Usage

Upon successful installation of `jupyter-matlab-proxy`, your Jupyter environment should present options to launch MATLAB.

* Open your Jupyter environment by starting jupyter notebook or lab
  ```bash
  # For Jupyter Notebook
  jupyter notebook

  # For Jupyter Lab
  jupyter lab 
  ```

* If you are using Jupyter Notebook (on the left in figure below), on the `New` menu, select `MATLAB`. If you are using JupyterLab (on the right in figure below), select the MATLAB icon on the launcher.

<p align="center">
  <img width="600" src="https://github.com/mathworks/jupyter-matlab-proxy/raw/main/img/combined_launchers.png">
</p>

* To enter your license information, see [Licensing](../../README.md#licensing).

* Wait for the MATLAB session to start. This can take several minutes.
<p align="center">
  <img width="800" src="https://github.com/mathworks/jupyter-matlab-proxy/raw/main/img/jupyter_matlab_desktop.png">
</p>

* To manage the MATLAB integration for Jupyter, click the tools icon shown below.

<p align="center">
  <img width="100" src="https://github.com/mathworks/jupyter-matlab-proxy/raw/main/img/tools_icon.png">
</p>

* Clicking the tools icon opens a status panel with buttons like the ones below:

    <p align="center">
      <img width="800" src="https://github.com/mathworks/jupyter-matlab-proxy/raw/main/img/status_panel.png">
    </p>

   The following options are available in the status panel (some options are only available in a specific context):

  | Option |  Description |
  | ---- | ---- |
  | Start MATLAB Session | Start your MATLAB session. Available if MATLAB is stopped.|
  | Restart MATLAB Session | Restart your MATLAB session. Available if MATLAB is running or starting.|
  | Stop MATLAB Session | Stop your MATLAB session. Use this option if you want to free up RAM and CPU resources. Available if MATLAB is running or starting.|
  | Sign Out | Sign out of MATLAB. Use this to stop MATLAB and sign in with an alternative account. Available if using online licensing.|
  | Unset License Server Address | Unset network license manager server address. Use this to stop MATLAB and enter new licensing information. Available if using network license manager.|
  | Feedback | Send us feedback. This action opens your default email application.|
  | Help | Open a help pop-up for a detailed description of the options.|

## Limitations
This package supports the same subset of MATLAB features and commands as MATLAB® Online, except there is no support for Simulink® Online.
[Click here for a full list of Specifications and Limitations for MATLAB Online](https://www.mathworks.com/products/matlab-online/limitations.html). 

If you need to use functionality that is not yet supported, or for versions of MATLAB earlier than R2020b, you can use the alternative [MATLAB Integration for Jupyter using VNC](https://github.com/mathworks/jupyter-matlab-vnc-proxy).

## Troubleshooting

In the environment that you have installed the package:

* Verify if the MATLAB executable is discoverable (ie. if it is in the PATH)
    ```bash
    $ which matlab
    /usr/local/bin/matlab
    ```

* Check if their Python version is 3.6 or higher
    ```bash
    $ python --version
    Python 3.7.3
    ```

* Ensure that `matlab-proxy-app` and the `jupyter` executables are in the same environment as the python executable.
    For example if youare using VENV to manage your python environments:
    ```bash
    $ which python
    /home/user/my-project/packages/.venv/bin/python

    $ which matlab-proxy-app
    /home/user/my-project/packages/.venv/bin/matlab-proxy-app

    $ which jupyter
    /home/user/my-project/packages/.venv/bin/jupyter
    ```
    Notice that `matlab-proxy-app`, `jupyter` and the `python` executable are in the same parent directory, in this case it is: `/home/user/my-project/packages/.venv/bin`

* Ensure that you are launching `jupyter notebook` using the same executable as listed above.

* Ensure that all three packages are installed in the same python environment
    ```bash
    # Pipe the output of pip freeze and grep for jupyter, matlab-proxy and jupyter-matlab-proxy.
    # All three packages should be highlighted in the output.
    # If you don't see anyone of them, then either the packages missing in the output have been installed
    # in a different python environment or not installed at all.
    $ pip freeze | grep -E "jupyter|matlab-proxy|jupyter-matlab-proxy"
    ```

* If the integration is not showing up as an option to the dropdown box in the Juptyer notebook:
    ```bash
    #Run the following commands and verify that you are able to see similar output:
    
    $ jupyter serverextension list
    config dir: /home/user/anaconda3/etc/jupyter
        jupyter_server_proxy  enabled
        - Validating...
        jupyter_server_proxy  OK
        jupyterlab  enabled
        - Validating...
        jupyterlab 2.2.6 OK
    
    $ jupyter nbextension list
    Known nbextensions:
    config dir: /home/user/anaconda3/etc/jupyter/nbconfig
        notebook section
        jupyter-js-widgets/extension  enabled
        - Validating: OK
        tree section
        jupyter_server_proxy/tree  enabled
        - Validating: OK  $ pip freeze | grep -E "jupyter|matlab-proxy|jupyter-matlab-proxy"
    
    # IF the server does not show up in the commands above, install:
    $ pip install jupyter-contrib-nbextensions
    ```

----

Copyright (c) 2021-2022 The MathWorks, Inc. All rights reserved.

----
