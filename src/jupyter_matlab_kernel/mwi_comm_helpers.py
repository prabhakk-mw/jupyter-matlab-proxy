# Copyright 2022 The MathWorks, Inc.
# Helper functions to communicate with matlab-proxy and MATLAB

import pathlib

import requests
from matlab_proxy.util.mwi.embedded_connector.helpers import (
    get_data_to_feval_mcode,
    get_mvm_endpoint,
)


def fetch_matlab_proxy_status(url, headers):
    """
    Sends HTTP request to /get_status endpoint of matlab-proxy and returns
    license and MATLAB status.

    Args:
        url (string): Url of matlab-proxy server
        headers (dict): HTTP headers required for communicating with matlab-proxy.

    Returns:
        Tuple (bool, string):
            is_matlab_licensed (bool): True if matlab-proxy has license information, else False.
            matlab_status (string): Status of MATLAB. Values could be "up", "down" and "starting"
    
    Raises:
        HTTPError: Occurs when connection to matlab-proxy cannot be established.
    """
    resp = requests.get(url + "/get_status", headers=headers, verify=False)
    if resp.status_code == requests.codes.OK:
        data = resp.json()
        is_matlab_licensed = data["licensing"] != None
        matlab_status = data["matlab"]["status"]
        return is_matlab_licensed, matlab_status
    else:
        resp.raise_for_status()


def send_execution_request_to_matlab(url, headers, code):
    """
    Evaluate MATLAB code and capture results.

    Args:
        kernelid (string): A unique kernel identifier.
        url (string): Url of matlab-proxy server
        headers (dict): HTTP headers required for communicating with matlab-proxy
        code (string): MATLAB code to be evaluated

    Returns:
        List(dict): list of outputs captured during evaluation.

    Raises:
        HTTPError: Occurs when connection to matlab-proxy cannot be established.
    """
    resp = _send_jupyter_request_to_matlab(url, headers, "execute", [code])
    return resp["results"][0]


def _send_feval_request_to_matlab(url, headers, fname, nargout, *args):
    req_body = get_data_to_feval_mcode(fname, *args, nargout=nargout)
    resp = requests.post(
        get_mvm_endpoint(url),
        headers=headers,
        json=req_body,
        verify=False,
    )
    if resp.status_code == requests.codes.OK:
        data = resp.json()
        return data["messages"]["FEvalResponse"][0]
    else:
        raise resp.raise_for_status()


def _send_jupyter_request_to_matlab(url, headers, request_type, inputs):
    args = [request_type] + inputs
    resp = _send_feval_request_to_matlab(
        url, headers, "processJupyterKernelRequest", 1, *args
    )
    # The error code returned in response is always MATLAB.codeerror. Hence,
    # we cannot distinguish "function not found" from other errors. Ideally,
    # MATLAB code shipped with kernel should be exception safe and the only
    # error when sending request to MATLAB should be "function not found".
    #
    # Going by this assumption, if an error is present in the response, we
    # treat it as "function not found" and add the path of MATLAB code shipped
    # with kernel and retry the original request.
    if resp["isError"]:
        temp = [str(pathlib.Path(__file__).parent / "matlab")]
        _send_feval_request_to_matlab(url, headers, "addpath", 0, *temp)
        resp = _send_feval_request_to_matlab(
            url, headers, "processJupyterKernelRequest", 1, *args
        )
    return resp
