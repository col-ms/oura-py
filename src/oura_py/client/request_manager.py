import logging
from typing import cast

import requests
from requests_oauthlib import OAuth2Session

from oura_py.auth.types import OAuthToken, TokenUpdater
from oura_py.constants import BASE_URL, PATH, TOKEN_URL, VERSION
from oura_py.data.exceptions import OuraPyException
from oura_py.data.response import Result


class RequestManager:
    def __init__(
        self,
        client_id: str,
        token: OAuthToken,
        client_secret: str | None = None,
        token_updater: TokenUpdater | None = None,
        ssl_verify: bool = True,
    ) -> None:
        """Manage authenticated HTTP requests to the Oura API."""
        self._url = f"{BASE_URL}/{VERSION}/{PATH}"
        self._version_url = f"{BASE_URL}/{VERSION}"
        self._client_id = client_id
        self._client_secret = client_secret
        self._ssl_verify = ssl_verify
        self._logger = logging.getLogger(__name__)
        if not ssl_verify:
            import urllib3

            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        token = cast(OAuthToken, dict(token))
        if not token.get("access_token"):
            raise ValueError("token must contain an access_token")
        token.setdefault("token_type", "Bearer")

        self._session = OAuth2Session(
            client_id=client_id,
            token=token,
            auto_refresh_url=TOKEN_URL,
            auto_refresh_kwargs={
                "client_id": client_id,
                "client_secret": client_secret,
            },
            token_updater=token_updater,
        )

    def get(
        self,
        endpoint: str,
        params: dict | None = None,
        headers: dict[str, str] | None = None,
    ) -> Result:
        """Send a GET request to the specified endpoint."""
        return self._request(
            method="GET", endpoint=endpoint, params=params, headers=headers
        )

    def post(
        self,
        endpoint: str,
        params: dict | None = None,
        data: dict | None = None,
        headers: dict[str, str] | None = None,
    ) -> Result:
        """Send a POST request to the specified endpoint."""
        return self._request(
            method="POST", endpoint=endpoint, params=params, data=data, headers=headers
        )

    def put(
        self,
        endpoint: str,
        data: dict | None = None,
        headers: dict[str, str] | None = None,
    ) -> Result:
        """Send a PUT request to the specified endpoint."""
        return self._request(
            method="PUT", endpoint=endpoint, data=data, headers=headers
        )

    def delete(self, endpoint: str, headers: dict[str, str] | None = None) -> Result:
        """Send a DELETE request to an API endpoint."""
        return self._request(method="DELETE", endpoint=endpoint, headers=headers)

    def _request(
        self,
        method: str,
        endpoint: str,
        params: dict | None = None,
        data: dict | None = None,
        headers: dict[str, str] | None = None,
    ) -> Result:
        """Send a request and return its decoded response."""
        url = (
            f"{self._version_url}/{endpoint[3:]}"
            if endpoint.startswith("../")
            else f"{self._url}/{endpoint}"
        )
        try:
            self._logger.debug("method=%s url=%s params=%s", method, url, params)
            response = self._session.request(
                method=method,
                url=url,
                params=params,
                json=data if method in {"POST", "PUT", "PATCH"} else None,
                headers=headers,
                verify=self._ssl_verify,
            )
        except requests.exceptions.RequestException as e:
            self._logger.error(str(e))
            raise OuraPyException("Error making request") from e
        if response.status_code == 204 or not response.content:
            data_out = {}
        else:
            try:
                data_out = response.json()
            except ValueError as e:
                raise OuraPyException("Bad JSON in response") from e
        # Result currently models payloads as dictionaries. Some Oura
        # endpoints, including webhook subscription listing, return a
        # top-level JSON array, so preserve that payload under ``data``.
        if not isinstance(data_out, dict):
            data_out = {"data": data_out}
        if response.ok:
            return Result(status_code=response.status_code, data=data_out)
        detail = data_out.get("detail") if isinstance(data_out, dict) else None
        error_message = f"{response.status_code}: {response.reason}"
        if detail:
            error_message += f" - {detail}"
        elif data_out:
            error_message += f" - {data_out}"
        self._logger.error(error_message)
        raise OuraPyException(error_message)
