from unittest.mock import Mock

from oura_py.models import Result
from oura_py.oura_client import OuraClient


def make_client() -> OuraClient:
    return OuraClient(
        client_id="client_id",
        token={"access_token": "token", "token_type": "Bearer"},
    )


def test_daily_cardiovascular_age_uses_query_pagination():
    client = make_client()
    client._manager.get = Mock(
        return_value=Result(status_code=200, message="OK", data={})
    )

    client.get_daily_cardiovascular_age(
        start="2025-01-01",
        end="2025-01-02",
        next_token="page-2",
        fields="pulse_wave_velocity",
    )

    client._manager.get.assert_called_once_with(
        "daily_cardiovascular_age",
        params={
            "start_date": "2025-01-01",
            "end_date": "2025-01-02",
            "next_token": "page-2",
            "fields": "pulse_wave_velocity",
        },
    )


def test_existing_route_uses_document_id_as_path():
    client = make_client()
    client._manager.get = Mock(
        return_value=Result(status_code=200, message="OK", data={})
    )

    try:
        client.get_daily_cardiovascular_age(document_id="record-1")
    except TypeError:
        # The raw endpoint intentionally does not require a model yet.
        raise AssertionError("raw document route should not be model validated")

    client._manager.get.assert_called_once_with("daily_cardiovascular_age/record-1")


def test_heartrate_uses_datetime_parameters():
    client = make_client()
    client._manager.get = Mock(
        return_value=Result(
            status_code=200,
            message="OK",
            data={"next_token": None, "data": []},
        )
    )

    client.get_heartrate_summary(
        start_datetime="2025-01-01T00:00:00Z",
        end_datetime="2025-01-02T00:00:00Z",
        latest=True,
        fields="bpm,timestamp",
    )

    client._manager.get.assert_called_once_with(
        "heartrate",
        params={
            "start_datetime": "2025-01-01T00:00:00Z",
            "end_datetime": "2025-01-02T00:00:00Z",
            "latest": True,
            "fields": "bpm,timestamp",
        },
    )


def test_webhook_routes_use_version_root():
    client = make_client()
    client._manager.get = Mock(
        return_value=Result(status_code=200, message="OK", data={})
    )
    client._manager.post = Mock(
        return_value=Result(status_code=201, message="Created", data={})
    )
    client._manager.put = Mock(
        return_value=Result(status_code=200, message="OK", data={})
    )
    client._manager.delete = Mock(
        return_value=Result(status_code=204, message="No Content", data={})
    )

    client.get_webhook_subscriptions()
    client.create_webhook_subscription({"callback_url": "https://example.test"})
    client.get_webhook_subscription("sub-1")
    client.update_webhook_subscription(
        "sub-1", {"callback_url": "https://example.test"}
    )
    client.renew_webhook_subscription("sub-1")
    client.delete_webhook_subscription("sub-1")

    client._manager.get.assert_any_call("../webhook/subscription")
    client._manager.post.assert_called_once_with(
        "../webhook/subscription", data={"callback_url": "https://example.test"}
    )
    client._manager.put.assert_any_call(
        "../webhook/subscription/sub-1",
        data={"callback_url": "https://example.test"},
    )
    client._manager.put.assert_any_call("../webhook/subscription/renew/sub-1")
    client._manager.delete.assert_called_once_with("../webhook/subscription/sub-1")
