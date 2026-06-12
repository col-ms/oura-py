import pytest
from oura_py.auth.oauth_manager import OuraOAuth2Client
from urllib.parse import quote
from tests.constants import CLIENT_ID, CLIENT_SECRET, AUTHORIZE_BASE_URL


@pytest.fixture
def auth_client() -> OuraOAuth2Client:
    return OuraOAuth2Client(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)


def test_good_oauth_client_init(auth_client):
    assert auth_client.client_id == CLIENT_ID
    assert auth_client.client_secret == CLIENT_SECRET
    assert auth_client.session.client_id == CLIENT_ID
    assert (
        auth_client.session.auto_refresh_url == "https://api.ouraring.com/oauth/token"
    )


def test_build_auth_url(auth_client):
    auth_url, state = auth_client.get_authorization_url(
        scope=["email", "heartrate"], state="TEST"
    )
    assert (
        auth_url
        == f"{AUTHORIZE_BASE_URL}?response_type=code&client_id=TEST_ID&scope=email+heartrate&state=TEST"
    )
    assert state == "TEST"


def test_build_auth_url_with_redirect(auth_client):
    redirect_uri = "http://localhost:8080/callback"
    encoded_uri = quote(redirect_uri, safe="")
    auth_url, _ = auth_client.get_authorization_url(
        scope=["personal"], redirect_uri=redirect_uri, state="TEST"
    )
    assert (
        auth_url
        == f"{AUTHORIZE_BASE_URL}?response_type=code&client_id=TEST_ID&redirect_uri={encoded_uri}&scope=personal&state=TEST"
    )
