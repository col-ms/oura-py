from typing import Dict, List
from datetime import datetime


class Result:
    """the result of an HTTP request operation.

    Attributes:
        status_code: An integer indicating the status code of the result.
        message: A human readable string describing the reason.
        data: A list of dictionaries (or single dictionary) containing the response data.
    """

    def __init__(self, status_code: int, message: str, data: List[Dict] = None) -> None:
        self.status_code = int(status_code)
        self.message = str(message)
        self.data = data if data else []


class PersonalInfo:
    """The user's personal info.

    Attributes:
        id: The user's Oura API ID.
        age: The user's age.
        weight: The user's weight in kilograms.
        height: The user's height in meters.
        biological_sex: The user's biological sex.
        email: The user's email address.
    """

    def __init__(
        self,
        id: str,
        age: int,
        weight: float,
        height: float,
        biological_sex: str,
        email: str,
    ) -> None:
        self.id = str(id)
        self.age = int(age)
        self.weight = float(weight)
        self.height = float(height)
        self.sex = str(biological_sex)
        self.email = str(email)


class RingConfigData:
    """Represents the configuration of a ring.

    Attributes:
        id (str): The unique identifier of the ring.
        color (str): The color of the ring.
        design (str): The design of the ring.
        firmware_version (str): The firmware version of the ring.
        hardware_type (str): The hardware type of the ring.
        set_up_at (datetime): The date and time when the ring was set up.
        size (int): The size of the ring.
        next_token (str): The next token for pagination or other purposes.
    """

    def __init__(
        self,
        id: str,
        color: str,
        design: str,
        firmware_version: str,
        hardware_type: str,
        set_up_at: datetime,
        size: int,
    ) -> None:
        self.id = id
        self.color = color
        self.design = design
        self.firmware_version = firmware_version
        self.hardware_type = hardware_type
        self.set_up_at = set_up_at
        self.size = size


class RingConfig:
    """Represents the configuration of a ring.

    Attributes:
        data (RingConfigData): The data of the ring configuration.
        next_token (str): Document ID for next result, if available.
    """

    def __init__(
        self, data: List[RingConfigData], next_token: str | None = None
    ) -> None:
        self.data = [RingConfigData(**d) for d in data] if data else []
        self.next_token = next_token


class SleepContributors:
    def __init__(
        self,
        deep_sleep: int,
        efficiency: int,
        latency: int,
        rem_sleep: int,
        restfulness: int,
        timing: int,
        total_sleep: int,
    ) -> None:
        self.deep_sleep = deep_sleep
        self.efficiency = efficiency
        self.latency = latency
        self.rem_sleep = rem_sleep
        self.restfulness = restfulness
        self.timing = timing
        self.total_sleep = total_sleep


class SleepSummaryDatum:
    def __init__(
        self,
        id: str,
        contributors: SleepContributors,
        day: datetime,
        score: int,
        timestamp: datetime,
    ) -> None:
        self.id = id
        self.contributors = SleepContributors(**contributors)
        self.day = day
        self.score = score
        self.timestamp = timestamp


class SleepSummary:
    def __init__(
        self, data: List[SleepSummaryDatum], next_token: str | None = None
    ) -> None:
        self.data = [SleepSummaryDatum(**d) for d in data] if data else []
        self.next_token = next_token
