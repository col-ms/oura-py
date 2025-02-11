import requests


class PersonalTokenRequestHandler:
    def __init__(self, personal_access_token):
        self.personal_access_token = personal_access_token

    def make_request(self, url: str, method: str = "GET") -> requests.Response:
        if not url:
            raise TypeError("URL is required")

        if method not in ["GET", "POST"]:
            raise ValueError("Method must be 'GET' or 'POST'")

        request_method = requests.post if method == "POST" else requests.get
        headers = {"Authorization": f"Bearer {self.personal_access_token}"}

        response = request_method(url, headers=headers)
        response.raise_for_status()

        return response
