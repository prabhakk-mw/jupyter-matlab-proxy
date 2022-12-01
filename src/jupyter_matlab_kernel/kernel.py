# Copyright 2022 The MathWorks, Inc.
# Implementation of MATLAB Kernel

# Import Python Standard Library
import os
import time

# Import Dependencies
import ipykernel.kernelbase
import requests
from requests.exceptions import HTTPError

from jupyter_matlab_kernel import mwi_comm_helpers


class MATLABConnectionError(Exception):
    """
    A connection error occurred while connecting to MATLAB.

    Args:
        message (string): Error message to be displayed
    """

    def __init__(self, message=None):
        if message is None:
            message = 'Error connecting to MATLAB. Check the status of MATLAB by clicking the "Open MATLAB Desktop" button. Restart the kernel after MATLAB is running successfully'
        super().__init__(message)


def start_matlab_proxy():
    """
    Start matlab-proxy registered with the jupyter server which started the
    current kernel process.

    Raises:
        MATLABConnectionError: Occurs when kernel is not started by jupyter server.
        HTTPError: Occurs when kernel cannot connect with matlab-proxy.

    Returns:
        Tuple (string, string, dict):
            url (string): Complete URL to send HTTP requests to matlab-proxy
            base_url (string): Complete base url for matlab-proxy provided by jupyter server
            headers (dict): HTTP headers required while sending HTTP requests to matlab-proxy
    """

    found_nb_server = False
    nb_server_list = []

    # The matlab-proxy server, if running, could have been started by either
    # "jupyter_server" or "notebook" package.
    try:
        from jupyter_server import serverapp

        nb_server_list += list(serverapp.list_running_servers())

        from notebook import notebookapp

        nb_server_list += list(notebookapp.list_running_servers())
    except ImportError:
        pass

    # Use parent process id of the kernel to filter Jupyter Server from the list
    ppid = os.getppid()
    nb_server = dict()

    for server in nb_server_list:
        if server["pid"] == ppid:
            found_nb_server = True
            nb_server = server

    # Fetch JupyterHub API token for HTTP request authentication
    # incase the jupyter server is started by JupyterHub.
    jh_api_token = os.getenv("JUPYTERHUB_API_TOKEN")

    if found_nb_server:
        url = "{protocol}://localhost:{port}{base_url}matlab".format(
            protocol="https" if nb_server["secure"] else "http",
            port=nb_server["port"],
            base_url=nb_server["base_url"],
        )

        token = nb_server["token"] if jh_api_token is None else jh_api_token
        headers = {
            "Authorization": f"token {token}",
        }

        # send request to the matlab-proxy endpoint to make sure it is available.
        # If matlab-proxy is not started, jupyter-server starts it at this point.
        resp = requests.get(url, headers=headers, verify=False)
        if resp.status_code == requests.codes.OK:
            return url, nb_server["base_url"], headers
        else:
            resp.raise_for_status()
    else:
        raise MATLABConnectionError(
            "Kernel needs to be started by a Jupyter Server. Please use JupyterLab or Classic Notebook while using MATLAB Kernel for Jupyter."
        )


