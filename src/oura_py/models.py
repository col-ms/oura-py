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


class Spo2Datum:
    def __init__(
        self,
        id: str,
        day: datetime,
        spo2_percentage: float,
        breathing_disturbance_index: int,
    ) -> None:
        self.id = id
        self.day = day
        self.spo2_percentage_avg = spo2_percentage["average"]
        self.breathing_disturbance_index = breathing_disturbance_index


class Spo2Summary:
    def __init__(
        self,
        data: List[Spo2Datum],
        next_token: str | None = None,
    ) -> None:
        self.data = [Spo2Datum(**d) for d in data] if data else []
        self.next_token = next_token


class TagDatum:
    def __init__(
        self,
        id: str,
        tag_type_code: str,
        start_time: datetime,
        end_time: datetime | None,
        start_day: datetime,
        end_day: datetime,
        comment: str,
        custom_name: str,
    ) -> None:
        self.id = id
        self.tag_type_code = tag_type_code
        self.start_time = start_time
        self.end_time = end_time
        self.start_day = start_day
        self.end_day = end_day
        self.comment = comment
        self.custom_name = custom_name


class TagSummary:
    def __init__(
        self,
        data: List[TagDatum],
        next_token: str | None,
    ) -> None:
        self.data = [TagDatum(**d) for d in data] if data else []
        self.next_token = next_token


class RestModeEpisodes:
    def __init__(self, tags: List[str], timestamp: datetime) -> None:
        self.tags = tags
        self.timestamp = timestamp


class RestModePeriodDatum:
    def __init__(
        self,
        id: str,
        end_day: datetime,
        end_time: datetime,
        episodes: RestModeEpisodes,
        start_day: datetime,
        start_time: datetime,
    ) -> None:
        self.id = id
        self.end_day = end_day
        self.end_time = end_time
        self.episodes = RestModeEpisodes(**episodes[0])
        self.start_day = start_day
        self.start_time = start_time


class RestModePeriodSummary:
    def __init__(self, data: List[RestModePeriodDatum], next_token: str | None) -> None:
        self.data = [RestModePeriodDatum(**d) for d in data] if data else []
        self.next_token = next_token


class SessionMeasureInfo:
    def __init__(
        self,
        interval: int,
        items: List[float | None],
        timestamp: datetime,
    ) -> None:
        self.interval = interval
        self.items = items
        self.timestamp = timestamp


class SessionDatum:
    def __init__(
        self,
        id: str,
        day: datetime,
        start_datetime: datetime,
        end_datetime: datetime,
        type: str,
        heart_rate: SessionMeasureInfo,
        heart_rate_variability: SessionMeasureInfo,
        mood: str,
        motion_count: SessionMeasureInfo,
    ) -> None:
        self.id = id
        self.day = day
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.type = type
        self.heart_rate = SessionMeasureInfo(**heart_rate)
        self.heart_rate_variability = SessionMeasureInfo(**heart_rate_variability)
        self.mood = mood
        self.motion_count = SessionMeasureInfo(**motion_count)


class SessionData:
    def __init__(
        self,
        data: List[SessionDatum],
        next_token: str | None,
    ) -> None:
        self.data = [SessionDatum(**d) for d in data] if data else []
        self.next_token = next_token


