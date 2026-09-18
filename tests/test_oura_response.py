import pytest

from oura_py.data import models
from oura_py.data.response import OuraResponse


@pytest.fixture()
def oura_response_data() -> OuraResponse[models.DailySleep]:
    return OuraResponse(
        data=[
            {
                "id": "testing-id",
                "contributors": {
                    "deep_sleep": 80,
                    "efficiency": 80,
                    "latency": 15,
                    "rem_sleep": 40,
                    "restfulness": 65,
                    "timing": 70,
                    "total_sleep": 95,
                },
                "day": "2026-01-01",
                "score": 85,
                "timestamp": "2025-01-01T08:00:00Z",
            }
        ],
        model_type=models.DailySleep,
        metadata={"endpoint": "daily_sleep"},
    )


def test_raw_representation(oura_response_data):

    raw = oura_response_data.raw()

    assert isinstance(raw, list)
    assert isinstance(raw[0], dict)
    assert raw[0]["day"] == "2026-01-01"
    assert raw[0]["contributors"]["total_sleep"] == 95


def test_model_representation(oura_response_data):

    model = oura_response_data.model()

    assert isinstance(model, list)
    assert isinstance(model[0], models.DailySleep)
    assert isinstance(model[0].contributors, models.DailySleepContributors)
    assert model[0].day == "2026-01-01"
    assert model[0].contributors.total_sleep == 95


def test_dataframe_representation(oura_response_data):

    with pytest.raises(NotImplementedError):
        oura_response_data.to_polars()

    with pytest.raises(NotImplementedError):
        oura_response_data.to_pandas()


def test_model_caching(oura_response_data):

    first = oura_response_data.model()
    second = oura_response_data.model()

    assert first is second
