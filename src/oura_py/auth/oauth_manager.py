import requests
from requests_oauthlib import OAuth2Session


class OuraOAuth2Client:
    AUTHORIZE_URL = "https://cloud.ouraring.com/oauth/authorize"
    TOKEN_URL = "https://api.ouraring.com/oauth/token"
    SCOPE = (
        "email",
        "personal",
        "daily",
        "heartrate",
        "workout",
        "tag",
        "session",
        "spo2",
    )

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = OAuth2Session(
            client_id=self.client_id, auto_refresh_url=self.TOKEN_URL
        )

    def get_authorization_url(
        self,
        scope: list[str] = None,
        redirect_uri: str | None = None,
        state: str | None = None,
    ) -> tuple[str, str]:
        self.session.scope = scope or self.SCOPE
        self.session.redirect_uri = redirect_uri
        return self.session.authorization_url(url=self.AUTHORIZE_URL, state=state)

    def exchange_code(self, code: str) -> dict:
        resp = requests.post(
            self.TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": self.session.redirect_uri,
            },
            auth=(self.client_id, self.client_secret),
        )
        resp.raise_for_status()
        return resp.json()
