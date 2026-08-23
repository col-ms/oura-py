"""Authorize with a custom OAuth scope set using OuraOAuth2Client directly."""

import os
from urllib.parse import parse_qs, urlparse

from dotenv import load_dotenv

from oura_py.auth.oauth_manager import OuraOAuth2Client
from oura_py.client.oura_client import OuraClient

if __name__ == "__main__":
    load_dotenv()
    client_id = os.environ["CLIENT_ID"]
    client_secret = os.environ["CLIENT_SECRET"]
    redirect_uri = os.getenv("REDIRECT_URI", "http://localhost:8080/callback")

    oauth_client = OuraOAuth2Client(client_id, client_secret)
    authorization_url, state = oauth_client.get_authorization_url(
        scope=["personal", "daily", "heartrate"],
        redirect_uri=redirect_uri,
    )

    print("Open this URL in a browser and authorize the application:\n")
    print(authorization_url)
    print(f"\nExpected callback: {redirect_uri}")
    callback_url = input("Paste the complete callback URL: ").strip()
    callback = urlparse(callback_url)

    params = parse_qs(callback.query)
    if params.get("state", [None])[0] != state:
        raise RuntimeError("State mismatch; authorization was rejected")
    if params.get("error", [None])[0]:
        raise RuntimeError(f"Authorization denied: {params['error'][0]}")
    if not params.get("code", [None])[0]:
        raise RuntimeError("Callback URL did not contain an authorization code")

    token = oauth_client.exchange_code(params["code"][0])
    client = OuraClient(
        client_id=client_id,
        client_secret=client_secret,
        token=token,
    )
    print(client.get_personal_info())
