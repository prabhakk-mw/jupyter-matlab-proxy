# Running MATLAB Integration for Jupyter on The Littlest JupyterHub in a Docker Container

This guide customizes a **"The Littlest JupyterHub"** aka **TLJH** stack to include MATLAB, its dependencies and the MATLAB Integration for Jupyter.

**TLJH** can run on several modern linux environments. For a full listing for the supported environements, See [Installing (TLJH)](https://tljh.jupyter.org/en/stable/install/index.html).

The rest of this document will use the [Setting up Development Environment (TLJH)](https://tljh.jupyter.org/en/stable/contributing/dev-setup.html) to install TLJH in a Docker Container and customize it to include MATLAB and the MATLAB Integration for Jupyter.

When completed, you will have access to a JupyterHub server running from within your Docker container, capable of serving Jupyter Notebook Servers for multiple users at `http://Your-FQDN:12000`

Customize it to include MATLAB and the MATLAB Integration for Jupyter with the plugin `tljh-matlab` using the following command:

```bash
python3 /srv/src/bootstrap/bootstrap.py --admin admin:password --plugin tljh-matlab
```

### Table of Contents
1. [Set up TLJH with Docker](#set-up-tljh-with-docker)
2. [Customize Installation to include MATLAB](#customize-installation-to-include-matlab)


## Set up TLJH with Docker

The following lines are taken directly from [Setting up Development Environment (TLJH)](https://tljh.jupyter.org/en/stable/contributing/dev-setup.html) for your convenience. We **highly** recommend following the instruction directly from the link above. 

> The easiest & safest way to develop & test TLJH is with [Docker](https://www.docker.com/).
> 
> 1. Install Docker Community Edition by following the instructions on [their website](https://www.docker.com/community-edition).
> 1. Clone the [git repo](https://github.com/jupyterhub/the-littlest-jupyterhub) (or your fork of it).
> 
> 1. Build a docker image that has a functional systemd in it.
>       ```bash
>       git clone https://github.com/jupyterhub/the-littlest-jupyterhub && cd the-littlest-jupyterhub 
>       docker build -t tljh-systemd . -f integration-tests/Dockerfile
>       ```
> 1. Run a docker container with the image in the background, while bind mounting your TLJH repository under `/srv/src`.
>       ```bash 
>       docker run \
>       --privileged \
>       --detach \
>       --name=tljh-dev \
>       --publish 12000:80 \
>       --mount type=bind,source="$(pwd)",target=/srv/src \
>       tljh-systemd
>       ```
> 1. Get a shell inside the running docker container.
>       ```bash
>       docker exec -it tljh-dev /bin/bash
>       ```
> 1. Run the bootstrapper from inside the container (see step above): The container image is already set up to default to a `dev` install, so it’ll install from your local repo rather than from github.
>       ```bash
>       python3 /srv/src/bootstrap/bootstrap.py --admin admin
>       ```
> 1. Or, if you would like to setup the admin’s password during install, you can use this command (replace “admin” with the desired admin username and “password” with the desired admin password):
>       ```bash
>       python3 /srv/src/bootstrap/bootstrap.py --admin admin:password
>       ```
> 
>   The primary hub environment will also be in your PATH already for convenience.
>   
>   You should be able to access the JupyterHub from your browser now at http://localhost:12000. 
>   
>   **Congratulations**, you are set up to develop TLJH!
> 

## Customize Installation to include MATLAB
TLJH can install additional *plugins* to customize the installation.
See [Installing TLJH plugins](https://tljh.jupyter.org/en/stable/topic/customizing-installer.html) for more information.

This repository publishes a python package `tljh-matlab` which installs MATLAB, its dependencies and the MATLAB integration for Jupyter into TLJH.

To install the plugin, run the `bootstrap.py` script in `step 6.` from the previous section, as shown below:
```bash
python3 /srv/src/bootstrap/bootstrap.py --admin admin:password --plugin tljh-matlab
```


Customize it using `tljh-matlab` ([TLJH Plugin](https://tljh.jupyter.org/en/stable/contributing/plugins.html) for MATLAB)


## Background Reading
### TLJH
A simple JupyterHub distribution for a small (0-100) number of users on a single server.

Refer to the official documentation of [The Littlest JupyterHub](https://tljh.jupyter.org/en/stable/index.html) for more information on capabilities and installation guides.

We recommend reading [When to use The Littlest JupyterHub](https://tljh.jupyter.org/en/stable/topic/whentouse.html) to determine if TLJH right tool for you.