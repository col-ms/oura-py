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


class SleepSummaryContributors:
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
        contributors: SleepSummaryContributors,
        day: datetime,
        score: int,
        timestamp: datetime,
    ) -> None:
        self.id = id
        self.contributors = SleepSummaryContributors(**contributors)
        self.day = day
        self.score = score
        self.timestamp = timestamp


class SleepSummary:
    def __init__(
        self, data: List[SleepSummaryDatum], next_token: str | None = None
    ) -> None:
        self.data = [SleepSummaryDatum(**d) for d in data] if data else []
        self.next_token = next_token


class ReadinessSummaryContributors:
    def __init__(
        self,
        activity_balance: int,
        body_temperature: int,
        hrv_balance: int,
        previous_day_activity: int,
        previous_night: int,
        recovery_index: int,
        resting_heart_rate: int,
        sleep_balance: int,
    ) -> None:
        self.acitvity_balance = activity_balance
        self.body_temperature = body_temperature
        self.hrv_balance = hrv_balance
        self.previous_day_activity = previous_day_activity
        self.previous_night = previous_night
        self.recovery_index = recovery_index
        self.resting_heart_rate = resting_heart_rate
        self.sleep_balance = sleep_balance


class ReadinessSummaryDatum:
    def __init__(
        self,
        id: str,
        contributors: ReadinessSummaryContributors,
        day: datetime,
        score: int,
        temperature_deviation: float,
        temperature_trend_deviation: float,
        timestamp: datetime,
    ) -> None:
        self.id = id
        self.contributors = ReadinessSummaryContributors(**contributors)
        self.day = day
        self.score = score
        self.temperature_deviation = temperature_deviation
        self.temperature_trend_deviation = temperature_trend_deviation
        self.timestamp = timestamp


class ReadinessSummary:
    def __init__(
        self, data: List[ReadinessSummaryDatum], next_token: str | None = None
    ) -> None:
        self.data = [ReadinessSummaryDatum(**d) for d in data] if data else []
        self.next_token = next_token


class ActivitySummaryContributors:
    def __init__(
        self,
        meet_daily_targets: int,
        move_every_hour: int,
        recovery_time: int,
        stay_active: int,
        training_frequency: int,
        training_volume: int,
    ) -> None:
        self.meet_daily_targets = meet_daily_targets
        self.move_every_hour = move_every_hour
        self.recovery_time = recovery_time
        self.stay_active = stay_active
        self.training_frequency = training_frequency
        self.training_volume = training_volume


class ActivitySummaryMET:
    def __init__(
        self, interval: float, items: List[float], timestamp: datetime
    ) -> None:
        self.interval = interval
        self.items = items
        self.timestamp = timestamp


class ActivitySummaryDatum:
    def __init__(
        self,
        id: str,
        class_5_min: str,
        score: int,
        active_calories: int,
        average_met_minutes: float,
        contributors: ActivitySummaryContributors,
        equivalent_walking_distance: int,
        high_activity_met_minutes: int,
        high_activity_time: int,
        inactivity_alerts: int,
        low_activity_met_minutes: int,
        low_activity_time: int,
        medium_activity_met_minutes: int,
        medium_activity_time: int,
        met: ActivitySummaryMET,
        meters_to_target: int,
        non_wear_time: int,
        resting_time: int,
        sedentary_met_minutes: int,
        sedentary_time: int,
        steps: int,
        target_calories: int,
        target_meters: int,
        total_calories: int,
        day: datetime,
        timestamp: datetime,
    ) -> None:
        self.id = id
        self.class_5_min = class_5_min
        self.score = score
        self.active_calories = active_calories
        self.average_met_minutes = average_met_minutes
        self.contributors = ActivitySummaryContributors(**contributors)
        self.equivalent_walking_distance = equivalent_walking_distance
        self.high_activity_met_minutes = high_activity_met_minutes
        self.high_activity_time = high_activity_time
        self.inactivity_alerts = inactivity_alerts
        self.low_activity_met_minutes = low_activity_met_minutes
        self.low_activity_time = low_activity_time
        self.medium_activity_met_minutes = medium_activity_met_minutes
        self.medium_activity_time = medium_activity_time
        self.met = ActivitySummaryMET(**met)
        self.meters_to_target = meters_to_target
        self.non_wear_time = non_wear_time
        self.resting_time = resting_time
        self.sedentary_met_minutes = sedentary_met_minutes
        self.sedentary_time = sedentary_time
        self.steps = steps
        self.target_calories = target_calories
        self.target_meters = target_meters
        self.total_calories = total_calories
        self.day = day
        self.timestamp = timestamp


class ActivitySummary:
    def __init__(
        self, data: List[ActivitySummaryDatum], next_token: str | None = None
    ) -> None:
        self.data = [ActivitySummaryDatum(**d) for d in data] if data else []
        self.next_token = next_token


class HeartRateDatum:
    def __init__(
        self,
        bpm: int,
        source: str,
        timestamp: datetime,
    ) -> None:
        self.bpm = bpm
        self.source = source
        self.timestamp = timestamp


class HeartRateSummary:
    def __init__(
        self, data: List[HeartRateDatum], next_token: str | None = None
    ) -> None:
        self.data = [HeartRateDatum(**d) for d in data] if data else []
        self.next_token = next_token


class StressDatum:
    def __init__(
        self,
        id: str,
        day: datetime,
        stress_high: int,
        recovery_high: int,
        day_summary: str,
    ) -> None:
        self.id = id
        self.day = day
        self.stress_high = stress_high
        self.recovery_high = recovery_high
        self.day_summary = day_summary


class StressSummary:
    def __init__(self, data: List[StressDatum], next_token: str | None = None) -> None:
        self.data = [StressDatum(**d) for d in data] if data else []
        self.next_token = next_token


class ResilienceContributors:
    def __init__(
        self,
        sleep_recovery: float,
        daytime_recovery: float,
        stress: float,
    ) -> None:
        self.sleep_recovery = sleep_recovery
        self.daytime_recovery = daytime_recovery
        self.stress = stress


class ResilienceDatum:
    def __init__(
        self,
        id: str,
        day: datetime,
        contributors: ResilienceContributors,
        level: str,
    ) -> None:
        self.id = id
        self.day = day
        self.contributors = ResilienceContributors(**contributors)
        self.level = level


class ResilienceSummary:
    def __init__(
        self, data: List[ResilienceDatum], next_token: str | None = None
    ) -> None:
        self.data = [ResilienceDatum(**d) for d in data] if data else []
        self.next_token = next_token
