import requests
from urllib3.exceptions import InsecureRequestWarning
from typing import Dict
from json import JSONDecodeError
from datetime import date, timedelta
import logging
from .auth import PersonalTokenRequestHandler
from .exceptions import OuraPyException
from .models import (
    Result,
    PersonalInfo,
    RingConfig,
    SleepSummary,
    SleepSummaryDatum,
    ReadinessSummary,
    ReadinessSummaryDatum,
    ActivitySummary,
    ActivitySummaryDatum,
)


class OuraClient:
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
    ) -> SleepSummary | SleepSummaryDatum:
        return self._get_summary_generic(
            summary_type="sleep",
            data_class=SleepSummary,
            data_class_datum=SleepSummaryDatum,
            start=start,
            end=end,
            next_token=next_token,
        )

    def get_readiness_summary(
        self,
        start: str | None = None,
        end: str | None = None,
        next_token: str | None = None,
    ) -> ReadinessSummary | ReadinessSummaryDatum:
        return self._get_summary_generic(
            summary_type="readiness",
            data_class=ReadinessSummary,
            data_class_datum=ReadinessSummaryDatum,
            start=start,
            end=end,
            next_token=next_token,
        )

    def get_activity_summary(
        self,
        start: str | None = None,
        end: str | None = None,
        next_token: str | None = None,
    ) -> ActivitySummary | ActivitySummaryDatum:
        return self._get_summary_generic(
            summary_type="activity",
            data_class=ActivitySummary,
            data_class_datum=ActivitySummaryDatum,
            start=start,
            end=end,
            next_token=next_token,
        )

    def _get_summary_generic(
        self,
        summary_type: str,
        data_class: type,
        data_class_datum: type,
        start: str | None = None,
        end: str | None = None,
        next_token: str | None = None,
    ):
        if next_token:
            self._logger.debug(msg=f"next_token={next_token}")
            result = self.get(f"daily_{summary_type}/{next_token}")
            data = data_class_datum(**result.data)
            return data
        start_date, end_date = self._prep_dates(start, end)
        result = self.get(
            f"daily_{summary_type}",
            params={"start_date": start_date, "end_date": end_date},
        )
        data = data_class(**result.data)
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

    def _prep_dates(
        self, start_date: str | None = None, end_date: str | None = None
    ) -> tuple[str, str]:
        end = date.fromisoformat(end_date) if end_date else date.today()
        start = (
            date.fromisoformat(start_date) if start_date else end - timedelta(days=1)
        )
        if start > end:
            log_msg = f"Start date must be before end date. Provided start: {start_date}, end: {end_date}"
            self._logger.error(msg=log_msg)
            raise OuraPyException("Start date must be before end date.")
        return str(start), str(end)

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
