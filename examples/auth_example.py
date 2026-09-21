import json
import os
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from dotenv import load_dotenv

from oura_py import OuraClient
from oura_py.auth import OuraOAuth2Client
from oura_py.auth.types import OAuthToken

TOKEN_PATH = Path(".oura_tokens.json")


def save_token(token: OAuthToken) -> None:
    """Persist refreshed credentials without touching the application's token."""
    TOKEN_PATH.write_text(json.dumps(token, indent=2), encoding="utf-8")


if __name__ == "__main__":
    load_dotenv()

    client_id = os.environ["CLIENT_ID"]
    client_secret = os.environ["CLIENT_SECRET"]
    redirect_uri = os.getenv("REDIRECT_URI", "http://localhost:8080/callback")

    oauth = OuraOAuth2Client(client_id, client_secret)
    authorization_url, state = oauth.get_authorization_url(
        redirect_uri=redirect_uri,
    )
    print(f"Open this URL and authorize the application:\n\n{authorization_url}")
    callback_url = input("Paste the complete callback URL: ").strip()
    params = parse_qs(urlparse(callback_url).query)

    if params.get("state", [None])[0] != state:
        raise RuntimeError("State mismatch; authorization was rejected")
    if params.get("error", [None])[0]:
        raise RuntimeError(f"Authorization denied: {params['error'][0]}")

    code = params.get("code", [None])[0]
    if not code:
        raise RuntimeError("Callback URL did not contain an authorization code")

    token = oauth.exchange_code(code)
    save_token(token)

    client = OuraClient(
        client_id=client_id,
        client_secret=client_secret,
        token=token,
        token_updater=save_token,
    )

    print(client.personal_info().raw())
    print(f"Token saved to {TOKEN_PATH}")
