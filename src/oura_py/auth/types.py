from collections.abc import Callable
from typing import Required, TypedDict


class OAuthToken(TypedDict, total=False):
    """OAuth credentials accepted by the Oura client."""

    access_token: Required[str]
    token_type: str
    refresh_token: str
    expires_at: float
    expires_in: int
    scope: str | list[str]


TokenUpdater = Callable[[OAuthToken], None]
