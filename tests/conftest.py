import pytest
import requests


@pytest.fixture(autouse=True)
def disable_network_calls(monkeypatch):
    def stunted_req():
        raise RuntimeError("Network access disabled during testing.")

    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: stunted_req())
    monkeypatch.setattr(requests, "post", lambda *args, **kwargs: stunted_req())
