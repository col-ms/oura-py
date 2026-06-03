import requests
import logging
from typing import Dict, Optional
from json import JSONDecodeError
from urllib3.exceptions import InsecureRequestWarning
from oura_py.exceptions import OuraPyException
from oura_py.models import Result
from oura_py.auth.oauth_manager import OuraOAuth2Client
from oura_py.auth.token_manager import TokenManager


class RequestManager:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        hostname: str,
        ver: str,
        path: str,
        ssl_verify: bool = True,
        logger: logging.Logger = None,
        personal_access_token: Optional[str] = None,
    ) -> None:
        """HTTP request manager.

        Args:
            personal_access_token (str): The personal access token for authenticating with the Oura API.
            hostname (str): The API hostname.
            ver (str): The API version.
            path (str): The API path.
            ssl_verify (bool, optional): Whether to verify SSL certificates. Defaults to True.
            logger (logging.Logger, optional): Logger instance for logging. Defaults to None.
        """
        self._url = f"https://{hostname}/{ver}/{path}"
        self._personal_access_token = personal_access_token
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri
        self._ssl_verify = ssl_verify
        self._logger = logger or logging.getLogger(__name__)
        if not ssl_verify:
            requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

        auth_client = OuraOAuth2Client(client_id, client_secret, redirect_uri)
        self.token_manager = TokenManager(auth_client)

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

    def _get_headers(self) -> dict:
        return {"Authorization": f"Bearer {self.token_manager.get_valid_token()}"}

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
        url = f"{self._url}/{endpoint}"
        log_pre = f"method={method}, url={url}, params={params}"
        log_post = ", ".join(("success={}", "status_code={}", "message={}"))
        try:
            self._logger.debug(msg=log_pre)
            response = requests.request(
                method=method,
                url=url,
                headers=self._get_headers(),
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
