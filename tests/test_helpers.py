from unittest.mock import Mock, patch

import pytest
import requests

from oura_py.exceptions import OuraPyException
from oura_py.helpers import RequestManager


@pytest.fixture
def manager():
    return RequestManager(client_id="client_id", token={"access_token": "test_token"})


def test_good_manager_init(manager):
    assert manager._url == "https://api.ouraring.com/v2/usercollection"
    assert manager._session.token["access_token"] == "test_token"
    assert manager._session.token["token_type"] == "Bearer"
    assert manager._ssl_verify is True
    assert manager._logger.name == "oura_py.helpers"


def test_init_ssl_verify_false():
    manager = RequestManager(
        client_id="client_id",
        token={"access_token": "test_token"},
        ssl_verify=False,
    )
    assert manager._ssl_verify is False


def test_bad_manage_init():
    with pytest.raises(TypeError):
        RequestManager()


def test_good_get(manager):
    with patch.object(manager._session, "request") as mock_request:
        mock_response = Mock(status_code=200, reason="OK")
        mock_response.json.return_value = {"data": "test data"}
        mock_request.return_value = mock_response

        result = manager.get("test_endpoint")
        assert result.data == {"data": "test data"}
        assert result.status_code == 200
        assert result.message == "OK"


def test_get_request_exception(manager):
    with (
        patch.object(
            manager._session,
            "request",
            side_effect=requests.exceptions.RequestException,
        ),
        pytest.raises(OuraPyException, match="Error making request"),
    ):
        manager.get("test_endpoint")


def test_get_bad_json(manager):
    with patch.object(manager._session, "request") as mock_request:
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("No JSON object")
        mock_request.return_value = mock_response

        with pytest.raises(OuraPyException, match="Bad JSON in response"):
            manager.get("test_endpoint")


def test_get_non_2xx_status(manager):
    with patch.object(manager._session, "request") as mock_request:
        mock_response = Mock(status_code=404, reason="Not Found")
        mock_response.json.return_value = {"error": "not found"}
        mock_request.return_value = mock_response

        with pytest.raises(OuraPyException, match="404: Not Found"):
            manager.get("test_endpoint")


def test_good_post(manager):
    with patch.object(manager._session, "request") as mock_request:
        mock_response = Mock(status_code=200, reason="OK")
        mock_response.json.return_value = {"data": "test data"}
        mock_request.return_value = mock_response

        result = manager.post("test_endpoint", data={"key": "value"})
        assert result.data == {"data": "test data"}
