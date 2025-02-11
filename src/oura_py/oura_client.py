from oura_py.auth import PersonalTokenRequestHandler


class OuraClient:
    URL_BASE = "https://api.ouraring.com/v2/usercollection/"

    def __init__(self, personal_access_token=None):
        if personal_access_token is not None:
            self.handler = PersonalTokenRequestHandler(personal_access_token)

    def get_daily_activity(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        document_id: str | None = None,
    ):
        if document_id:
            url = "".join([self.URL_BASE, "daily_activity/", document_id])
            return self.client_request(url)
        else:
            url = "".join([self.URL_BASE, "daily_activity"])
            params = self.build_start_end_params(start_date, end_date)
            return self.client_request(url, params)

    def get_daily_readiness(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        document_id: str | None = None,
    ):
        if document_id:
            url = "".join([self.URL_BASE, "daily_readiness/", document_id])
            return self.client_request(url)
        else:
            url = "".join([self.URL_BASE, "daily_readiness"])
            params = self.build_start_end_params(start_date, end_date)
            return self.client_request(url, params)

    def get_daily_sleep(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        document_id: str | None = None,
    ):
        if document_id:
            url = "".join([self.URL_BASE, "daily_sleep/", document_id])
            return self.client_request(url)
        else:
            url = "".join([self.URL_BASE, "daily_sleep"])
            params = self.build_start_end_params(start_date, end_date)
            return self.client_request(url, params)

    def get_daily_resilience(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        document_id: str | None = None,
    ):
        if document_id:
            url = "".join([self.URL_BASE, "daily_resilience/", document_id])
            return self.client_request(url)
        else:
            url = "".join([self.URL_BASE, "daily_resilience"])
            params = self.build_start_end_params(start_date, end_date)
            return self.client_request(url, params)

    def get_daily_spo2(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        document_id: str | None = None,
    ):
        if document_id:
            url = "".join([self.URL_BASE, "daily_spo2/", document_id])
            return self.client_request(url)
        else:
            url = "".join([self.URL_BASE, "daily_spo2"])
            params = self.build_start_end_params(start_date, end_date)
            return self.client_request(url, params)

    def get_daily_stress(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        document_id: str | None = None,
    ):
        if document_id:
            url = "".join([self.URL_BASE, "daily_stress/", document_id])
            return self.client_request(url)
        else:
            url = "".join([self.URL_BASE, "daily_stress"])
            params = self.build_start_end_params(start_date, end_date)
            return self.client_request(url, params)

    def get_enhanced_tags(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        document_id: str | None = None,
    ):
        if document_id:
            url = "".join([self.URL_BASE, "enhanced_tag/", document_id])
            return self.client_request(url)
        else:
            url = "".join([self.URL_BASE, "enhanced_tag"])
            params = self.build_start_end_params(start_date, end_date)
            return self.client_request(url, params)

    def get_heart_rate(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        document_id: str | None = None,
    ):
        if document_id:
            url = "".join([self.URL_BASE, "heartrate/", document_id])
            return self.client_request(url)
        else:
            url = "".join([self.URL_BASE, "heartrate"])
            params = self.build_start_end_params(start_date, end_date)
            return self.client_request(url, params)

    def get_rest_mode_periods(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        document_id: str | None = None,
    ):
        if document_id:
            url = "".join([self.URL_BASE, "rest_mode_period/", document_id])
            return self.client_request(url)
        else:
            url = "".join([self.URL_BASE, "rest_mode_period"])
            params = self.build_start_end_params(start_date, end_date)
            return self.client_request(url, params)

    def get_sessions(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        document_id: str | None = None,
    ):
        if document_id:
            url = "".join([self.URL_BASE, "session/", document_id])
            return self.client_request(url)
        else:
            url = "".join([self.URL_BASE, "session"])
            params = self.build_start_end_params(start_date, end_date)
            return self.client_request(url, params)

    def get_sleep_detail(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        document_id: str | None = None,
    ):
        if document_id:
            url = "".join([self.URL_BASE, "sleep/", document_id])
            return self.client_request(url)
        else:
            url = "".join([self.URL_BASE, "sleep"])
            params = self.build_start_end_params(start_date, end_date)
            return self.client_request(url, params)

    def get_ring_config(self):
        url = "".join([self.URL_BASE, "ring_configuration"])
        return self.client_request(url)

    def get_personal_info(self):
        url = "".join([self.URL_BASE, "personal_info"])
        return self.client_request(url)

    def client_request(self, url, params: dict = {}):
        response = self.handler.make_request(url, params=params)
        return response.text

    def build_start_end_params(self, start_date: str, end_date: str):
        params = {}

        if start_date is not None:
            if not isinstance(start_date, str):
                raise ValueError("start_date must be a string")
            params["start_date"] = start_date

        if end_date is not None:
            if not isinstance(end_date, str):
                raise ValueError("end_date must be a string")
            params["end_date"] = end_date

        return params
