from __future__ import annotations

import datetime
import logging
from collections.abc import Callable
from typing import Any, Literal

from oura_py.auth.oauth_manager import OuraOAuth2Client
from oura_py.auth.token_manager import JsonTokenStore, TokenManager, TokenStore
from oura_py.client.request_manager import RequestManager
from oura_py.constants import DOC_ID_ERR_MSG, WebhookDataType
from oura_py.data import models
from oura_py.data.exceptions import OuraPyException
from oura_py.data.response import JSONValue, OuraResponse

ResponseFormat = Literal["raw", "models"]


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
        response_format: ResponseFormat = "raw",
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
            response_format: Whether to return raw API response or data models.
                Usage of "models" requires oura-py[models] to be installed.
        """
        if response_format not in {"raw", "models"}:
            raise ValueError("response_format must be 'raw' or 'models'")

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
        self._response_format = response_format

    def _get_model_classes(self):
        if self._response_format == "raw":
            return None
        try:
            from oura_py.data import models
        except ImportError as exception:
            raise ImportError("""
                "Model responses require optional dependency. Install with `pip install "oura-py[models]"`
            """) from exception
        return models

    def daily_activity(
        self,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> OuraResponse[models.DailyAcitivity]:
        params: dict[str, Any] = {}

        if start_date is not None:
            params["start_date"] = start_date

        if end_date is not None:
            params["end_date"] = end_date

        data, metadata = self._fetch("daily_sleep", params=params)

        return OuraResponse(
            data=data, model_type=models.DailyActivity, metadata=metadata
        )

    def daily_sleep(
        self,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> OuraResponse[models.DailySleep]:
        params: dict[str, Any] = {}

        if start_date is not None:
            params["start_date"] = start_date

        if end_date is not None:
            params["end_date"] = end_date

        data, metadata = self._fetch("daily_sleep", params=params)

        return OuraResponse(data=data, model_type=models.DailySleep, metadata=metadata)

    def get_sleep_summary(
        self,
        start: str | None = None,
        end: str | None = None,
        next_token: str | None = None,
        document_id: str | None = None,
        fields: str | None = None,
        response_format: ResponseFormat | None = None,
    ) -> models.SleepSummary | models.SleepSummaryDatum | JSONValue:
        return self._get_summary_generic(
            summary_endpoint="daily_sleep",
            data_class_name="SleepSummary",
            datum_class_name="SleepSummaryDatum",
            start=start,
            end=end,
            next_token=next_token,
            document_id=document_id,
            fields=fields,
            response_format=response_format,
        )

    def get_readiness_summary(
        self,
        start: str | None = None,
        end: str | None = None,
        next_token: str | None = None,
        document_id: str | None = None,
        fields: str | None = None,
        response_format: ResponseFormat | None = None,
    ) -> models.ReadinessSummary | models.ReadinessSummaryDatum | JSONValue:
        return self._get_summary_generic(
            summary_endpoint="daily_readiness",
            data_class_name="ReadinessSummary",
            datum_class_name="ReadinessSummaryDatum",
            start=start,
            end=end,
            next_token=next_token,
            document_id=document_id,
            fields=fields,
            response_format=response_format,
        )

    def get_activity_summary(
        self,
        start: str | None = None,
        end: str | None = None,
        next_token: str | None = None,
        document_id: str | None = None,
        fields: str | None = None,
        response_format: ResponseFormat | None = None,
    ) -> models.ActivitySummary | models.ActivitySummaryDatum | JSONValue:
        return self._get_summary_generic(
            summary_endpoint="daily_activity",
            data_class_name="ActivitySummary",
            datum_class_name="ActivitySummaryDatum",
            start=start,
            end=end,
            next_token=next_token,
            document_id=document_id,
            fields=fields,
            response_format=response_format,
        )

    def get_heartrate_summary(
        self,
        start_datetime: str | None = None,
        end_datetime: str | None = None,
        next_token: str | None = None,
        latest: bool | None = None,
        fields: str | None = None,
    ) -> models.HeartRateSummary | models.HeartRateDatum | JSONValue:
        params = self._compact_params(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            next_token=next_token,
            latest=latest,
            fields=fields,
        )
        result = self._manager.get("heartrate", params=params)
        if self._response_format == "raw":
            return result.data

        models = self._get_model_classes()
        return models.HeartRateSummary.model_validate(result.data)

    def get_stress_summary(
        self,
        start: str | None = None,
        end: str | None = None,
        next_token: str | None = None,
        document_id: str | None = None,
        fields: str | None = None,
        response_format: ResponseFormat | None = None,
    ) -> models.StressSummary | models.StressDatum | JSONValue:
        return self._get_summary_generic(
            summary_endpoint="daily_stress",
            data_class_name="StressSummary",
            datum_class_name="StressDatum",
            start=start,
            end=end,
            next_token=next_token,
            document_id=document_id,
            fields=fields,
            response_format=response_format,
        )

    def get_resilience_summary(
        self,
        start: str | None = None,
        end: str | None = None,
        next_token: str | None = None,
        document_id: str | None = None,
        fields: str | None = None,
        response_format: ResponseFormat | None = None,
    ) -> models.ResilienceSummary | models.ResilienceDatum | JSONValue:
        return self._get_summary_generic(
            summary_endpoint="daily_resilience",
            data_class_name="ResilienceSummary",
            datum_class_name="ResilienceDatum",
            start=start,
            end=end,
            next_token=next_token,
            document_id=document_id,
            fields=fields,
            response_format=response_format,
        )

    def get_spo2_summary(
        self,
        start: str | None = None,
        end: str | None = None,
        next_token: str | None = None,
        document_id: str | None = None,
        fields: str | None = None,
        response_format: ResponseFormat | None = None,
    ) -> models.Spo2Summary | models.Spo2Datum | JSONValue:
        return self._get_summary_generic(
            summary_endpoint="daily_spo2",
            data_class_name="Spo2Summary",
            datum_class_name="Spo2Datum",
            start=start,
            end=end,
            next_token=next_token,
            document_id=document_id,
            fields=fields,
            response_format=response_format,
        )

    def get_tags_summary(
        self,
        start: str | None = None,
        end: str | None = None,
        next_token: str | None = None,
        document_id: str | None = None,
        fields: str | None = None,
        response_format: ResponseFormat | None = None,
    ) -> models.TagSummary | models.TagDatum | JSONValue:
        return self._get_summary_generic(
            summary_endpoint="enhanced_tag",
            data_class_name="TagSummary",
            datum_class_name="TagDatum",
            start=start,
            end=end,
            next_token=next_token,
            document_id=document_id,
            fields=fields,
            response_format=response_format,
        )

    def get_rest_mode_periods(
        self,
        start: str | None = None,
        end: str | None = None,
        next_token: str | None = None,
        document_id: str | None = None,
        fields: str | None = None,
        response_format: ResponseFormat | None = None,
    ) -> models.RestModePeriodSummary | models.RestModePeriodDatum | JSONValue:
        return self._get_summary_generic(
            summary_endpoint="rest_mode_period",
            data_class_name="RestModePeriodSummary",
            datum_class_name="RestModePeriodDatum",
            start=start,
            end=end,
            next_token=next_token,
            document_id=document_id,
            fields=fields,
            response_format=response_format,
        )

    def get_session_data(
        self,
        start: str | None = None,
        end: str | None = None,
        next_token: str | None = None,
        document_id: str | None = None,
        fields: str | None = None,
        response_format: ResponseFormat | None = None,
    ) -> models.SessionData | models.SessionDatum | JSONValue:
        return self._get_summary_generic(
            summary_endpoint="session",
            data_class_name="SessionData",
            datum_class_name="SessionDatum",
            start=start,
            end=end,
            next_token=next_token,
            document_id=document_id,
            fields=fields,
            response_format=response_format,
        )

    def get_sleep_detail(
        self,
        start: str | None = None,
        end: str | None = None,
        next_token: str | None = None,
        document_id: str | None = None,
        fields: str | None = None,
        response_format: ResponseFormat | None = None,
    ) -> models.SleepDetailData | models.SleepDetailDatum | JSONValue:
        return self._get_summary_generic(
            summary_endpoint="sleep",
            data_class_name="SleepDetailData",
            datum_class_name="SleepDetailDatum",
            start=start,
            end=end,
            next_token=next_token,
            document_id=document_id,
            fields=fields,
            response_format=response_format,
        )

    def get_sleep_times(
        self,
        start: str | None = None,
        end: str | None = None,
        next_token: str | None = None,
        document_id: str | None = None,
        fields: str | None = None,
        response_format: ResponseFormat | None = None,
    ) -> models.SleepTimeData | models.SleepTimeDatum | JSONValue:
        return self._get_summary_generic(
            summary_endpoint="sleep_time",
            data_class_name="SleepTimeData",
            datum_class_name="SleepTimeDatum",
            start=start,
            end=end,
            next_token=next_token,
            document_id=document_id,
            fields=fields,
            response_format=response_format,
        )

    def get_vo2_max(
        self,
        start: str | None = None,
        end: str | None = None,
        next_token: str | None = None,
        document_id: str | None = None,
        fields: str | None = None,
        response_format: ResponseFormat | None = None,
    ) -> models.VO2MaxData | models.VO2MaxDatum | JSONValue:
        return self._get_summary_generic(
            summary_endpoint="vO2_max",
            data_class_name="VO2MaxData",
            datum_class_name="VO2MaxDatum",
            start=start,
            end=end,
            next_token=next_token,
            document_id=document_id,
            fields=fields,
            response_format=response_format,
        )

    def get_workouts(
        self,
        start: str | None = None,
        end: str | None = None,
        next_token: str | None = None,
        document_id: str | None = None,
        fields: str | None = None,
        response_format: ResponseFormat | None = None,
    ) -> models.WorkoutData | models.WorkoutDatum | JSONValue:
        return self._get_summary_generic(
            summary_endpoint="workout",
            data_class_name="WorkoutData",
            datum_class_name="WorkoutDatum",
            start=start,
            end=end,
            next_token=next_token,
            document_id=document_id,
            fields=fields,
            response_format=response_format,
        )

    def get_daily_cardiovascular_age(
        self,
        start: str | None = None,
        end: str | None = None,
        next_token: str | None = None,
        document_id: str | None = None,
        fields: str | None = None,
        response_format: ResponseFormat | None = None,
    ) -> (
        models.DailyCardiovascularAgeData
        | models.DailyCardiovascularAgeDatum
        | JSONValue
    ):
        """Get daily cardiovascular-age records or one record by ID."""
        return self._get_summary_generic(
            summary_endpoint="daily_cardiovascular_age",
            data_class_name="DailyCardiovascularAgeData",
            datum_class_name="DailyCardiovascularAgeDatum",
            start=start,
            end=end,
            next_token=next_token,
            document_id=document_id,
            fields=fields,
            response_format=response_format,
        )

    def get_ring_battery_level(
        self,
        start_datetime: str | None = None,
        end_datetime: str | None = None,
        next_token: str | None = None,
        latest: bool | None = None,
        fields: str | None = None,
    ) -> models.RingBatteryLevelData | JSONValue:
        """Get ring battery-level time-series data."""
        params = self._compact_params(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            next_token=next_token,
            latest=latest,
            fields=fields,
        )
        result = self._manager.get("ring_battery_level", params=params)
        if self._response_format == "raw":
            return result.data

        models = self._get_model_classes()
        return models.RingBatteryLevelData.model_validate(result.data)

    def get_tag(
        self,
        start: str | None = None,
        end: str | None = None,
        next_token: str | None = None,
        document_id: str | None = None,
        fields: str | None = None,
        response_format: ResponseFormat | None = None,
    ) -> models.BasicTagData | models.BasicTagDatum | JSONValue:
        """Get basic tag records or one record by ID."""
        return self._get_summary_generic(
            summary_endpoint="tag",
            data_class_name="BasicTagData",
            datum_class_name="BasicTagDatum",
            start=start,
            end=end,
            next_token=next_token,
            document_id=document_id,
            fields=fields,
            response_format=response_format,
        )

    def get_webhook_subscriptions(
        self,
    ) -> models.WebhookSubscriptions | JSONValue:
        """List the application's webhook subscriptions."""
        result = self._manager.webhook_get("../webhook/subscription")
        if self._response_format == "raw":
            return result.data

        models = self._get_model_classes()
        return models.WebhookSubscriptions.model_validate(result.data)

    def create_webhook_subscription(self, data: dict) -> JSONValue:
        """Create a webhook subscription from an OpenAPI request payload."""
        payload = dict(data)
        if isinstance(payload.get("data_type"), WebhookDataType):
            payload["data_type"] = payload["data_type"].value
        result = self._manager.webhook_post("../webhook/subscription", data=payload)
        return result.data

    def get_webhook_subscription(
        self, subscription_id: str
    ) -> models.WebhookSubscriptionModel | JSONValue:
        """Get one webhook subscription by ID."""
        result = self._manager.webhook_get(f"../webhook/subscription/{subscription_id}")
        if self._response_format == "raw":
            return result.data

        models = self._get_model_classes()
        return models.WebhookSubscriptionModel.model_validate(result.data)

    def update_webhook_subscription(
        self, subscription_id: str, data: dict
    ) -> JSONValue:
        """Update a webhook subscription."""
        result = self._manager.webhook_put(
            f"../webhook/subscription/{subscription_id}", data=data
        )
        return result.data

    def delete_webhook_subscription(self, subscription_id: str) -> JSONValue:
        """Delete a webhook subscription."""
        result = self._manager.webhook_delete(
            f"../webhook/subscription/{subscription_id}"
        )
        return result.data

    def renew_webhook_subscription(self, subscription_id: str) -> JSONValue:
        """Renew a webhook subscription."""
        result = self._manager.webhook_put(
            f"../webhook/subscription/renew/{subscription_id}"
        )
        return result.data

    def get_personal_info(
        self, response_format: ResponseFormat | None = None
    ) -> models.PersonalInfo | JSONValue:
        result = self._manager.get("personal_info")
        response_format = response_format or self._response_format
        if response_format == "raw":
            return result.data

        models = self._get_model_classes()
        return models.PersonalInfo.model_validate(result.data)

    def get_ring_config(
        self,
        document_id: str | None = None,
        next_token: str | None = None,
        fields: str | None = None,
    ) -> models.RingConfig | JSONValue:
        if document_id and next_token:
            raise ValueError(DOC_ID_ERR_MSG)
        endpoint = (
            "ring_configuration"
            if document_id is None
            else f"ring_configuration/{document_id}"
        )
        params = self._compact_params(next_token=next_token, fields=fields)
        result = self._manager.get(endpoint=endpoint, params=params)
        if self._response_format == "raw":
            return result.data

        models = self._get_model_classes()
        return models.RingConfig.model_validate(result.data)

    def _get_raw_collection(
        self,
        endpoint: str,
        start: str | None,
        end: str | None,
        next_token: str | None,
        document_id: str | None,
        fields: str | None,
    ) -> JSONValue:
        if document_id and next_token:
            raise ValueError(DOC_ID_ERR_MSG)
        if document_id:
            result = self._manager.get(f"{endpoint}/{document_id}")
            return result.data
        start_date, end_date = self._prep_dates(start, end)
        params = self._compact_params(
            start_date=start_date,
            end_date=end_date,
            next_token=next_token,
            fields=fields,
        )
        result = self._manager.get(endpoint, params=params)
        return result.data

    def _fetch(  # TODO add kwarg support & date range defaults
        self, endpoint: str, *, params: dict[str, Any] | None = None
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]:

        records: list[dict[str, Any]] = []
        request_params: dict = dict(params or {})
        next_token: str | None = None

        while True:
            if next_token is not None:
                request_params["next_token"] = next_token

            result = self._manager.get(endpoint, params=request_params)
            data = result.data
            records.extend(data.get("data", []))
            next_token = data.get("next_token")

            if next_token is None:
                break

        metadata = {
            "endpoint": endpoint,
            "request_params": params,
        }

        return records, metadata

    def _get_summary_generic(
        self,
        summary_endpoint: str,
        data_class_name: str,
        datum_class_name: str,
        start: str | None = None,
        end: str | None = None,
        next_token: str | None = None,
        document_id: str | None = None,
        fields: str | None = None,
        response_format: ResponseFormat | None = None,
    ) -> JSONValue:
        if document_id and next_token:
            raise ValueError(DOC_ID_ERR_MSG)

        response_format = response_format or self._response_format

        if document_id:
            result = self._manager.get(f"{summary_endpoint}/{document_id}")
            if response_format == "raw":
                return result.data

            models = self._get_model_classes()
            datum_class = getattr(models, datum_class_name)
            return datum_class.model_validate(result.data)

        start_date, end_date = self._prep_dates(start, end)
        params = self._compact_params(
            start_date=start_date,
            end_date=end_date,
            next_token=next_token,
            fields=fields,
        )
        result = self._manager.get(
            f"{summary_endpoint}",
            params=params,
        )

        if response_format == "raw":
            return result.data

        models = self._get_model_classes()
        data_class = getattr(models, data_class_name)
        return data_class.model_validate(result.data)

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

    @staticmethod
    def _compact_params(**params: object) -> dict:
        """Remove unset optional query parameters before sending a request."""
        return {key: value for key, value in params.items() if value is not None}
