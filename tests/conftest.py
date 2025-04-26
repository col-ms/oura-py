import pytest
import requests


@pytest.fixture(autouse=True)
def disable_network_calls(monkeypatch):
    def stunted_req():
        raise RuntimeError("Network access disabled during testing.")

    monkeypatch.setattr(requests, "request", lambda *args, **kwargs: stunted_req())


@pytest.fixture()
def result_data():
    return {
        "status_code": 200,
        "message": "OK",
        "data": {"key": "value"},
    }


@pytest.fixture()
def personal_info_data():
    return {
        "id": "12345",
        "age": 30,
        "weight": 70.5,
        "height": 175.1,
        "biological_sex": "Male",
        "email": "john.smith@example.com",
    }


@pytest.fixture()
def ring_config_data():
    return {
        "id": "12345",
        "color": "glossy_black",
        "design": "horizon",
        "firmware_version": "3.2.2",
        "hardware_type": "gen3",
        "set_up_at": "2024-12-31T00:00:00+00:00",
        "size": 9,
    }
