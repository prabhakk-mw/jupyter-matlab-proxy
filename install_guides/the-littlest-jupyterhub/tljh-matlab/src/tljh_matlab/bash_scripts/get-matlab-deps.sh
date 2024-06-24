#!/bin/bash
# Copyright 2024 The MathWorks, Inc.

# Example invocation:
# subprocess.call(["bash", "/mathworks/devel/sandbox/prabhakk/cit/jupyter/tljh/the-littlest-jupyterhub/tljh_matlab/get-matlab-deps"],
#                     env={"MATLAB_RELEASE":"R2024a", "OUTPUT_FILE":"myfile.txt", "OS":"ubuntu20.04"})

# Set the default release to R2024a.
MATLAB_RELEASE="${MATLAB_RELEASE:-"r2024a"}"
# Lowercase first letter, to form correct URL
MATLAB_RELEASE="${MATLAB_RELEASE,}"

# Set the default OS to ubuntu22.04
OS="${OS:-"ubuntu22.04"}"

MATLAB_DEPS_REQUIREMENTS_FILE="https://raw.githubusercontent.com/mathworks-ref-arch/container-images/main/matlab-deps/${MATLAB_RELEASE}/${OS}/base-dependencies.txt"

echo "Fetching dependencies for ${MATLAB_RELEASE}"
curl -O -s ${MATLAB_DEPS_REQUIREMENTS_FILE}
