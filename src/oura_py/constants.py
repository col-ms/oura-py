from enum import Enum

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

DOC_ID_ERR_MSG = "document_id and next_token cannot be used together"


class WebhookDataType(str, Enum):
    """Data types accepted by Oura webhook subscriptions."""

    TAG = "tag"
    ENHANCED_TAG = "enhanced_tag"
    WORKOUT = "workout"
    SESSION = "session"
    SLEEP = "sleep"
    DAILY_SLEEP = "daily_sleep"
    DAILY_READINESS = "daily_readiness"
    DAILY_ACTIVITY = "daily_activity"
    DAILY_SPO2 = "daily_spo2"
    SLEEP_TIME = "sleep_time"
    REST_MODE_PERIOD = "rest_mode_period"
    RING_CONFIGURATION = "ring_configuration"
    DAILY_STRESS = "daily_stress"
    DAILY_CARDIOVASCULAR_AGE = "daily_cardiovascular_age"
    DAILY_RESILIENCE = "daily_resilience"
    VO2_MAX = "vo2_max"
    MEAL = "meal"