class SleepDetailDatum:
    def __init__(
        self,
        id: str,
        average_breath: float,
        average_heart_rate: float,
        average_hrv: int,
        awake_time: int,
        bedtime_end: datetime,
        bedtime_start: datetime,
        day: datetime,
        deep_sleep_duration: int,
        efficiency: int,
        heart_rate: SessionMeasureInfo,
        hrv: SessionMeasureInfo,
        latency: int,
        light_sleep_duration: int,
        low_battery_alert: bool,
        lowest_heart_rate: int,
        movement_30_sec: str,
        period: int,
        readiness: ReadinessSummaryDatum,
        readiness_score_delta: int,
        rem_sleep_duration: int,
        restless_periods: int,
        sleep_phase_5_min: str,
        sleep_score_delta: int,
        sleep_algorithm_version: str,
        time_in_bed: int,
        total_sleep_duration: int,
        type: str,
    ) -> None:
        self.id = id
        self.avaverage_breath = average_breath
        self.avaverage_heart_rate = average_heart_rate
        self.average_hrv = average_hrv
        self.awake_time = awake_time
        self.bedtime_end = bedtime_end
        self.bedtime_start = bedtime_start
        self.day = day
        self.deep_sleep_duration = deep_sleep_duration
        self.efficiency = efficiency
        self.heart_rate = SessionMeasureInfo(**heart_rate)
        self.hrv = SessionMeasureInfo(**hrv)
        self.latency = latency
        self.light_sleep_duration = light_sleep_duration
        self.low_battery_alert = low_battery_alert
        self.lowest_heart_rate = lowest_heart_rate
        self.movement_30_sec = movement_30_sec
        self.period = period
        self.readiness = ReadinessSummaryDatum(
            **readiness, id=None, timestamp=bedtime_start, day=day
        )
        self.readiness_score_delta = readiness_score_delta
        self.rem_sleep_duration = rem_sleep_duration
        self.restless_periods = restless_periods
        self.sleep_phase_5_min = sleep_phase_5_min
        self.sleep_score_delta = sleep_score_delta
        self.sleep_algorithm_version = sleep_algorithm_version
        self.time_in_bed = time_in_bed
        self.total_sleep_duration = total_sleep_duration
        self.type = type


class SleepDetailData:
    def __init__(
        self,
        data: List[SleepDetailDatum],
        next_token: str | None,
    ) -> None:
        self.data = [SleepDetailDatum(**d) for d in data] if data else []
        self.next_token = next_token


class SleepTimeWindow:
    def __init__(self, day_tz: int, end_offset: int, start_offset: int) -> None:
        self.day_tz = day_tz
        self.end_offset = end_offset
        self.start_offset = start_offset


class SleepTimeDatum:
    def __init__(
        self,
        id: str,
        day: str,
        optimal_bedtime: SleepTimeWindow | None,
        recommendation: str,
        status: str,
    ) -> None:
        self.id = id
        self.day = day
        self.optimal_bedtime = (
            SleepTimeWindow(**optimal_bedtime) if optimal_bedtime else None
        )
        self.recommendation = recommendation
        self.status = status


class SleepTimeData:
    def __init__(
        self,
        data: List[SleepTimeDatum],
        next_token: str | None,
    ) -> None:
        self.data = [SleepTimeDatum(**d) for d in data] if data else []
        self.next_token = next_token


class VO2MaxDatum:
    def __init__(
        self,
        id: str,
        day: datetime,
        timestamp: datetime,
        vo2_max: int,
    ) -> None:
        self.id = id
        self.day = day
        self.timestamp = timestamp
        self.vo2_max = vo2_max


class VO2MaxData:
    def __init__(
        self,
        data: List[VO2MaxDatum],
        next_token: str | None,
    ) -> None:
        self.data = [VO2MaxDatum(**d) for d in data] if data else []
        self.next_token = next_token


class WorkoutDatum:
    def __init__(
        self,
        id: str,
        activity: str,
        calories: float,
        day: datetime,
        distance: float,
        end_datetime: datetime,
        intensity: str,
        label: str,
        source: str,
        start_datetime: datetime,
    ) -> None:
        self.id = id
        self.activity = activity
        self.calories = calories
        self.day = day
        self.distance = distance
        self.end_datetime = end_datetime
        self.intensity = intensity
        self.label = label
        self.source = source
        self.start_datetime = start_datetime


class WorkoutData:
    def __init__(
        self,
        data: List[WorkoutDatum],
        next_token: str | None,
    ) -> None:
        self.data = [WorkoutDatum(**d) for d in data] if data else []
        self.next_token = next_token
