BASE_URL = "https://api.ouraring.com"
VERSION = "v2"
PATH = "usercollection"
AUTHORIZE_URL = "https://cloud.ouraring.com/oauth/authorize"
TOKEN_URL = f"{BASE_URL}/oauth/token"
SCOPE = (
    "email",
    "personal",
    "daily",
    "heartrate",
    "workout",
    "tag",
    "session",
    "spo2",
)
