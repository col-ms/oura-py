import pytest
import requests
from unittest.mock import patch, Mock
from oura_py.helpers import RequestManager
from oura_py.exceptions import OuraPyException


@pytest.fixture
def manager():
    return RequestManager(
        personal_access_token="test_token",
        hostname="api.example.com",
        ver="v1",
        path="data",
    )


def test_good_manager_init(manager):
    assert manager._url == "https://api.example.com/v1/data"
    assert manager._personal_access_token == "test_token"
    assert manager._ssl_verify
    assert manager._logger.name == "oura_py.helpers"


def test_bad_manage_init():
    with pytest.raises(TypeError):
        RequestManager()


def test_good_get(manager):
    with patch("oura_py.helpers.requests.request") as mock_request:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.reason = "OK"
        mock_response.json.return_value = {"data": "test data"}
        mock_request.return_value = mock_response

        result = manager.get("test_endpoint")
        assert result.data == {"data": "test data"}
        assert result.status_code == 200
        assert result.message == "OK"


def test_get_request_exception(manager):
    with patch(
        "oura_py.helpers.requests.request",
        side_effect=requests.exceptions.RequestException,
    ):
        with pytest.raises(OuraPyException, match="Error making request"):
            manager.get("test_endpoint")


def test_get_bad_json(manager):
    with patch("oura_py.helpers.requests.request") as mock_request:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.reason = "OK"
        mock_response.json.side_effect = ValueError("No JSON object could be decoded")
        mock_request.return_value = mock_response

        with pytest.raises(OuraPyException, match="Bad JSON in response"):
            manager.get("test_endpoint")


def test_get_non_2xx_status(manager):
    with patch("oura_py.helpers.requests.request") as mock_request:
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.reason = "Not Found"
        mock_response.json.return_value = {"error": "not found"}
        mock_request.return_value = mock_response

        with pytest.raises(OuraPyException, match="404: Not Found"):
            manager.get("test_endpoint")
