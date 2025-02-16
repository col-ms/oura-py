import requests
import logging
from typing import Dict
from json import JSONDecodeError
from urllib3.exceptions import InsecureRequestWarning
from .exceptions import OuraPyException
from .models import Result


class RequestManager:
    def __init__(
        self,
        personal_access_token: str,
        url: str,
        ssl_verify: bool = True,
        logger: logging.Logger = None,
    ):
        """HTTP request manager.

        Args:
            personal_access_token (str): The personal access token for authenticating with the Oura API.
            hostname (str): The API hostname.
            ver (str): The API version.
            ssl_verify (bool, optional): Whether to verify SSL certificates. Defaults to True.
            logger (logging.Logger, optional): Logger instance for logging. Defaults to None.
        """
        self.url = url
        self._personal_access_token = personal_access_token
        self._ssl_verify = ssl_verify
        self._logger = logger or logging.getLogger(__name__)
        if not ssl_verify:
            requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

    def get(self, endpoint: str, params: Dict = None) -> Result:
        """Sends a GET request to the specified endpoint with optional parameters.

        Args:
            endpoint (str): The API endpoint to send the GET request to.
            params (Dict, optional): A dictionary of query parameters to include in the request. Defaults to None.

        Returns:
            Result: The result of the GET request.
        """
        return self._request(method="GET", endpoint=endpoint, params=params)

    def post(self, endpoint: str, params: Dict = None, data: Dict = None) -> Result:
        """
        Sends a POST request to the specified endpoint with the given parameters and data.

        Args:
            endpoint (str): The API endpoint to send the request to.
            params (Dict, optional): The query parameters to include in the request. Defaults to None.
            data (Dict, optional): The data to include in the body of the request. Defaults to None.

        Returns:
            Result: The result of the POST request.
        """
        return self._request(method="POST", endpoint=endpoint, params=params, data=data)

    def _request(
        self, method: str, endpoint: str, params: Dict = None, data: Dict = None
    ) -> Result:
        """
        Makes an HTTP request to the specified endpoint with the given method, parameters, and data.

        Args:
            method (str): The HTTP method to use for the request (e.g., 'GET', 'POST').
            endpoint (str): The API endpoint to send the request to.
            params (Dict, optional): The query parameters to include in the request. Defaults to None.
            data (Dict, optional): The data to include in the request body. Defaults to None.

        Returns:
            Result: An object containing the status code, message, and data from the response.

        Raises:
            OuraPyException: If there is an error making the request or if the response contains bad JSON.
        """
        url = f"{self.url}/{endpoint}"
        headers = {"Authorization": f"Bearer {self._personal_access_token}"}
        log_pre = f"method={method}, url={url}, params={params}"
        log_post = ", ".join(("success={}", "status_code={}", "message={}"))
        try:
            self._logger.debug(msg=log_pre)
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                data=data,
                verify=self._ssl_verify,
            )
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=str(e))
            raise OuraPyException("Error making request") from e
        try:
            data_out = response.json()
        except (ValueError, JSONDecodeError) as e:
            self._logger.error(msg=log_post.format(False, None, e))
            raise OuraPyException("Bad JSON in response") from e
        req_success = 299 >= response.status_code >= 200
        log_line = log_post.format(req_success, response.status_code, response.reason)
        if req_success:
            self._logger.debug(msg=log_line)
            return Result(
                status_code=response.status_code, message=response.reason, data=data_out
            )
        self._logger.error(msg=log_line)
        raise OuraPyException(f"{response.status_code}: {response.reason}")
