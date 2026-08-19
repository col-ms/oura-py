from requests_oauthlib import OAuth2Session

from oura_py.constants import AUTHORIZE_URL, SCOPE, TOKEN_URL


class OuraOAuth2Client:
    def __init__(self, client_id: str, client_secret: str) -> None:
        if not client_id or not client_secret:
            raise ValueError("client_id and client_secret are required")
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = OAuth2Session(
            client_id=self.client_id,
            auto_refresh_url=TOKEN_URL,
            auto_refresh_kwargs={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
        )

    def get_authorization_url(
        self,
        scope: list[str] | None = None,
        redirect_uri: str | None = None,
        state: str | None = None,
    ) -> tuple[str, str]:
        self.session.scope = scope or SCOPE
        self.session.redirect_uri = redirect_uri
        return self.session.authorization_url(url=AUTHORIZE_URL, state=state)

    def exchange_code(self, code: str) -> dict:
        return self.session.fetch_token(
            token_url=TOKEN_URL,
            code=code,
            client_secret=self.client_secret,
            include_client_id=True,
        )

    def refresh_access_token(self, refresh_token: str) -> dict:
        if not refresh_token:
            raise ValueError("refresh_token is required")
        token = self.session.refresh_token(
            token_url=TOKEN_URL,
            refresh_token=refresh_token,
            client_id=self.client_id,
            client_secret=self.client_secret,
        )
        # OAuth providers are allowed to omit refresh_token when it has not
        # rotated. Keep the existing credential in that case.
        token.setdefault("refresh_token", refresh_token)
        return token
