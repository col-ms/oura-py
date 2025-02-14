import requests
from urllib3.exceptions import InsecureRequestWarning
from typing import Dict
from json import JSONDecodeError
import logging
from .auth import PersonalTokenRequestHandler
from .exceptions import OuraPyException
from .models import Result, PersonalInfo, RingConfig, SleepSummary


class OuraClient:
    URL_BASE = "https://api.ouraring.com/v2/usercollection/"

    def __init__(
        self,
        personal_access_token: str,
        hostname: str = "api.ouraring.com",
        ver: str = "v2",
        ssl_verify: bool = True,
        logger: logging.Logger = None,
    ):
        """Initializes the OuraClient instance.

        Args:
            personal_access_token (str): The personal access token for authenticating with the Oura API.
            hostname (str, optional): The API hostname. Defaults to "api.ouraring.com".
            ver (str, optional): The API version. Defaults to "v2".
            ssl_verify (bool, optional): Whether to verify SSL certificates. Defaults to True.
            logger (logging.Logger, optional): Logger instance for logging. Defaults to None.
        """
        self.url = f"https://{hostname}/{ver}/usercollection"
        self._personal_access_token = personal_access_token
        self._handler = PersonalTokenRequestHandler(personal_access_token)
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

    def get_sleep_summary(
        self,
        start: str | None = None,
        end: str | None = None,
        next_token: str | None = None,
    ) -> SleepSummary:
        if next_token is not None:
            self._logger.debug(msg=f"next_token={next_token}")
            endpoint = f"daily_sleep/{next_token}"
            result = self.get(endpoint=endpoint)
            data = SleepSummary(**result.data)
            return data
        if isinstance(start, str) or isinstance(end, str):
            params = {}
            if start:
                params["start_date"] = start
            if end:
                params["end_date"] = end
            result = self.get("daily_sleep", params=params)
            data = SleepSummary(**result.data)
            return data
        result = self.get("daily_sleep")
        data = SleepSummary(**result.data)
        return data

    def get_personal_info(self) -> PersonalInfo:
        result = self.get("personal_info")
        data = PersonalInfo(**result.data)
        return data

    def get_ring_config(self, document_id: str | None = None) -> RingConfig:
        endpoint = (
            "ring_configuration"
            if document_id is None
            else f"ring_configuration/{document_id}"
        )
        result = self.get(endpoint=endpoint)
        data = RingConfig(**result.data)
        return data

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
