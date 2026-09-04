"""Pydantic models for Oura API v2 response payloads."""

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class OuraModel(BaseModel):
    """Common configuration for API response models."""

    model_config = ConfigDict(extra="ignore", validate_assignment=True)


RingColor = Literal[
    "brushed_silver",
    "glossy_black",
    "glossy_gold",
    "glossy_white",
    "gucci",
    "matt_gold",
    "rose",
    "silver",
    "stealth_black",
    "titanium",
    "titanium_and_gold",
    "cloud",
    "petal",
    "midnight",
    "tide",
    "deep_rose",
]
RingDesign = Literal["heritage", "balance", "balance_diamond", "horizon", "ceramic"]
RingHardwareType = Literal["gen1", "gen2", "gen2m", "gen3", "gen4", "or5"]
HeartRateSource = Literal["awake", "workout", "rest", "sleep", "live", "session"]
StressSummaryType = Literal["restored", "normal", "stressful"]
ResilienceLevel = Literal["limited", "adequate", "solid", "strong", "exceptional"]
MomentMood = Literal["bad", "worse", "same", "good", "great"]
MomentType = Literal[
    "breathing", "meditation", "nap", "relaxation", "rest", "body_status"
]
SleepAlgorithmVersion = Literal["v1", "v2"]
SleepAnalysisReason = Literal[
    "foreground_sleep_analysis",
    "bedtime_edit",
    "background_sleep_analysis",
    "background_created_foreground_updated",
]
SleepType = Literal["deleted", "sleep", "long_sleep", "late_nap", "rest"]
SleepTimeRecommendation = Literal[
    "improve_efficiency",
    "earlier_bedtime",
    "later_bedtime",
    "earlier_wake_up_time",
    "later_wake_up_time",
    "follow_optimal_bedtime",
]
SleepTimeStatus = Literal[
    "not_enough_nights",
    "not_enough_recent_nights",
    "bad_sleep_quality",
    "only_recommended_found",
    "optimal_found",
]
WorkoutIntensity = Literal["easy", "moderate", "hard"]
WorkoutSource = Literal["manual", "autodetected", "confirmed", "workout_heart_rate"]


class DailyActivity(OuraModel):
    id: str
    # TODO fill in class


class DailySleepContributors(OuraModel):
    deep_sleep: int
    efficiency: int
    latency: int
    rem_sleep: int
    restfulness: int
    timing: int
    total_sleep: int


class DailySleep(OuraModel):
    id: str
    contributors: DailySleepContributors
    day: str
    score: int
    timestamp: datetime


class PersonalInfo(OuraModel):
    id: str
    age: int | None = None
    weight: float | None = None
    height: float | None = None
    biological_sex: str | None = None
    email: str | None = None


class RingConfigData(OuraModel):
    id: str
    color: RingColor | None = None
    design: RingDesign | None = None
    firmware_version: str | None = None
    hardware_type: RingHardwareType | None = None
    set_up_at: datetime | None = None
    size: int | None = None


class RingConfig(OuraModel):
    next_token: str | None = None
    data: list[RingConfigData] = Field(default_factory=list)


class SleepSummaryContributors(OuraModel):
    deep_sleep: int | None = None
    efficiency: int | None = None
    latency: int | None = None
    rem_sleep: int | None = None
    restfulness: int | None = None
    timing: int | None = None
    total_sleep: int | None = None


class SleepSummaryDatum(OuraModel):
    id: str
    contributors: SleepSummaryContributors
    day: date
    score: int | None = None
    timestamp: datetime


class SleepSummary(OuraModel):
    next_token: str | None = None
    data: list[SleepSummaryDatum] = Field(default_factory=list)


class ReadinessSummaryContributors(OuraModel):
    activity_balance: int | None = None
    body_temperature: int | None = None
    hrv_balance: int | None = None
    previous_day_activity: int | None = None
    previous_night: int | None = None
    recovery_index: int | None = None
    resting_heart_rate: int | None = None
    sleep_balance: int | None = None
    sleep_regularity: int | None = None


class Readiness(OuraModel):
    contributors: ReadinessSummaryContributors
    score: int | None = None
    temperature_deviation: float | None = None
    temperature_trend_deviation: float | None = None


