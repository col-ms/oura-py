from datetime import datetime

import pytest
from pydantic import ValidationError

from oura_py.data import models
from oura_py.data.response import Result


def test_good_result(result_data):
    result = Result(**result_data)
    assert result.status_code == 200
    assert result.message == "OK"
    assert result.data == {"key": "value"}


def test_bad_result(result_data):
    result_data["status_code"] = "200"
    with pytest.raises(
        TypeError,
        match=f"status_code must be <class 'int'>, got {type(result_data['status_code'])}",
    ):
        Result(**result_data)


def test_good_personal_info(personal_info_data):
    personal_info = models.PersonalInfo(**personal_info_data)
    assert personal_info.id == "12345"
    assert personal_info.age == 30
    assert personal_info.weight == 70.5
    assert personal_info.height == 175.1
    assert personal_info.biological_sex == "Male"
    assert personal_info.email == "john.smith@example.com"


def test_bad_personal_info(personal_info_data):
    personal_info_data["id"] = 12345
    with pytest.raises(ValidationError):
        models.PersonalInfo(**personal_info_data)


def test_good_ring_config(ring_config_data):
    ring_config = models.RingConfigData(**ring_config_data)
    assert ring_config.id == "12345"
    assert ring_config.color == "glossy_black"
    assert ring_config.design == "horizon"
    assert ring_config.firmware_version == "3.2.2"
    assert ring_config.hardware_type == "gen3"
    assert ring_config.set_up_at == datetime.fromisoformat("2024-12-31T00:00:00+00:00")
    assert ring_config.size == 9


def test_bad_ring_config(ring_config_data):
    ring_config_data["color"] = 12345
    with pytest.raises(ValidationError):
        models.RingConfigData(**ring_config_data)


def test_good_sleep_summary_contributor(sleep_summary_contributor_data):
    sleep_summary_contributor = models.SleepSummaryContributors(
        **sleep_summary_contributor_data
    )
    assert sleep_summary_contributor.deep_sleep == 120
    assert sleep_summary_contributor.efficiency == 85
    assert sleep_summary_contributor.latency == 15
    assert sleep_summary_contributor.rem_sleep == 80
    assert sleep_summary_contributor.restfulness == 5
    assert sleep_summary_contributor.timing == 5
    assert sleep_summary_contributor.total_sleep == 480


def test_bad_sleep_summary_contributor(sleep_summary_contributor_data):
    sleep_summary_contributor_data["deep_sleep"] = []
    with pytest.raises(ValidationError):
        models.SleepSummaryContributors(**sleep_summary_contributor_data)


def test_nested_response_values_are_parsed():
    summary = models.SleepSummary(
        next_token=None,
        data=[
            {
                "id": "sleep-1",
                "contributors": {"deep_sleep": 90},
                "day": "2025-01-01",
                "score": 85,
                "timestamp": "2025-01-01T08:00:00Z",
            }
        ],
    )

    assert isinstance(summary.data[0], models.SleepSummaryDatum)
    assert summary.data[0].day.isoformat() == "2025-01-01"
    assert summary.data[0].timestamp.tzinfo is not None
    assert summary.data[0].contributors.deep_sleep == 90


def test_enum_values_are_validated():
    with pytest.raises(ValidationError):
        models.WorkoutDatum(
            id="workout-1",
            activity="running",
            day="2025-01-01",
            end_datetime="2025-01-01T10:00:00Z",
            intensity="invalid",
            source="manual",
            start_datetime="2025-01-01T09:00:00Z",
        )
