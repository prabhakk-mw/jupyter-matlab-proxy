# Copyright 2024 The MathWorks, Inc.

"""
MATLAB plugin that installs MATLAB, its dependencies and the MATLAB Integration for Jupyter
"""

from tljh.hooks import hookimpl

from . import get_extra_apt_packages_for_matlab
from . import install_matlab


@hookimpl
def tljh_extra_user_pip_packages():
    return ["jupyter-matlab-proxy"]


@hookimpl
def tljh_extra_apt_packages():
    return get_extra_apt_packages_for_matlab.get_extra_apt_packages_for_matlab_impl()


@hookimpl
def tljh_post_install():
    """
    Post install script to be executed after installation
    and after all the other hooks.

    This can be arbitrary Python code.
    """
    install_matlab.install_matlab_impl()


# @hookimpl
# def tljh_custom_jupyterhub_config(c):
#     # c.Test.jupyterhub_config_set_by_matlab_plugin = True
#     # c.JupyterHub.services.cull.every = 60
#     # c.JupyterHub.services.cull.timeout = 180
#     # # Dont set a max age, and dont cull users (these are default anyways)
#     # c.JupyterHub.services.cull.max_age = 0
#     # c.JupyterHub.services.cull.users = False
#     # c.JupyterHub.services.cull.users = False


# @hookimpl
# def tljh_config_post_install(config):
#     config["Test"] = {"tljh_config_set_by_matlab_plugin": True}


# @hookimpl
# def tljh_new_user_create(username):
#     with open("test_new_user_create", "w") as f:
#         f.write("tljh_config_set_by_matlab_plugin")
#         f.write(username)
