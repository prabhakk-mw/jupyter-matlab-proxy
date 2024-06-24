# Copyright 2024 The MathWorks, Inc.

import subprocess
import os

# @package install_matlab
#  This module provides functionalities to install MATLAB using a bash script.


def install_matlab_impl():
    """
    @brief Installs MATLAB using a predefined bash script.

    This function constructs the path to a bash script responsible for installing MATLAB and executes it.
    The MATLAB release and product list are specified through environment variables. If not present, defaults are used.

    @param None
    @return None
    """
    # Construct the path to the install script
    script = os.path.join(os.path.dirname(__file__), "bash_scripts/install-matlab.sh")

    # Call the bash script with environment variables
    subprocess.call(
        [
            "bash",
            script,
        ],
        env={
            # Default to R2024a if not specified
            "MATLAB_RELEASE": os.environ.get("MATLAB_RELEASE", "R2024a"),
            # Default products if not specified
            "MATLAB_PRODUCT_LIST": os.environ.get(
                "MATLAB_PRODUCT_LIST", "MATLAB Symbolic_Math_Toolbox"
            ),
        },
    )


# Execute the install function
install_matlab_impl()
