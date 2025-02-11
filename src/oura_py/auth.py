import requests


class PersonalTokenRequestHandler:
    def __init__(self, personal_access_token):
        self.personal_access_token = personal_access_token

    def make_request(self, url, method="GET"):
        request_method = requests.post if method == "POST" else requests.get
        return request_method(
            url, headers={"Authorization": f"Bearer: {self.personal_access_token}"}
        )

    def revoke_token(self):
        return self.make_request("https://api.ouraring.com/oauth/revoke", method="POST")
