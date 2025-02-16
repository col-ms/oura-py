from datetime import date, timedelta
import logging
from .helpers import RequestManager
from .exceptions import OuraPyException
from .models import (
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
        self._ssl_verify = ssl_verify
        self._logger = logger or logging.getLogger(__name__)
        self._manager = RequestManager(
            personal_access_token=self._personal_access_token,
            url=self.url,
            ssl_verify=self._ssl_verify,
            logger=self._logger,
        )

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

    def get_personal_info(self) -> PersonalInfo:
        result = self._manager.get("personal_info")
        data = PersonalInfo(**result.data)
        return data

    def get_ring_config(self, document_id: str | None = None) -> RingConfig:
        endpoint = (
            "ring_configuration"
            if document_id is None
            else f"ring_configuration/{document_id}"
        )
        result = self._manager.get(endpoint=endpoint)
        data = RingConfig(**result.data)
        return data

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
            result = self._manager.get(f"daily_{summary_type}/{next_token}")
            data = data_class_datum(**result.data)
            return data
        start_date, end_date = self._prep_dates(start, end)
        result = self._manager.get(
            f"daily_{summary_type}",
            params={"start_date": start_date, "end_date": end_date},
        )
        data = data_class(**result.data)
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
