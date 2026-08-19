import datetime
import logging
from collections.abc import Callable

from oura_py.auth.oauth_manager import OuraOAuth2Client
from oura_py.auth.token_manager import JsonTokenStore, TokenManager, TokenStore
from oura_py.exceptions import OuraPyException
from oura_py.helpers import RequestManager
from oura_py.models import (
    ActivitySummary,
    ActivitySummaryDatum,
    HeartRateDatum,
    HeartRateSummary,
    PersonalInfo,
    ReadinessSummary,
    ReadinessSummaryDatum,
    ResilienceDatum,
    ResilienceSummary,
    RestModePeriodDatum,
    RestModePeriodSummary,
    RingConfig,
    SessionData,
    SessionDatum,
    SleepDetailData,
    SleepDetailDatum,
    SleepSummary,
    SleepSummaryDatum,
    SleepTimeData,
    SleepTimeDatum,
    Spo2Datum,
    Spo2Summary,
    StressDatum,
    StressSummary,
    TagDatum,
    TagSummary,
    VO2MaxData,
    VO2MaxDatum,
    WorkoutData,
    WorkoutDatum,
)


class OuraClient:
    """Authenticated client for Oura's v2 API.

    A complete OAuth token can be supplied directly through ``token``. When
    it is omitted, the client uses ``token_manager`` or creates a local
    ``TokenManager`` backed by ``token_store``/``token_path``. Browser-based
    authorization is only attempted when ``interactive=True``.
    """

    def __init__(
        self,
        client_id: str,
        token: dict | None = None,
        client_secret: str | None = None,
        token_updater: Callable | None = None,
        token_manager: TokenManager | None = None,
        token_store: TokenStore | None = None,
        interactive: bool = False,
        token_path: str | None = None,
        redirect_uri: str | None = None,
        ssl_verify: bool = True,
        logger: logging.Logger | None = None,
    ):
        """Initialize an authenticated Oura API client.

        Args:
            client_id: OAuth application client ID.
            token: Complete OAuth token response. If omitted, a token is
                resolved through ``token_manager`` or the configured store.
            client_secret: OAuth application client secret.
            token_updater: Optional callback for persisting refreshed tokens.
            token_manager: Custom token acquisition and refresh handler.
            token_store: Token store used by the default token manager.
            interactive: Whether missing credentials may start browser auth.
            token_path: Local JSON token path used by the default store.
            redirect_uri: Registered OAuth callback URL.
            ssl_verify: Whether to verify SSL certificates.
            logger: Optional logger used by the client and request manager.
        """
        self._logger = logger or logging.getLogger(__name__)
        if token is None:
            if token_manager is None:
                if not client_secret:
                    raise ValueError("client_secret is required when token is omitted")
                store = token_store or JsonTokenStore(token_path or ".oura_tokens.json")
                token_manager = TokenManager(
                    OuraOAuth2Client(client_id, client_secret),
                    store=store,
                    redirect_uri=redirect_uri,
                )
            token = token_manager.get_valid_token(interactive=interactive)
        self._manager = RequestManager(
            client_id=client_id,
            token=token,
            client_secret=client_secret,
            token_updater=token_updater,
            ssl_verify=ssl_verify,
            logger=self._logger,
        )

    def get_sleep_summary(
        self,
        start: str | None = None,
        end: str | None = None,
        next_token: str | None = None,
    ) -> SleepSummary | SleepSummaryDatum:
        return self._get_summary_generic(
            summary_endpoint="daily_sleep",
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
            summary_endpoint="daily_readiness",
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
            summary_endpoint="daily_activity",
            data_class=ActivitySummary,
            data_class_datum=ActivitySummaryDatum,
            start=start,
            end=end,
            next_token=next_token,
        )

    def get_heartrate_summary(
        self,
        start: str | None = None,
        end: str | None = None,
        next_token: str | None = None,
    ) -> HeartRateSummary | HeartRateDatum:
        return self._get_summary_generic(
            summary_endpoint="heartrate",
            data_class=HeartRateSummary,
            data_class_datum=HeartRateDatum,
            start=start,
            end=end,
            next_token=next_token,
        )

    def get_stress_summary(
        self,
        start: str | None = None,
        end: str | None = None,
        next_token: str | None = None,
    ) -> StressSummary | StressDatum:
        return self._get_summary_generic(
            summary_endpoint="daily_stress",
            data_class=StressSummary,
            data_class_datum=StressDatum,
            start=start,
            end=end,
            next_token=next_token,
        )

    def get_resilience_summary(
        self,
        start: str | None = None,
        end: str | None = None,
        next_token: str | None = None,
    ) -> ResilienceSummary | ResilienceDatum:
        return self._get_summary_generic(
            summary_endpoint="daily_resilience",
            data_class=ResilienceSummary,
            data_class_datum=ResilienceDatum,
            start=start,
            end=end,
            next_token=next_token,
        )

    def get_spo2_summary(
        self,
        start: str | None = None,
        end: str | None = None,
        next_token: str | None = None,
    ) -> Spo2Summary | Spo2Datum:
        return self._get_summary_generic(
            summary_endpoint="daily_spo2",
            data_class=Spo2Summary,
            data_class_datum=Spo2Datum,
            start=start,
            end=end,
            next_token=next_token,
        )

    def get_tags_summary(
        self,
        start: str | None = None,
        end: str | None = None,
        next_token: str | None = None,
    ) -> TagSummary | TagDatum:
        return self._get_summary_generic(
            summary_endpoint="enhanced_tag",
            data_class=TagSummary,
            data_class_datum=TagDatum,
            start=start,
            end=end,
            next_token=next_token,
        )

    def get_rest_mode_periods(
        self,
        start: str | None = None,
        end: str | None = None,
        next_token: str | None = None,
    ) -> RestModePeriodSummary | RestModePeriodDatum:
        return self._get_summary_generic(
            summary_endpoint="rest_mode_period",
            data_class=RestModePeriodSummary,
            data_class_datum=RestModePeriodDatum,
            start=start,
            end=end,
            next_token=next_token,
        )

    def get_session_data(
        self,
        start: str | None = None,
        end: str | None = None,
        next_token: str | None = None,
    ) -> SessionData | SessionDatum:
        return self._get_summary_generic(
            summary_endpoint="session",
            data_class=SessionData,
            data_class_datum=SessionDatum,
            start=start,
            end=end,
            next_token=next_token,
        )

    def get_sleep_detail(
        self,
        start: str | None = None,
        end: str | None = None,
        next_token: str | None = None,
    ) -> SleepDetailData | SleepDetailDatum:
        return self._get_summary_generic(
            summary_endpoint="sleep",
            data_class=SleepDetailData,
            data_class_datum=SleepDetailDatum,
            start=start,
            end=end,
            next_token=next_token,
        )

    def get_sleep_times(
        self,
        start: str | None = None,
        end: str | None = None,
        next_token: str | None = None,
    ) -> SleepTimeData | SleepTimeDatum:
        return self._get_summary_generic(
            summary_endpoint="sleep_time",
            data_class=SleepTimeData,
            data_class_datum=SleepTimeDatum,
            start=start,
            end=end,
            next_token=next_token,
        )

    def get_vo2_max(
        self,
        start: str | None = None,
        end: str | None = None,
        next_token: str | None = None,
    ) -> VO2MaxData | VO2MaxDatum:
        return self._get_summary_generic(
            summary_endpoint="vO2_max",
            data_class=VO2MaxData,
            data_class_datum=VO2MaxDatum,
            start=start,
            end=end,
            next_token=next_token,
        )

    def get_workouts(
        self,
        start: str | None = None,
        end: str | None = None,
        next_token: str | None = None,
    ) -> WorkoutData | WorkoutDatum:
        return self._get_summary_generic(
            summary_endpoint="workout",
            data_class=WorkoutData,
            data_class_datum=WorkoutDatum,
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
        summary_endpoint: str,
        data_class: type,
        data_class_datum: type,
        start: str | None = None,
        end: str | None = None,
        next_token: str | None = None,
    ):
        if next_token:
            self._logger.debug(msg=f"next_token={next_token}")
            result = self._manager.get(f"{summary_endpoint}/{next_token}")
            data = data_class_datum(**result.data)
            return data
        start_date, end_date = self._prep_dates(start, end)
        result = self._manager.get(
            f"{summary_endpoint}",
            params={"start_date": start_date, "end_date": end_date},
        )
        data = data_class(**result.data)
        return data

    def _prep_dates(
        self, start_date: str | None = None, end_date: str | None = None
    ) -> tuple[str, str]:
        end = (
            datetime.date.fromisoformat(end_date)
            if end_date
            else datetime.datetime.now(tz=datetime.UTC).date()
        )
        start = (
            datetime.date.fromisoformat(start_date)
            if start_date
            else end - datetime.timedelta(days=1)
        )
        if start > end:
            log_msg = f"Start date must be before end date. Provided start: {start_date}, end: {end_date}"
            self._logger.error(msg=log_msg)
            raise OuraPyException("Start date must be before end date.")
        return str(start), str(end)
