from oura_py.auth import PersonalTokenRequestHandler


class OuraClient:
    URL_BASE = "https://api.ouraring.com/v2/usercollection/"

    def __init__(self, personal_access_token=None):
        if personal_access_token is not None:
            self.handler = PersonalTokenRequestHandler(personal_access_token)

    def _make_request(self, url):
        response = self.handler.make_request(url)
        return response.text

    def get_personal_info(self):
        url = "".join([self.URL_BASE, "personal_info"])
        return self._make_request(url)
