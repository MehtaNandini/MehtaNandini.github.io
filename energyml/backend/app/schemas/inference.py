from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ForecastInferenceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)

    model_id: str | None = None
    solar_irradiance: float = Field(ge=0, le=1500)
    temperature_c: float = Field(ge=-80, le=80)
    wind_speed_mps: float = Field(ge=0, le=80)
    humidity_percent: float = Field(ge=0, le=100)
    cloud_cover_percent: float = Field(ge=0, le=100)
    hour: int = Field(ge=0, le=23)
    day_of_week: int = Field(ge=0, le=6)
    month: int = Field(ge=1, le=12)
    day_of_year: int = Field(ge=1, le=366)
    generation_lag_1: float = Field(ge=0, le=100_000)
    generation_lag_3: float = Field(ge=0, le=100_000)
    generation_lag_6: float = Field(ge=0, le=100_000)
    generation_lag_24: float = Field(ge=0, le=100_000)
    generation_rolling_mean_3: float = Field(ge=0, le=100_000)
    generation_rolling_mean_6: float = Field(ge=0, le=100_000)
    generation_rolling_mean_24: float = Field(ge=0, le=100_000)


class ForecastInferenceResponse(BaseModel):
    prediction: float
    unit: str = "MW"
    model_id: str
    model_version: str
    experiment_id: str
    prediction_timestamp: datetime


class StateInferenceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)

    model_id: str | None = None
    measurements: dict[str, float]


class StateInferenceResponse(BaseModel):
    voltages: dict[str, float]
    unit: str = "p.u."
    model_id: str
    model_version: str
    experiment_id: str
    prediction_timestamp: datetime
