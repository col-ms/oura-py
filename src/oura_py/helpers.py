import logging
from collections.abc import Callable
from json import JSONDecodeError

import requests
from requests_oauthlib import OAuth2Session
from urllib3.exceptions import InsecureRequestWarning

from oura_py.constants import BASE_URL, PATH, TOKEN_URL, VERSION
from oura_py.exceptions import OuraPyException
from oura_py.models import Result


class RequestManager:
    def __init__(
        self,
        client_id: str,
        token: dict,
        client_secret: str | None = None,
        token_updater: Callable | None = None,
        ssl_verify: bool = True,
        logger: logging.Logger | None = None,
    ) -> None:
        """Manage authenticated HTTP requests to the Oura API.

        Args:
            client_id: OAuth application client ID.
            token: Complete OAuth token response, including ``access_token``.
            client_secret: OAuth application client secret.
            token_updater: Optional callback invoked with a refreshed token.
            ssl_verify: Whether to verify SSL certificates.
            logger: Optional logger used for request diagnostics.
        """
        self._url = f"{BASE_URL}/{VERSION}/{PATH}"
        self._version_url = f"{BASE_URL}/{VERSION}"
        self._client_id = client_id
        self._client_secret = client_secret
        self._logger = logger or logging.getLogger(__name__)
        self._ssl_verify = ssl_verify
        if not ssl_verify:
            requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

        token = dict(token)
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

    def get(self, endpoint: str, params: dict | None = None) -> Result:
        """Sends a GET request to the specified endpoint with optional parameters.

        Args:
            endpoint (str): The API endpoint to send the GET request to.
            params (Dict, optional): A dictionary of query parameters to include in the request. Defaults to None.

        Returns:
            Result: The result of the GET request.
        """
        return self._request(method="GET", endpoint=endpoint, params=params)

    def post(
        self, endpoint: str, params: dict | None = None, data: dict | None = None
    ) -> Result:
        """
        Sends a POST request to the specified endpoint with the given parameters and data.

        Args:
            endpoint (str): The API endpoint to send the request to.
            params (Dict, optional): The query parameters to include in the request. Defaults to None.
            data (Dict, optional): The data to include in the body of the request. Defaults to None.

        Returns:
            Result: The result of the POST request.
        """
        return self._request(method="POST", endpoint=endpoint, params=params, data=data)

    def put(self, endpoint: str, data: dict | None = None) -> Result:
        """Send a JSON PUT request to an API endpoint."""
        return self._request(method="PUT", endpoint=endpoint, data=data)

    def delete(self, endpoint: str) -> Result:
        """Send a DELETE request to an API endpoint."""
        return self._request(method="DELETE", endpoint=endpoint)

    def webhook_get(self, endpoint: str) -> Result:
        """Send a webhook-management GET using client credential headers."""
        return self._request(
            method="GET", endpoint=endpoint, headers=self._webhook_headers()
        )

    def webhook_post(self, endpoint: str, data: dict) -> Result:
        """Send a webhook-management POST using client credential headers."""
        return self._request(
            method="POST", endpoint=endpoint, data=data, headers=self._webhook_headers()
        )

    def webhook_put(self, endpoint: str, data: dict | None = None) -> Result:
        """Send a webhook-management PUT using client credential headers."""
        return self._request(
            method="PUT", endpoint=endpoint, data=data, headers=self._webhook_headers()
        )

    def webhook_delete(self, endpoint: str) -> Result:
        """Send a webhook-management DELETE using client credential headers."""
        return self._request(
            method="DELETE", endpoint=endpoint, headers=self._webhook_headers()
        )

    def _webhook_headers(self) -> dict[str, str]:
        if not self._client_secret:
            raise ValueError("client_secret is required for webhook operations")
        return {
            "x-client-id": self._client_id,
            "x-client-secret": self._client_secret,
        }

    def _request(
        self,
        method: str,
        endpoint: str,
        params: dict | None = None,
        data: dict | None = None,
        headers: dict[str, str] | None = None,
    ) -> Result:
        """
        Makes an HTTP request to the specified endpoint with the given method, parameters, and data.

        Args:
            method (str): The HTTP method to use for the request (e.g., 'GET', 'POST').
            endpoint (str): The API endpoint to send the request to.
            params (Dict, optional): The query parameters to include in the request. Defaults to None.
            data (Dict, optional): The data to include in the request body. Defaults to None.

        Returns:
            Result: An object containing the status code, message, and data from the response.

        Raises:
            OuraPyException: If there is an error making the request or if the response contains bad JSON.
        """
        url = (
            f"{self._version_url}/{endpoint[3:]}"
            if endpoint.startswith("../")
            else f"{self._url}/{endpoint}"
        )
        log_pre = f"method={method}, url={url}, params={params}"
        log_post = "success={}, status_code={}, message={}"
        try:
            self._logger.debug(msg=log_pre)
            response = self._session.request(
                method=method,
                url=url,
                params=params,
                json=data if method in {"POST", "PUT", "PATCH"} else None,
                headers=headers,
                verify=self._ssl_verify,
            )
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=str(e))
            raise OuraPyException("Error making request") from e
        if response.status_code == 204 or not response.content:
            data_out = {}
        else:
            try:
                data_out = response.json()
            except (ValueError, JSONDecodeError) as e:
                self._logger.error(msg=log_post.format(False, None, e))
                raise OuraPyException("Bad JSON in response") from e
        # Result currently models payloads as dictionaries. Some Oura
        # endpoints, including webhook subscription listing, return a
        # top-level JSON array, so preserve that payload under ``data``.
        if not isinstance(data_out, dict):
            data_out = {"data": data_out}
        req_success = 299 >= response.status_code >= 200
        log_line = log_post.format(req_success, response.status_code, response.reason)
        if req_success:
            self._logger.debug(msg=log_line)
            return Result(
                status_code=response.status_code, message=response.reason, data=data_out
            )
        self._logger.error(msg=log_line)
        detail = data_out.get("detail") if isinstance(data_out, dict) else None
        error_message = f"{response.status_code}: {response.reason}"
        if detail:
            error_message += f" - {detail}"
        elif data_out:
            error_message += f" - {data_out}"
        raise OuraPyException(error_message)
