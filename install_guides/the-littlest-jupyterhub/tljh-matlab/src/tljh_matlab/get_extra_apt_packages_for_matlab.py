# Copyright 2024 The MathWorks, Inc.

# @package get_extra_apt_packages_for_matlab
#  This module is designed to manage the dependencies required for setting
#  up a MATLAB environment for the R2024a release. It includes functionalities to dynamically
#  fetch and list additional apt packages necessary for the installation on a Ubuntu 22.04 system.

import subprocess
import os

# List of basic extra apt packages required for MATLAB setup.
#  These are the fundamental packages needed across different MATLAB releases and setups.
extra_apt_packages = [
    "wget",
    "unzip",
    "ca-certificates",
    "xvfb",
    "git",
]

# List of dependencies specifically required for MATLAB R2024a.
#  This list includes both the basic packages and those specifically needed for MATLAB R2024a on a Ubuntu 22.04 system.
matlab_deps_for_r2024a = extra_apt_packages + [
    "ca-certificates",
    "libasound2",
    "libc6",
    "libcairo-gobject2",
    "libcairo2",
    "libcap2",
    "libcups2",
    "libdrm2",
    "libfontconfig1",
    "libgbm1",
    "libgdk-pixbuf-2.0-0",
    "libgl1",
    "libglib2.0-0",
    "libgstreamer-plugins-base1.0-0",
    "libgstreamer1.0-0",
    "libgtk-3-0",
    "libice6",
    "libltdl7",
    "libnspr4",
    "libnss3",
    "libpam0g",
    "libpango-1.0-0",
    "libpangocairo-1.0-0",
    "libpangoft2-1.0-0",
    "libsndfile1",
    "libudev1",
    "libuuid1",
    "libwayland-client0",
    "libxcomposite1",
    "libxcursor1",
    "libxdamage1",
    "libxfixes3",
    "libxft2",
    "libxinerama1",
    "libxrandr2",
    "libxt6",
    "libxtst6",
    "libxxf86vm1",
    "locales",
    "locales-all",
    "make",
    "net-tools",
    "procps",
    "sudo",
    "unzip",
    "zlib1g",
]


# Retrieves the list of extra apt packages required for The Littlest JupyterHub (TLJH) setup with MATLAB dependencies.
#  This function dynamically fetches the dependencies by executing a bash script and reading its output.
#  In case of any failure, it defaults to returning a static list of dependencies for MATLAB R2024a.
#  @return Returns a list of apt package dependencies.
def get_extra_apt_packages_for_matlab_impl():

    try:
        script = os.path.join(
            os.path.dirname(__file__), "bash_scripts/get-matlab-deps.sh"
        )
        result = subprocess.call(
            [
                "bash",
                script,
            ],
            env={
                "MATLAB_RELEASE": os.environ.get("MATLAB_RELEASE", "R2024a"),
                "OS": "ubuntu22.04",
            },
        )

        if result == 0:
            # No error, read file
            deps_file = "base-dependencies.txt"

            with open(deps_file) as f:
                matlab_deps = f.read().splitlines()

            if "404: Not Found" in matlab_deps:
                raise Exception("Invalid Release or OS Specified to fetch matlab-deps")
            print(f"extra libs: ${matlab_deps}")

            # Drool clean
            os.remove(deps_file)

            return extra_apt_packages + matlab_deps
        else:
            # In case the bash script above fails, return a list for R2024a
            return matlab_deps_for_r2024a
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise err


get_extra_apt_packages_for_matlab_impl()
