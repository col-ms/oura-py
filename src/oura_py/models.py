from typing import Dict, List, Union
from datetime import datetime
from dataclasses import dataclass, field, fields


def generic_type_checker(self):
    """Generic type checker for dataclass fields."""
    for f in fields(type(self)):
        if not isinstance(getattr(self, f.name), f.type):
            current_type = type(getattr(self, f.name))
            raise TypeError(f"{f.name} must be {f.type}, got {current_type}")


@dataclass
class Result:
    """the result of an HTTP request operation.

    Attributes:
        status_code: An integer indicating the status code of the result.
        message: A human readable string describing the reason.
        data: A list of dictionaries (or single dictionary) containing the response data.
    """

    status_code: int
    message: str
    data: Dict

    def __post_init__(self):
        generic_type_checker(self)


@dataclass
class PersonalInfo:
    id: str
    age: int
    weight: float
    height: float
    biological_sex: str
    email: str

    def __post_init__(self):
        generic_type_checker(self)


@dataclass
class RingConfigData:
    id: str
    color: str
    design: str
    firmware_version: str
    hardware_type: str
    set_up_at: str
    size: int

    def __post_init__(self):
        generic_type_checker(self)


@dataclass
class RingConfig:
    next_token: Union[str, None]
    data: List[RingConfigData] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.data, list):
            self.data = [
                RingConfigData(**item) if isinstance(item, dict) else item
                for item in self.data
            ]


@dataclass
class SleepSummaryContributors:
    deep_sleep: int
    efficiency: int
    latency: int
    rem_sleep: int
    restfulness: int
    timing: int
    total_sleep: int

    def __post_init__(self):
        generic_type_checker(self)


@dataclass
class SleepSummaryDatum:
    id: str
    contributors: SleepSummaryContributors
    day: datetime
    score: int
    timestamp: datetime

    def __post_init__(self):
        if isinstance(self.contributors, dict):
            self.contributors = SleepSummaryContributors(**self.contributors)


@dataclass
class SleepSummary:
    next_token: Union[str, None]
    data: List[SleepSummaryDatum] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.data, list):
            self.data = [
                SleepSummaryDatum(**item) if isinstance(item, dict) else item
                for item in self.data
            ]


@dataclass
class ReadinessSummaryContributors:
    activity_balance: int
    body_temperature: int
    hrv_balance: int
    previous_day_activity: int
    previous_night: int
    recovery_index: int
    resting_heart_rate: int
    sleep_balance: int


@dataclass
class ReadinessSummaryDatum:
    id: str
    contributors: ReadinessSummaryContributors
    day: datetime
    score: int
    temperature_deviation: float
    temperature_trend_deviation: float
    timestamp: datetime

    def __post_init__(self):
        if isinstance(self.contributors, dict):
            self.contributors = ReadinessSummaryContributors(**self.contributors)


@dataclass
class ReadinessSummary:
    next_token: Union[str, None]
    data: List[ReadinessSummaryDatum] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.data, list):
            self.data = [
                ReadinessSummaryDatum(**item) if isinstance(item, dict) else item
                for item in self.data
            ]


@dataclass
class ActivitySummaryContributors:
    meet_daily_targets: int
    move_every_hour: int
    recovery_time: int
    stay_active: int
    training_frequency: int
    training_volume: int


@dataclass
class ActivitySummaryMET:
    interval: float
    items: List[float]
    timestamp: datetime


@dataclass
class ActivitySummaryDatum:
    id: str
    class_5_min: str
    score: int
    active_calories: int
    average_met_minutes: float
    contributors: ActivitySummaryContributors
    equivalent_walking_distance: int
    high_activity_met_minutes: int
    high_activity_time: int
    inactivity_alerts: int
    low_activity_met_minutes: int
    low_activity_time: int
    medium_activity_met_minutes: int
    medium_activity_time: int
    met: ActivitySummaryMET
    meters_to_target: int
    non_wear_time: int
    resting_time: int
    sedentary_met_minutes: int
    sedentary_time: int
    steps: int
    target_calories: int
    target_meters: int
    total_calories: int
    day: datetime
    timestamp: datetime

    def __post_init__(self):
        if isinstance(self.contributors, dict):
            self.contributors = ActivitySummaryContributors(**self.contributors)
        if isinstance(self.met, dict):
            self.met = ActivitySummaryMET(**self.met)


@dataclass
class ActivitySummary:
    next_token: Union[str, None]
    data: List[ActivitySummaryDatum] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.data, list):
            self.data = [
                ActivitySummaryDatum(**item) if isinstance(item, dict) else item
                for item in self.data
            ]


@dataclass
class HeartRateDatum:
    bpm: int
    source: str
    timestamp: datetime


@dataclass
class HeartRateSummary:
    next_token: Union[str, None]
    data: List[HeartRateDatum] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.data, list):
            self.data = [
                HeartRateDatum(**item) if isinstance(item, dict) else item
                for item in self.data
            ]


@dataclass
class StressDatum:
    id: str
    day: datetime
    stress_high: int
    recovery_high: int
    day_summary: str


@dataclass
class StressSummary:
    next_token: Union[str, None]
    data: List[StressDatum] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.data, list):
            self.data = [
                StressDatum(**item) if isinstance(item, dict) else item
                for item in self.data
            ]


@dataclass
class ResilienceContributors:
    sleep_recovery: float
    daytime_recovery: float
    stress: float


@dataclass
class ResilienceDatum:
    id: str
    day: datetime
    contributors: ResilienceContributors
    level: str

    def __post_init__(self):
        if isinstance(self.contributors, dict):
            self.contributors = ResilienceContributors(**self.contributors)