class ReadinessSummaryDatum(OuraModel):
    id: str
    contributors: ReadinessSummaryContributors
    day: date
    score: int | None = None
    temperature_deviation: float | None = None
    temperature_trend_deviation: float | None = None
    timestamp: datetime


class ReadinessSummary(OuraModel):
    next_token: str | None = None
    data: list[ReadinessSummaryDatum] = Field(default_factory=list)


class ActivitySummaryContributors(OuraModel):
    meet_daily_targets: int | None = None
    move_every_hour: int | None = None
    recovery_time: int | None = None
    stay_active: int | None = None
    training_frequency: int | None = None
    training_volume: int | None = None


class ActivitySummaryMET(OuraModel):
    interval: float
    items: list[float | None]
    timestamp: datetime


class ActivitySummaryDatum(OuraModel):
    id: str
    active_calories: int
    average_met_minutes: float
    class_5_min: str | None = None
    contributors: ActivitySummaryContributors
    day: date
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
    score: int | None = None
    sedentary_met_minutes: int
    sedentary_time: int
    steps: int
    target_calories: int
    target_meters: int
    timestamp: datetime
    total_calories: int


class ActivitySummary(OuraModel):
    next_token: str | None = None
    data: list[ActivitySummaryDatum] = Field(default_factory=list)


class HeartRateDatum(OuraModel):
    timestamp: datetime
    timestamp_unix: int
    bpm: int
    source: HeartRateSource


class HeartRateSummary(OuraModel):
    next_token: str | None = None
    data: list[HeartRateDatum] = Field(default_factory=list)


class StressDatum(OuraModel):
    id: str
    day: date
    day_summary: StressSummaryType | None = None
    stress_high: int | None = None
    recovery_high: int | None = None


class StressSummary(OuraModel):
    next_token: str | None = None
    data: list[StressDatum] = Field(default_factory=list)


class ResilienceContributors(OuraModel):
    sleep_recovery: float
    daytime_recovery: float
    stress: float


class ResilienceDatum(OuraModel):
    id: str
    day: date
    contributors: ResilienceContributors
    level: ResilienceLevel


class ResilienceSummary(OuraModel):
    next_token: str | None = None
    data: list[ResilienceDatum] = Field(default_factory=list)


class Spo2AggregatedValues(OuraModel):
    average: float


class Spo2Datum(OuraModel):
    id: str
    day: date
    spo2_percentage: Spo2AggregatedValues | None = None
    breathing_disturbance_index: int | None = None


class Spo2Summary(OuraModel):
    next_token: str | None = None
    data: list[Spo2Datum] = Field(default_factory=list)


class TagDatum(OuraModel):
    id: str
    tag_type_code: str | None = None
    start_time: datetime
    end_time: datetime | None = None
    start_day: date
    end_day: date | None = None
    comment: str | None = None
    custom_name: str | None = None


class TagSummary(OuraModel):
    next_token: str | None = None
    data: list[TagDatum] = Field(default_factory=list)


class RestModeEpisodes(OuraModel):
    tags: list[str]
    timestamp: datetime


class RestModePeriodDatum(OuraModel):
    id: str
    end_day: date | None = None
    end_time: datetime | None = None
    episodes: list[RestModeEpisodes]
    start_day: date
    start_time: datetime | None = None


class RestModePeriodSummary(OuraModel):
    next_token: str | None = None
    data: list[RestModePeriodDatum] = Field(default_factory=list)


class SessionMeasureInfo(OuraModel):
    interval: float
    items: list[float | None]
    timestamp: datetime


class SessionDatum(OuraModel):
    id: str
    day: date
    start_datetime: datetime
    end_datetime: datetime
    type: MomentType
    heart_rate: SessionMeasureInfo | None = None
    heart_rate_variability: SessionMeasureInfo | None = None
    mood: MomentMood | None = None
    motion_count: SessionMeasureInfo | None = None


class SessionData(OuraModel):
    next_token: str | None = None
    data: list[SessionDatum] = Field(default_factory=list)


