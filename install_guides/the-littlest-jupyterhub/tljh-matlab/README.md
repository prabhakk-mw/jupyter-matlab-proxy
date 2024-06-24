# tljh-matlab

TLJH plugin for [The Littlest JupyterHub](https://tljh.jupyter.org/) that installs MATLAB, and the MATLAB Integration for Jupyter.

The [Littlest JupyterHub installation](https://tljh.jupyter.org/en/latest/topic/customizing-installer.html#installing-tljh-plugins) can install **plugins** that provide additional features, in the JupyterHub stack being provisioned.

The `tljh-matlab` plugin installs:
* A specified version of MATLAB
* The system libraries required by MATLAB 
* The MATLAB Integration for Jupyter, to enable the usage of MATLAB via Notebooks, and to access the MATLAB desktop from Jupyter. See [jupyter-matlab-proxy](github.com/mathworks/jupyter-matlab-proxy) for more information.


Command to install plugin:
```bash
docker run   --privileged   --detach   --name=tljh-dev   --publish 12000:80   --mount type=bind,source="$(pwd)",target=/srv/src  tljh-systemd
docker exec -it tljh-dev /bin/bash
python3 /srv/src/bootstrap/bootstrap.py --admin admin:password --plugin tljh-matlab
```

To customize the default values used by the plugin , set the appropriate environment variable before the `bootstrap` command

| Environment Variable Name | Default Values | Notes|
|--|--|--|
| MATLAB_RELEASE | R2024a | Specify the MATLAB release you would like to install |
| MATLAB_PRODUCT_LIST | "MATLAB Symbolic_Math_Toolbox" | See `--products` section of [MPM.md](https://github.com/mathworks-ref-arch/matlab-dockerfile/blob/main/MPM.md) for information on the supported products and their name specification. For example to install Simulink along with MATLAB use `"MATLAB Simulink"` |
|MATLAB_INSTALL_DESTINATION| /opt/matlab/R2024a | Specify the path to the location you would like to install MATLAB |
| OS | ubuntu22.04 | See [matlab-deps](https://github.com/mathworks-ref-arch/container-images/tree/main/matlab-deps/r2024a) for the list of supported OS values by Release.|

Example:
```bash
env MATLAB_RELEASE=R2023b MATLAB_PRODUCT_LIST="MATLAB Simulink" python3 /srv/src/bootstrap/bootstrap.py --admin admin:password --plugin tljh-matlab
```



----

Copyright 2024 The MathWorks, Inc.

----