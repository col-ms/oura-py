from unittest.mock import Mock

import pytest

from oura_py.client.oura_client import OuraClient
from oura_py.data.response import Result


def make_client() -> OuraClient:
    return OuraClient(
        client_id="client_id",
        client_secret="client_secret",
        token={"access_token": "token", "token_type": "Bearer"},
    )


def test_daily_cardiovascular_age_uses_query_pagination():
    client = make_client()
    client._manager.get = Mock(
        return_value=Result(status_code=200, message="OK", data={})
    )

    client.daily_cardiovascular_age(
        start_date="2025-01-01",
        end_date="2025-01-02",
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


def test_daily_cardiovascular_age_passes_document_id_as_path_parameter():
    client = make_client()
    client._manager.get = Mock(
        return_value=Result(status_code=200, message="OK", data={})
    )

    client.daily_cardiovascular_age(
        start_date="2025-01-01", end_date="2025-01-02", document_id="record-1"
    )

    client._manager.get.assert_called_once_with(
        "daily_cardiovascular_age/record-1",
        params={},
    )


def test_document_id_cannot_be_combined_with_next_token():
    client = make_client()

    with pytest.raises(ValueError, match="document_id and next_token"):
        client.daily_cardiovascular_age(document_id="record-1", next_token="page-2")


def test_heartrate_uses_datetime_parameters():
    client = make_client()
    client._manager.get = Mock(
        return_value=Result(
            status_code=200,
            message="OK",
            data={"next_token": None, "data": []},
        )
    )

    client.heartrate(
        start_datetime="2025-01-01T00:00:00Z",
        end_datetime="2025-01-02T00:00:00Z",
        start_date="2025-01-01",
        end_date="2025-01-02",
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


def test_heartrate_defaults_to_datetime_parameters():
    client = make_client()
    client._manager.get = Mock(
        return_value=Result(200, "OK", {"next_token": None, "data": []})
    )

    client.heartrate()

    params = client._manager.get.call_args.kwargs["params"]
    assert set(params) == {"start_datetime", "end_datetime"}
    assert params["start_datetime"].endswith("Z")
    assert params["end_datetime"].endswith("Z")


def test_webhook_routes_use_version_root():
    client = make_client()
    client._manager.get = Mock(
        return_value=Result(status_code=200, message="OK", data={"data": []})
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
    headers = {
        "x-client-id": "client_id",
        "x-client-secret": "client_secret",
    }

    client.list_webhook_subscriptions()
    client.create_webhook_subscription({"callback_url": "https://example.test"})
    client.get_webhook_subscription("sub-1")
    client.update_webhook_subscription(
        "sub-1", {"callback_url": "https://example.test"}
    )
    client.renew_webhook_subscription("sub-1")
    client.delete_webhook_subscription("sub-1")

    client._manager.get.assert_any_call(
        endpoint="../webhook/subscription", headers=headers
    )
    client._manager.get.assert_any_call(
        "../webhook/subscription/sub-1", headers=headers
    )
    client._manager.post.assert_called_once_with(
        endpoint="../webhook/subscription",
        data={"callback_url": "https://example.test"},
        headers=headers,
    )
    client._manager.put.assert_any_call(
        "../webhook/subscription/sub-1",
        data={"callback_url": "https://example.test"},
        headers=headers,
    )
    client._manager.put.assert_any_call(
        endpoint="../webhook/subscription/renew/sub-1", headers=headers
    )
    client._manager.delete.assert_called_once_with(
        endpoint="../webhook/subscription/sub-1", headers=headers
    )
