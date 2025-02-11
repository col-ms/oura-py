import pytest
from unittest.mock import patch
from oura_py.auth import PersonalTokenRequestHandler


@pytest.fixture
def handler():
    return PersonalTokenRequestHandler(personal_access_token="test_token")


@patch("requests.get")
def test_make_request_get(mock_get, handler):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "Success"

    response = handler.make_request(url="https://api.example.com/data", method="GET")

    mock_get.assert_called_once_with(
        "https://api.example.com/data", headers={"Authorization": "Bearer test_token"}
    )
    assert response.status_code == 200
    assert response.text == "Success"


@patch("requests.post")
def test_make_request_post(mock_post, handler):
    mock_post.return_value.status_code = 201
    mock_post.return_value.text = "Created"

    response = handler.make_request(url="https://api.example.com/data", method="POST")

    mock_post.assert_called_once_with(
        "https://api.example.com/data", headers={"Authorization": "Bearer test_token"}
    )
    assert response.status_code == 201
    assert response.text == "Created"


@patch("requests.get")
def test_make_request_no_url(mock_get, handler):
    with pytest.raises(TypeError):
        handler.make_request(method="GET")


def test_make_request_invalid_method(handler):
    with pytest.raises(ValueError):
        handler.make_request(url="https://api.example.com/data", method="PUT")