@dataclass
class ResilienceSummary:
    next_token: Union[str, None]
    data: List[ResilienceDatum] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.data, list):
            self.data = [
                ResilienceDatum(**item) if isinstance(item, dict) else item
                for item in self.data
            ]


@dataclass
class Spo2Datum:
    id: str
    day: datetime
    spo2_percentage: dict
    breathing_disturbance_index: int


@dataclass
class Spo2Summary:
    next_token: Union[str, None]
    data: List[Spo2Datum] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.data, list):
            self.data = [
                Spo2Datum(**item) if isinstance(item, dict) else item
                for item in self.data
            ]


@dataclass
class TagDatum:
    id: str
    tag_type_code: str
    start_time: datetime
    end_time: Union[datetime, None]
    start_day: datetime
    end_day: datetime
    comment: str
    custom_name: str


@dataclass
class TagSummary:
    next_token: Union[str, None]
    data: List[TagDatum] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.data, list):
            self.data = [
                TagDatum(**item) if isinstance(item, dict) else item
                for item in self.data
            ]


@dataclass
class RestModeEpisodes:
    tags: List[str]
    timestamp: datetime


@dataclass
class RestModePeriodDatum:
    id: str
    end_day: datetime
    end_time: datetime
    episodes: RestModeEpisodes
    start_day: datetime
    start_time: datetime

    def __post_init__(self):
        if isinstance(self.episodes, dict):
            self.episodes = RestModeEpisodes(**self.episodes)


@dataclass
class RestModePeriodSummary:
    next_token: Union[str, None]
    data: List[RestModePeriodDatum] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.data, list):
            self.data = [
                RestModePeriodDatum(**item) if isinstance(item, dict) else item
                for item in self.data
            ]


@dataclass
class SessionMeasureInfo:
    interval: int
    items: List[Union[float, None]]
    timestamp: datetime


@dataclass
class SessionDatum:
    id: str
    day: datetime
    start_datetime: datetime
    end_datetime: datetime
    type: str
    heart_rate: SessionMeasureInfo
    heart_rate_variability: SessionMeasureInfo
    mood: str
    motion_count: SessionMeasureInfo

    def __post_init__(self):
        if isinstance(self.heart_rate, dict):
            self.heart_rate = SessionMeasureInfo(**self.heart_rate)
        if isinstance(self.heart_rate_variability, dict):
            self.heart_rate_variability = SessionMeasureInfo(
                **self.heart_rate_variability
            )
        if isinstance(self.motion_count, dict):
            self.motion_count = SessionMeasureInfo(**self.motion_count)


@dataclass
class SessionData:
    next_token: Union[str, None]
    data: List[SessionDatum] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.data, list):
            self.data = [
                SessionDatum(**item) if isinstance(item, dict) else item
                for item in self.data
            ]


@dataclass
class SleepDetailDatum:
    id: str
    average_breath: float
    average_heart_rate: float
    average_hrv: int
    awake_time: int
    bedtime_end: datetime
    bedtime_start: datetime
    day: datetime
    deep_sleep_duration: int
    efficiency: int
    heart_rate: SessionMeasureInfo
    hrv: SessionMeasureInfo
    latency: int
    light_sleep_duration: int
    low_battery_alert: bool
    lowest_heart_rate: int
    movement_30_sec: str
    period: int
    readiness: ReadinessSummaryDatum
    readiness_score_delta: int
    rem_sleep_duration: int
    restless_periods: int
    sleep_phase_5_min: str
    sleep_score_delta: int
    sleep_algorithm_version: str
    time_in_bed: int
    total_sleep_duration: int
    type: str

    def __post_init__(self):
        if isinstance(self.heart_rate, dict):
            self.heart_rate = SessionMeasureInfo(**self.heart_rate)
        if isinstance(self.hrv, dict):
            self.hrv = SessionMeasureInfo(**self.hrv)
        if isinstance(self.readiness, dict):
            self.readiness = ReadinessSummaryDatum(
                **self.readiness, id=None, timestamp=self.bedtime_start, day=self.day
            )


@dataclass
class SleepDetailData:
    next_token: Union[str, None]
    data: List[SleepDetailDatum] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.data, list):
            self.data = [
                SleepDetailDatum(**item) if isinstance(item, dict) else item
                for item in self.data
            ]


@dataclass
class SleepTimeWindow:
    day_tz: int
    end_offset: int
    start_offset: int


@dataclass
class SleepTimeDatum:
    id: str
    day: str
    optimal_bedtime: Union[SleepTimeWindow, None]
    recommendation: str
    status: str

    def __post_init__(self):
        if isinstance(self.optimal_bedtime, dict):
            self.optimal_bedtime = SleepTimeWindow(**self.optimal_bedtime)


@dataclass
class SleepTimeData:
    next_token: Union[str, None]
    data: List[SleepTimeDatum] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.data, list):
            self.data = [
                SleepTimeDatum(**item) if isinstance(item, dict) else item
                for item in self.data
            ]


@dataclass
class VO2MaxDatum:
    id: str
    day: datetime
    timestamp: datetime
    vo2_max: int


@dataclass
class VO2MaxData:
    next_token: Union[str, None]
    data: List[VO2MaxDatum] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.data, list):
            self.data = [
                VO2MaxDatum(**item) if isinstance(item, dict) else item
                for item in self.data
            ]


@dataclass
class WorkoutDatum:
    id: str
    activity: str
    calories: float
    day: datetime
    distance: float
    end_datetime: datetime
    intensity: str
    label: str
    source: str
    start_datetime: datetime


@dataclass
class WorkoutData:
    next_token: Union[str, None]
    data: List[WorkoutDatum] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.data, list):
            self.data = [
                WorkoutDatum(**item) if isinstance(item, dict) else item
                for item in self.data
            ]
