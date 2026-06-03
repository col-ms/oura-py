import json
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

from oura_py.auth.oauth_manager import OuraOAuth2Client

CACHE_FILE = Path(".oura_tokens.json")


class TokenManager:
    def __init__(self, client: OuraOAuth2Client):
        self.client = client

    def get_valid_token(self) -> str:
        """Return a valid access token, refreshing or re-authorizing as needed."""
        tokens = self._load_cache()

        if tokens:
            if self._is_expired(tokens):
                tokens = self.client.refresh_access_token(tokens["refresh_token"])
                self._save_cache(tokens)
            return tokens["access_token"]

        tokens = self._authorize()
        self._save_cache(tokens)
        return tokens["access_token"]

    def _authorize(self) -> dict:
        url, state = self.client.get_authorization_url()
        print(f"Opening browser for Oura authorization...\n{url}\n")
        webbrowser.open(url)

        params = self._wait_for_callback()

        if "error" in params:
            raise RuntimeError(f"Authorization denied: {params['error'][0]}")
        if params.get("state", [None])[0] != state:
            raise RuntimeError("State mismatch — possible CSRF. Aborting.")

        return self.client.exchange_code(params["code"][0])

    def _wait_for_callback(self, port: int = 8080) -> dict:
        server = HTTPServer(("localhost", port), _CallbackHandler)
        server.handle_request()
        return server.callback_params

    def _save_cache(self, tokens: dict):
        tokens["cached_at"] = time.time()
        CACHE_FILE.write_text(json.dumps(tokens))

    def _load_cache(self) -> dict | None:
        if not CACHE_FILE.exists():
            return None
        return json.loads(CACHE_FILE.read_text())

    def _is_expired(self, tokens: dict) -> bool:
        expires_in = tokens.get("expires_in", 0)
        cached_at = tokens.get("cached_at", 0)
        return time.time() >= cached_at + expires_in - 60


class _CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.server.callback_params = parse_qs(urlparse(self.path).query)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Authorization successful - you can close this tab.")

    def log_message(self, *args):
        pass
