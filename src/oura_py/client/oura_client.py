from __future__ import annotations

import datetime as dt
from collections.abc import Callable
from datetime import timedelta
from typing import Any

from oura_py.client.request_manager import RequestManager
from oura_py.constants import (
    DOC_ID_ERR_MSG,
    WEBHOOK_DATA_TYPES,
    WEBHOOK_PATH,
    WebhookDataType,
)
from oura_py.data import models
from oura_py.data.response import OuraResponse


class OuraClient:
    """Authenticated client for Oura's v2 API.

    The consuming application owns OAuth authorization and token persistence.
    Supply a complete OAuth token; ``token_updater`` is called by the request
    layer when a refreshed token is obtained.
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str | None = None,
        token: dict | None = None,
        token_updater: Callable | None = None,
        ssl_verify: bool = True,
    ):
        """
        Initialize an authenticated Oura API client.
        """

        if token is None:
            raise ValueError("token is required")

        self._manager = RequestManager(
            client_id=client_id,
            client_secret=client_secret,
            token=token,
            token_updater=token_updater,
            ssl_verify=ssl_verify,
        )
        self._client_id = client_id
        self._client_secret = client_secret

    def daily_activity(self, **kwargs) -> OuraResponse[models.DailyActivity]:
        data, metadata = self._fetch("daily_activity", **kwargs)
        return OuraResponse(
            data=data, model_type=models.DailyActivity, metadata=metadata
        )

    def daily_cardiovascular_age(
        self, **kwargs
    ) -> OuraResponse[models.DailyCardiovascularAge]:
        data, metadata = self._fetch("daily_cardiovascular_age", **kwargs)
        return OuraResponse(
            data=data, model_type=models.DailyCardiovascularAge, metadata=metadata
        )

    def daily_readiness(self, **kwargs) -> OuraResponse[models.DailyReadiness]:
        data, metadata = self._fetch("daily_readiness", **kwargs)
        return OuraResponse(
            data=data, model_type=models.DailyReadiness, metadata=metadata
        )

    def daily_resilience(self, **kwargs) -> OuraResponse[models.DailyResilience]:
        data, metadata = self._fetch("daily_resilience", **kwargs)
        return OuraResponse(
            data=data, model_type=models.DailyResilience, metadata=metadata
        )

    def daily_sleep(self, **kwargs) -> OuraResponse[models.DailySleep]:
        data, metadata = self._fetch("daily_sleep", **kwargs)
        return OuraResponse(data=data, model_type=models.DailySleep, metadata=metadata)

    def daily_spo2(self, **kwargs) -> OuraResponse[models.DailySpo2]:
        data, metadata = self._fetch("daily_spo2", **kwargs)
        return OuraResponse(data=data, model_type=models.DailySpo2, metadata=metadata)

    def daily_stress(self, **kwargs) -> OuraResponse[models.DailyStress]:
        data, metadata = self._fetch("daily_stress", **kwargs)
        return OuraResponse(data=data, model_type=models.DailyStress, metadata=metadata)

    def enhanced_tag(self, **kwargs) -> OuraResponse[models.EnhancedTag]:
        data, metadata = self._fetch("enhanced_tag", **kwargs)
        return OuraResponse(data=data, model_type=models.EnhancedTag, metadata=metadata)

    def heartrate(self, **kwargs) -> OuraResponse[models.Heartrate]:
        data, metadata = self._fetch("heartrate", **kwargs)
        return OuraResponse(data=data, model_type=models.Heartrate, metadata=metadata)

    def personal_info(self, **kwargs) -> OuraResponse[models.PersonalInfo]:
        data, metadata = self._fetch_direct("personal_info", **kwargs)
        return OuraResponse(
            data=data, model_type=models.PersonalInfo, metadata=metadata
        )

    def rest_mode_periods(self, **kwargs) -> OuraResponse[models.RestModePeriod]:
        data, metadata = self._fetch("rest_mode_period", **kwargs)
        return OuraResponse(
            data=data, model_type=models.RestModePeriod, metadata=metadata
        )

    def ring_configuration(self, **kwargs) -> OuraResponse[models.RingConfiguration]:
        data, metadata = self._fetch("ring_configuration", **kwargs)
        return OuraResponse(
            data=data, model_type=models.RingConfiguration, metadata=metadata
        )

    def session(self, **kwargs) -> OuraResponse[models.Session]:
        data, metadata = self._fetch("session", **kwargs)
        return OuraResponse(data=data, model_type=models.Session, metadata=metadata)

    def sleep(self, **kwargs) -> OuraResponse[models.Sleep]:
        data, metadata = self._fetch("sleep", **kwargs)
        return OuraResponse(data=data, model_type=models.Sleep, metadata=metadata)

    def sleep_time(self, **kwargs) -> OuraResponse[models.SleepTime]:
        data, metadata = self._fetch("sleep_time", **kwargs)
        return OuraResponse(data=data, model_type=models.SleepTime, metadata=metadata)

    def vo2_max(self, **kwargs) -> OuraResponse[models.VO2Max]:
        data, metadata = self._fetch("vo2_max", **kwargs)
        return OuraResponse(data=data, model_type=models.VO2Max, metadata=metadata)

    def workout(self, **kwargs) -> OuraResponse[models.Workout]:
        data, metadata = self._fetch("workout", **kwargs)
        return OuraResponse(data=data, model_type=models.Workout, metadata=metadata)

    def ring_battery_level(self, **kwargs) -> OuraResponse[models.RingBatteryLevel]:
        data, metadata = self._fetch("ring_battery_level", **kwargs)
        return OuraResponse(
            data=data, model_type=models.RingBatteryLevel, metadata=metadata
        )

    def list_webhook_subscriptions(
        self,
    ) -> OuraResponse[models.WebhookSubscription]:
        """List the application's webhook subscriptions."""
        result = self._manager.get(
            endpoint=WEBHOOK_PATH, headers=self._webhook_headers()
        )
        return OuraResponse(
            data=result.data.get("data", []),
            model_type=models.WebhookSubscription,
            metadata={"endpoint": WEBHOOK_PATH},
        )

    def get_webhook_subscription(
        self, subscription_id: str
    ) -> OuraResponse[models.WebhookSubscription]:
        """Get one webhook subscription by ID."""
        result = self._manager.get(
            f"{WEBHOOK_PATH}/{subscription_id}", headers=self._webhook_headers()
        )
        return OuraResponse(
            data=result.data,
            model_type=models.WebhookSubscription,
            metadata={"endpoint": f"{WEBHOOK_PATH}/{subscription_id}"},
        )

    def create_webhook_subscription(
        self, data: dict[str, str]
    ) -> OuraResponse[models.WebhookSubscription]:
        """Create a webhook subscription from an OpenAPI request payload."""
        payload = dict(data)
        data_type = payload.get("data_type")

        if isinstance(data_type, WebhookDataType):
            data_type = data_type.value
            payload["data_type"] = data_type
        if data_type not in WEBHOOK_DATA_TYPES:
            raise ValueError(f"Invalid webhook data type: {data_type!r}")
        result = self._manager.post(
            endpoint=WEBHOOK_PATH, data=payload, headers=self._webhook_headers()
        )
        return OuraResponse(
            data=result.data,
            model_type=models.WebhookSubscription,
            metadata={"endpoint": WEBHOOK_PATH, "data": payload},
        )

    def update_webhook_subscription(
        self, subscription_id: str, data: dict[str, str]
    ) -> OuraResponse[models.WebhookSubscription]:
        """Update a webhook subscription."""
        result = self._manager.put(
            f"{WEBHOOK_PATH}/{subscription_id}",
            data=data,
            headers=self._webhook_headers(),
        )
        return OuraResponse(
            data=result.data,
            model_type=models.WebhookSubscription,
            metadata={"endpoint": f"{WEBHOOK_PATH}/{subscription_id}", "data": data},
        )

    def renew_webhook_subscription(
        self, subscription_id: str
    ) -> OuraResponse[models.WebhookSubscription]:
        """Renew a webhook subscription."""
        result = self._manager.put(
            endpoint=f"{WEBHOOK_PATH}/renew/{subscription_id}",
            headers=self._webhook_headers(),
        )
        return OuraResponse(
            data=result.data,
            model_type=models.WebhookSubscription,
            metadata={"endpoint": f"{WEBHOOK_PATH}/renew/{subscription_id}"},
        )

    def delete_webhook_subscription(self, subscription_id: str) -> None:
        """Delete a webhook subscription."""
        self._manager.delete(
            endpoint=f"{WEBHOOK_PATH}/{subscription_id}",
            headers=self._webhook_headers(),
        )

    def _fetch(
        self, endpoint: str, **kwargs: Any
    ) -> tuple[list[dict[str, Any]] | dict[str, Any], dict[str, Any]]:
        document_id = kwargs.pop("document_id", None)
        if document_id is not None:
            if kwargs.get("next_token") is not None:
                raise ValueError(DOC_ID_ERR_MSG)
            kwargs.pop("start_date", None)
            kwargs.pop("end_date", None)
            return self._fetch_direct(f"{endpoint}/{document_id}", **kwargs)

        kwargs = self._set_default_dates(endpoint, **kwargs)
        params = self._compact_params(**kwargs)
        request_params = params.copy()

        records: list[dict[str, Any]] = []
        next_token: str | None = None

        while True:
            if next_token is not None:
                params["next_token"] = next_token

            result = self._manager.get(endpoint, params=params)
            data = result.data
            records.extend(data.get("data", []))
            next_token = data.get("next_token")

            if next_token is None:
                break

        metadata = {
            "endpoint": endpoint,
            "params": request_params,
        }

        return records, metadata

    def _fetch_direct(
        self, endpoint: str, **kwargs: Any
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        params = self._compact_params(**kwargs)
        result = self._manager.get(endpoint, params=params)
        return result.data, {"endpoint": endpoint, "params": params}

    def _webhook_headers(self) -> dict[str, str]:
        if not self._client_secret:
            raise ValueError("client_secret is required for webhook operations")
        return {
            "x-client-id": self._client_id,
            "x-client-secret": self._client_secret,
        }

    @staticmethod
    def _set_default_dates(endpoint: str, **kwargs: Any) -> dict[str, Any]:
        if endpoint in {"heartrate", "ring_battery_level"}:
            return OuraClient._set_default_datetimes(**kwargs)

        end_date = kwargs.get("end_date")
        start_date = kwargs.get("start_date")

        if end_date is None:
            end_date = dt.datetime.now(dt.UTC).date().isoformat()

        if start_date is None:
            start_date = (
                dt.date.fromisoformat(end_date) - timedelta(days=1)
            ).isoformat()

        kwargs["start_date"] = start_date
        kwargs["end_date"] = end_date

        return kwargs

    @staticmethod
    def _set_default_datetimes(**kwargs: Any) -> dict[str, Any]:
        kwargs.pop("start_date", None)
        kwargs.pop("end_date", None)

        end_datetime = kwargs.get("end_datetime")
        if end_datetime is None:
            end_datetime = dt.datetime.now(dt.UTC)
        elif isinstance(end_datetime, str):
            end_datetime = dt.datetime.fromisoformat(end_datetime)

        start_datetime = kwargs.get("start_datetime")
        if start_datetime is None:
            start_datetime = end_datetime - timedelta(days=1)

        kwargs["start_datetime"] = OuraClient._format_datetime(start_datetime)
        kwargs["end_datetime"] = OuraClient._format_datetime(end_datetime)
        return kwargs

    @staticmethod
    def _format_datetime(value: dt.datetime | str) -> str:
        if isinstance(value, dt.datetime):
            return value.isoformat().replace("+00:00", "Z")
        return value

    @staticmethod
    def _compact_params(**params: Any) -> dict[str, Any]:
        """Remove unset optional query parameters before sending a request."""
        return {key: value for key, value in params.items() if value is not None}
