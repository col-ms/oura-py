import json
import os
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Protocol
from urllib.parse import parse_qs, urlparse

from oura_py.auth.oauth_manager import OuraOAuth2Client


class TokenStore(Protocol):
    def load(self) -> dict | None: ...
    def save(self, token: dict) -> None: ...


class JsonTokenStore:
    """Small file-backed token store for local applications."""

    def __init__(self, path: str | Path = ".oura_tokens.json") -> None:
        self.path = Path(path)

    def load(self) -> dict | None:
        if not self.path.exists():
            return None
        try:
            token = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(
                f"Unable to read OAuth token store: {self.path}"
            ) from exc
        return token if isinstance(token, dict) else None

    def save(self, token: dict) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = dict(token)
        payload["cached_at"] = time.time()
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(json.dumps(payload), encoding="utf-8")
        os.replace(temporary, self.path)
        try:
            self.path.chmod(0o600)
        except OSError:
            pass


class TokenManager:
    def __init__(
        self,
        client: OuraOAuth2Client,
        store: TokenStore | None = None,
        host: str = "localhost",
        port: int = 8080,
        redirect_uri: str | None = None,
    ):
        self.client = client
        self.store = store or JsonTokenStore()
        self.host = host
        self.port = port
        self.redirect_uri = redirect_uri

    def get_valid_token(self, interactive: bool = False) -> dict:
        """Return a complete valid OAuth token, optionally authorizing in a browser."""
        token = self.store.load()

        if token and not self._is_expired(token):
            return token
        if token and token.get("refresh_token"):
            token = self.client.refresh_access_token(token["refresh_token"])
            self.store.save(token)
            return token
        if not interactive:
            raise RuntimeError(
                "No usable Oura OAuth token found; pass interactive=True to authorize"
            )

        token = self._authorize()
        self.store.save(token)
        return token

    def _authorize(self) -> dict:
        if self.redirect_uri:
            parsed_redirect = urlparse(self.redirect_uri)
            if parsed_redirect.scheme != "http" or not parsed_redirect.hostname:
                raise ValueError("redirect_uri must be an HTTP URL with a hostname")
            bind_host = parsed_redirect.hostname
            bind_port = parsed_redirect.port or 80
        else:
            bind_host = self.host
            bind_port = self.port

        server = HTTPServer((bind_host, bind_port), _CallbackHandler)
        redirect_uri = self.redirect_uri or (
            f"http://{bind_host}:{server.server_port}/callback"
        )
        url, state = self.client.get_authorization_url(redirect_uri=redirect_uri)
        print(f"Opening browser for Oura authorization...\n{url}\n")
        webbrowser.open(url)

        try:
            params = self._wait_for_callback(server)
        finally:
            server.server_close()

        if "error" in params:
            raise RuntimeError(f"Authorization denied: {params['error'][0]}")
        if params.get("state", [None])[0] != state:
            raise RuntimeError("State mismatch — possible CSRF. Aborting.")
        if not params.get("code", [None])[0]:
            raise RuntimeError("Authorization callback did not contain a code")

        return self.client.exchange_code(params["code"][0])

    def _wait_for_callback(self, server: HTTPServer) -> dict:
        server.timeout = 300
        server.handle_request()
        return getattr(server, "callback_params", {})

    def _is_expired(self, tokens: dict) -> bool:
        if tokens.get("expires_at"):
            expires_at = float(tokens["expires_at"])
        else:
            expires_at = tokens.get("cached_at", 0) + tokens.get("expires_in", 0)
        return time.time() >= expires_at - 60


class _CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.server.callback_params = parse_qs(urlparse(self.path).query)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Authorization successful - you can close this tab.")

    def log_message(self, *args):
        pass