class SleepDetailDatum(OuraModel):
    id: str
    average_breath: float | None = None
    average_heart_rate: float | None = None
    average_hrv: int | None = None
    awake_time: int | None = None
    bedtime_end: datetime
    bedtime_start: datetime
    day: date
    deep_sleep_duration: int | None = None
    efficiency: int | None = None
    heart_rate: SessionMeasureInfo | None = None
    hrv: SessionMeasureInfo | None = None
    latency: int | None = None
    light_sleep_duration: int | None = None
    low_battery_alert: bool
    lowest_heart_rate: int | None = None
    movement_30_sec: str | None = None
    period: int
    readiness: Readiness | None = None
    readiness_score_delta: int | None = None
    rem_sleep_duration: int | None = None
    restless_periods: int | None = None
    sleep_algorithm_version: SleepAlgorithmVersion | None = None
    sleep_analysis_reason: SleepAnalysisReason | None = None
    sleep_phase_30_sec: str | None = None
    sleep_phase_5_min: str | None = None
    sleep_score_delta: int | None = None
    time_in_bed: int
    total_sleep_duration: int | None = None
    type: SleepType | None = None
    ring_id: str | None = None
    app_sleep_phase_5_min: str | None = None


class SleepDetailData(OuraModel):
    next_token: str | None = None
    data: list[SleepDetailDatum] = Field(default_factory=list)


class SleepTimeWindow(OuraModel):
    day_tz: int
    end_offset: int
    start_offset: int


class SleepTimeDatum(OuraModel):
    id: str
    day: date
    optimal_bedtime: SleepTimeWindow | None = None
    recommendation: SleepTimeRecommendation | None = None
    status: SleepTimeStatus | None = None


class SleepTimeData(OuraModel):
    next_token: str | None = None
    data: list[SleepTimeDatum] = Field(default_factory=list)


class VO2MaxDatum(OuraModel):
    id: str
    day: date
    timestamp: datetime
    vo2_max: int


class VO2MaxData(OuraModel):
    next_token: str | None = None
    data: list[VO2MaxDatum] = Field(default_factory=list)


class WorkoutDatum(OuraModel):
    id: str
    activity: str
    calories: float | None = None
    day: date
    distance: float | None = None
    end_datetime: datetime
    intensity: WorkoutIntensity
    label: str | None = None
    source: WorkoutSource
    start_datetime: datetime


class WorkoutData(OuraModel):
    next_token: str | None = None
    data: list[WorkoutDatum] = Field(default_factory=list)


class DailyCardiovascularAgeDatum(OuraModel):
    id: str
    day: date
    pulse_wave_velocity: float | None = None
    vascular_age: int | None = None


class DailyCardiovascularAgeData(OuraModel):
    next_token: str | None = None
    data: list[DailyCardiovascularAgeDatum] = Field(default_factory=list)


class RingBatteryLevelDatum(OuraModel):
    timestamp: datetime
    timestamp_unix: int
    charging: bool | None = None
    in_charger: bool | None = None
    level: int


class RingBatteryLevelData(OuraModel):
    next_token: str | None = None
    data: list[RingBatteryLevelDatum] = Field(default_factory=list)


class BasicTagDatum(OuraModel):
    id: str
    day: date
    text: str | None = None
    timestamp: datetime
    tags: list[str]


class BasicTagData(OuraModel):
    next_token: str | None = None
    data: list[BasicTagDatum] = Field(default_factory=list)


WebhookOperation = Literal["create", "update", "delete"]
WebhookDataType = Literal[
    "tag",
    "enhanced_tag",
    "workout",
    "session",
    "sleep",
    "daily_sleep",
    "daily_readiness",
    "daily_activity",
    "daily_spo2",
    "sleep_time",
    "rest_mode_period",
    "ring_configuration",
    "daily_stress",
    "daily_cardiovascular_age",
    "daily_resilience",
    "vo2_max",
    "meal",
]


class WebhookSubscriptionModel(OuraModel):
    id: str
    callback_url: str
    event_type: WebhookOperation
    data_type: WebhookDataType
    expiration_time: str


class WebhookSubscriptions(OuraModel):
    data: list[WebhookSubscriptionModel] = Field(default_factory=list)
    next_token: str | None = None