class MATLABKernel(ipykernel.kernelbase.Kernel):
    # Required variables for Jupyter Kernel to function
    # banner is shown only for Jupyter Console.
    banner = "MATLAB"
    implementation = "jupyter_matlab_kernel"
    implementation_version: str = "0.0.1"

    # Values should be same as Codemirror mode
    language_info = {
        "name": "matlab",
        "mimetype": "text/x-matlab",
        "file_extension": ".m",
    }

    # MATLAB Kernel state
    is_matlab_licensed: bool = False
    matlab_status = ""
    server_base_url = ""
    headers = dict()
    startup_error = None
    startup_checks_completed: bool = False

    def __init__(self, *args, **kwargs):
        # Call superclass constructor to initialize ipykernel infrastructure
        super(MATLABKernel, self).__init__(*args, **kwargs)
        try:
            # Start matlab-proxy using the jupyter-matlab-proxy registered endpoint
            self.murl, self.server_base_url, self.headers = start_matlab_proxy()
            (
                self.is_matlab_licensed,
                self.matlab_status,
            ) = mwi_comm_helpers.fetch_matlab_proxy_status(self.murl, self.headers)
        except (MATLABConnectionError, HTTPError) as err:
            self.startup_error = err

    # ipykernel Interface API
    # https://ipython.readthedocs.io/en/stable/development/wrapperkernels.html

    def do_execute(
        self,
        code,
        silent,
        store_history=True,
        user_expressions=None,
        allow_stdin=False,
        *,
        cell_id=None,
    ):
        """
        Used by ipykernel infrastructure for execution. For more info, look at
        https://jupyter-client.readthedocs.io/en/stable/messaging.html#execute
        """
        try:
            # Complete one-time startup checks before sending request to MATLAB.
            # Blocking call, returns after MATLAB is started.
            if not self.startup_checks_completed:
                self.perform_startup_checks()
                self.startup_checks_completed = True

            # Perform execution and categorization of outputs in MATLAB. Blocks
            # until execution results are received from MATLAB.
            outputs = mwi_comm_helpers.send_execution_request_to_matlab(
                self.murl, self.headers, code
            )

            # Clear the output area of the current cell. This removes any previous
            # outputs before publishing new outputs.
            self.display_output({"type": "clear_output", "content": {"wait": False}})

            # Display all the outputs produced during the execution of code.
            for data in outputs:
                # Ignore empty values returned from MATLAB.
                if not data:
                    continue
                self.display_output(data)
        except Exception as e:
            self.send_response(
                self.iopub_socket, "stream", {"name": "stderr", "text": str(e)}
            )
        return {
            "status": "ok",
            "execution_count": self.execution_count,
            "payload": [],
            "user_expressions": {},
        }

    def do_complete(self, code, cursor_pos):
        # TODO: Implement Tab completion
        return super().do_complete(code, cursor_pos)

    def do_is_complete(self, code):
        # TODO: Seems like indentation rules. https://jupyter-client.readthedocs.io/en/stable/messaging.html#code-completeness
        return super().do_is_complete(code)

    def do_inspect(self, code, cursor_pos, detail_level=0, omit_sections=...):
        # TODO: Implement Shift+Tab functionality. Can be used to provide any contextual information.
        return super().do_inspect(code, cursor_pos, detail_level, omit_sections)

    def do_history(
        self,
        hist_access_type,
        output,
        raw,
        session=None,
        start=None,
        stop=None,
        n=None,
        pattern=None,
        unique=False,
    ):
        # TODO: Implement accessing history in Notebook. Usually this history is related to the code typed in notebook.
        # However, we may also choose to associate with MATLAB History stored on disk.
        return super().do_history(
            hist_access_type, output, raw, session, start, stop, n, pattern, unique
        )

    def do_shutdown(self, restart):
        # TODO: Implement clean-up
        return super().do_shutdown(restart)

    # Helper functions

    def perform_startup_checks(self):
        """
        One time checks triggered during the first execution request. Displays
        login window if matlab is not licensed using matlab-proxy.

        Raises:
            HTTPError, MATLABConnectionError: Occurs when matlab-proxy is not started or kernel cannot
                                              communicate with MATLAB.
        """
        # Incase an error occurred while kernel initialization, display it to the user.
        if self.startup_error is not None:
            raise self.startup_error

        iframe_display_style = "none"
        if not self.is_matlab_licensed:
            iframe_display_style = "block"

        # Display iframe containing matlab-proxy. The iframe serves two purposes.
        # 1. Show login window if MATLAB is not licensed using matlab-proxy. After licensing is
        #    completed, the iframe is hidden.
        # 2. Render MATLAB desktop in background. When kernel is communicating with MATLAB for
        #    Jupyter related requests, MATLAB would wait until the desktop is rendered completely
        #    to ensure all services are initialized.
        #
        # The iframe is removed after first MATLAB completes first execution request.
        #
        # This approach does not work when using the kernel in VS Code. We are using relative path
        # as src for iframe to avoid hardcoding any hostname/domain information. This is done to
        # ensure the kernel works in Jupyter deployments. VS Code however does not work the same way
        # as other browser based Jupyter clients.
        #
        # TODO: Find a workaround for users to be able to use our Jupyter kernel in VS Code.
        self.display_output(
            {
                "type": "display_data",
                "content": {
                    "data": {
                        "text/html": f"""<iframe id="matlabLogin" src={self.server_base_url + "matlab"} width=700 height=600 style="display:{iframe_display_style}"></iframe>
                                        <script>
                                            function hideIframe() {{
                                                matlabLoginIframe = document.getElementById("matlabLogin")
                                                if (matlabLoginIframe.contentDocument.getElementById("MatlabJsd") != null) {{
                                                    matlabLoginIframe.style.display = 'none';
                                                }}
                                            }};
                                            setInterval(hideIframe, 200);
                                        </script>"""
                    },
                    "metadata": {},
                },
            }
        )

        # Wait until MATLAB is started before sending requests.
        timeout = 0
        while self.matlab_status != "up" and timeout != 15:
            if self.is_matlab_licensed:
                timeout += 1
            time.sleep(1)
            (
                self.is_matlab_licensed,
                self.matlab_status,
            ) = mwi_comm_helpers.fetch_matlab_proxy_status(self.murl, self.headers)

        # If MATLAB is not available after 15 seconds, display connection
        # error to the user.
        if timeout == 15:
            raise MATLABConnectionError

    def display_output(self, out):
        """
        Common function to send execution outputs to Jupyter UI.
        For more information, look at https://jupyter-client.readthedocs.io/en/stable/messaging.html#messages-on-the-iopub-pub-sub-channel

        Input Example:
        1.  Execution Output:
            out = {
                "type": "execute_result",
                "mimetype": ["text/plain","text/html"],
                "value": ["Hello","<html><body>Hello</body></html>"]
            }
        2.  For all other message types:
            out = {
                "type": "stream",
                "content": {
                    "name": "stderr",
                    "text": "An error occurred"
                }
            }

        Args:
            out (dict): A dictionary containing the type of output and the content of the output.
        """
        msg_type = out["type"]
        if msg_type == "execute_result":
            assert len(out["mimetype"]) == len(out["value"])
            response = {
                # Use zip to create a tuple of KV pair of mimetype and value.
                "data": dict(zip(out["mimetype"], out["value"])),
                "metadata": {},
                "execution_count": self.execution_count,
            }
        else:
            response = out["content"]
        self.send_response(self.iopub_socket, msg_type, response)