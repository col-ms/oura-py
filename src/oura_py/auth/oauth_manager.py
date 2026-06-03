import requests
import secrets
from urllib.parse import urlencode


AUTHORIZE_URL = "https://cloud.ouraring.com/oauth/authorize"
TOKEN_URL = "https://api.ouraring.com/oauth/token"
ALL_SCOPES = [
    "email",
    "personal",
    "daily",
    "heartrate",
    "workout",
    "tag",
    "session",
    "spo2",
]


class OuraOAuth2Client:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def get_authorization_url(self, scopes: list[str] = None) -> tuple[str, str]:
        state = secrets.token_urlsafe(16)
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": " ".join(scopes or ALL_SCOPES),
            "state": state,
        }
        return f"{AUTHORIZE_URL}?{urlencode(params)}", state

    def exchange_code(self, code: str) -> dict:
        """Exchange an authorization code for access and refresh tokens."""
        resp = requests.post(
            TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": self.redirect_uri,
            },
            auth=(self.client_id, self.client_secret),
        )
        resp.raise_for_status()
        return resp.json()

    def refresh_access_token(self, refresh_token: str) -> dict:
        """Use a refresh token to get a new access token."""
        resp = requests.post(
            TOKEN_URL,
            data={"grant_type": "refresh_token", "refresh_token": refresh_token},
            auth=(self.client_id, self.client_secret),
        )
        resp.raise_for_status()
        return resp.json()
