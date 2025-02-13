import requests
from urllib3.exceptions import InsecureRequestWarning
from typing import Dict
from json import JSONDecodeError
import logging
from .auth import PersonalTokenRequestHandler
from .exceptions import OuraPyException
from .models import Result, PersonalInfo


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

    def get_personal_info(self) -> PersonalInfo:
        result = self.get("personal_info")
        data = PersonalInfo(**result.data)
        print(data)

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
        log_post = ", ".join((log_pre, "success={}, status_code={}, message={}"))
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

    def get_daily_activity(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        document_id: str | None = None,
    ):
        if document_id:
            url = "".join([self.URL_BASE, "daily_activity/", document_id])
            return self.client_request(url)
        else:
            url = "".join([self.URL_BASE, "daily_activity"])
            params = self.build_start_end_params(start_date, end_date)
            return self.client_request(url, params)

    def get_daily_readiness(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        document_id: str | None = None,
    ):
        if document_id:
            url = "".join([self.URL_BASE, "daily_readiness/", document_id])
            return self.client_request(url)
        else:
            url = "".join([self.URL_BASE, "daily_readiness"])
            params = self.build_start_end_params(start_date, end_date)
            return self.client_request(url, params)

    def get_daily_sleep(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        document_id: str | None = None,
    ):
        if document_id:
            url = "".join([self.URL_BASE, "daily_sleep/", document_id])
            return self.client_request(url)
        else:
            url = "".join([self.URL_BASE, "daily_sleep"])
            params = self.build_start_end_params(start_date, end_date)
            return self.client_request(url, params)

    def get_daily_resilience(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        document_id: str | None = None,
    ):
        if document_id:
            url = "".join([self.URL_BASE, "daily_resilience/", document_id])
            return self.client_request(url)
        else:
            url = "".join([self.URL_BASE, "daily_resilience"])
            params = self.build_start_end_params(start_date, end_date)
            return self.client_request(url, params)

    def get_daily_spo2(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        document_id: str | None = None,
    ):
        if document_id:
            url = "".join([self.URL_BASE, "daily_spo2/", document_id])
            return self.client_request(url)
        else:
            url = "".join([self.URL_BASE, "daily_spo2"])
            params = self.build_start_end_params(start_date, end_date)
            return self.client_request(url, params)

    def get_daily_stress(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        document_id: str | None = None,
    ):
        if document_id:
            url = "".join([self.URL_BASE, "daily_stress/", document_id])
            return self.client_request(url)
        else:
            url = "".join([self.URL_BASE, "daily_stress"])
            params = self.build_start_end_params(start_date, end_date)
            return self.client_request(url, params)

    def get_enhanced_tags(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        document_id: str | None = None,
    ):
        if document_id:
            url = "".join([self.URL_BASE, "enhanced_tag/", document_id])
            return self.client_request(url)
        else:
            url = "".join([self.URL_BASE, "enhanced_tag"])
            params = self.build_start_end_params(start_date, end_date)
            return self.client_request(url, params)

    def get_heart_rate(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        document_id: str | None = None,
    ):
        if document_id:
            url = "".join([self.URL_BASE, "heartrate/", document_id])
            return self.client_request(url)
        else:
            url = "".join([self.URL_BASE, "heartrate"])
            params = self.build_start_end_params(start_date, end_date)
            return self.client_request(url, params)

    def get_rest_mode_periods(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        document_id: str | None = None,
    ):
        if document_id:
            url = "".join([self.URL_BASE, "rest_mode_period/", document_id])
            return self.client_request(url)
        else:
            url = "".join([self.URL_BASE, "rest_mode_period"])
            params = self.build_start_end_params(start_date, end_date)
            return self.client_request(url, params)

    def get_sessions(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        document_id: str | None = None,
    ):
        if document_id:
            url = "".join([self.URL_BASE, "session/", document_id])
            return self.client_request(url)
        else:
            url = "".join([self.URL_BASE, "session"])
            params = self.build_start_end_params(start_date, end_date)
            return self.client_request(url, params)

    def get_sleep_detail(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        document_id: str | None = None,
    ):
        if document_id:
            url = "".join([self.URL_BASE, "sleep/", document_id])
            return self.client_request(url)
        else:
            url = "".join([self.URL_BASE, "sleep"])
            params = self.build_start_end_params(start_date, end_date)
            return self.client_request(url, params)

    def get_bedtimes(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        document_id: str | None = None,
    ):
        if document_id:
            url = "".join([self.URL_BASE, "sleep_time/", document_id])
            return self.client_request(url)
        else:
            url = "".join([self.URL_BASE, "sleep_time"])
            params = self.build_start_end_params(start_date, end_date)
            print(url)
            print(params)
            return self.client_request(url, params)

    def get_vo2_max(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        document_id: str | None = None,
    ):
        if document_id:
            url = "".join([self.URL_BASE, "vO2_max/", document_id])
            return self.client_request(url)
        else:
            url = "".join([self.URL_BASE, "vO2_max"])
            params = self.build_start_end_params(start_date, end_date)
            return self.client_request(url, params)

    def get_workouts(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        document_id: str | None = None,
    ):
        if document_id:
            url = "".join([self.URL_BASE, "workout/", document_id])
            return self.client_request(url)
        else:
            url = "".join([self.URL_BASE, "workout"])
            params = self.build_start_end_params(start_date, end_date)
            return self.client_request(url, params)

    def get_ring_config(self):
        url = "".join([self.URL_BASE, "ring_configuration"])
        return self.client_request(url)

    # def get_personal_info(self):
    #     url = "".join([self.URL_BASE, "personal_info"])
    #     return self.client_request(url)

    def client_request(self, url, params: dict = {}):
        response = self.handler.make_request(url, params=params)
        return response.text

    def build_start_end_params(self, start_date: str, end_date: str):
        params = {}

        if start_date is not None:
            if not isinstance(start_date, str):
                raise ValueError("start_date must be a string")
            params["start_date"] = start_date

        if end_date is not None:
            if not isinstance(end_date, str):
                raise ValueError("end_date must be a string")
            params["end_date"] = end_date

        return params
