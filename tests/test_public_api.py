import oura_py
from oura_py import auth, client, data
from oura_py.auth.oauth_manager import OuraOAuth2Client
from oura_py.client.oura_client import OuraClient
from oura_py.data import models
from oura_py.data.exceptions import OuraPyException
from oura_py.data.response import OuraResponse


def test_top_level_public_exports():
    assert oura_py.__all__ == ["OuraClient", "WebhookDataType"]
    assert oura_py.OuraClient is OuraClient


def test_client_public_exports():
    assert client.__all__ == ["OuraClient"]
    assert client.OuraClient is OuraClient
    assert not hasattr(client, "RequestManager")


def test_data_public_exports():
    assert data.__all__ == ["OuraPyException", "OuraResponse", "models"]
    assert data.OuraPyException is OuraPyException
    assert data.OuraResponse is OuraResponse
    assert data.models is models


def test_auth_public_exports():
    assert auth.__all__ == [
        "OuraOAuth2Client",
    ]
    assert auth.OuraOAuth2Client is OuraOAuth2Client
