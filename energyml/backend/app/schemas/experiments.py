from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ForecastModelConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)

    type: Literal["HistGradientBoostingRegressor"] = "HistGradientBoostingRegressor"
    learning_rate: float = Field(default=0.08, gt=0, le=1)
    max_iter: int = Field(default=250, ge=10, le=5000)
    max_depth: int | None = Field(default=8, ge=1, le=100)
    min_samples_leaf: int = Field(default=20, ge=1, le=10_000)


class SplitConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)

    train: float = Field(default=0.7, gt=0, lt=1)
    validation: float = Field(default=0.15, ge=0, lt=1)
    test: float = Field(default=0.15, gt=0, lt=1)

    @model_validator(mode="after")
    def sum_to_one(self) -> "SplitConfig":
        if abs(self.train + self.validation + self.test - 1.0) > 1e-9:
            raise ValueError("train, validation and test ratios must sum to 1")
        return self


class ForecastExperimentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    dataset_id: str
    name: str = Field(
        default="Renewable generation forecast", min_length=1, max_length=160
    )
    random_seed: int = Field(default=42, ge=0, le=2**32 - 1)
    model: ForecastModelConfig = Field(default_factory=ForecastModelConfig)
    split: SplitConfig = Field(default_factory=SplitConfig)


class StateModelConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)

    type: Literal["RandomForestRegressor"] = "RandomForestRegressor"
    n_estimators: int = Field(default=200, ge=10, le=5000)
    max_depth: int | None = Field(default=16, ge=1, le=100)
    min_samples_split: int = Field(default=2, ge=2, le=1000)
    min_samples_leaf: int = Field(default=1, ge=1, le=1000)
    max_features: float | Literal["sqrt", "log2"] = 1.0
    n_jobs: int = Field(default=1, ge=-1, le=128)


class StateExperimentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)

    dataset_id: str
    name: str = Field(default="Voltage state estimation", min_length=1, max_length=160)
    random_seed: int = Field(default=42, ge=0, le=2**32 - 1)
    test_ratio: float = Field(default=0.2, ge=0.05, le=0.5)
    model: StateModelConfig = Field(default_factory=StateModelConfig)


class ExperimentView(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    experiment_type: str
    dataset_id: str
    dataset_version: str
    model_type: str
    model_parameters_json: dict[str, Any]
    feature_config_json: dict[str, Any]
    random_seed: int
    status: str
    started_at: datetime | None
    completed_at: datetime | None
    metrics_json: dict[str, Any] | None
    performance_json: dict[str, Any] | None
    artifact_directory: str | None
    artifact_hash: str | None
    code_version: str | None
    error_message: str | None
    created_at: datetime
