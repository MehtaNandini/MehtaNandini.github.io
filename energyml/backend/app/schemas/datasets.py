from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class RenewableDatasetCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)

    name: str = Field(default="Annual renewable generation", min_length=1, max_length=120)
    start_date: str = "2025-01-01"
    number_of_days: int = Field(default=365, ge=2, le=3650)
    solar_capacity_mw: float = Field(default=60.0, gt=0, le=10_000)
    wind_capacity_mw: float = Field(default=40.0, gt=0, le=10_000)
    noise_level: float = Field(default=0.04, ge=0, le=0.5)
    random_seed: int = Field(default=42, ge=0, le=2**32 - 1)


class StateDatasetCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)

    name: str = Field(default="Synthetic distribution network", min_length=1, max_length=120)
    network_size: int = Field(default=5, ge=2, le=50)
    number_of_samples: int = Field(default=5_000, ge=50, le=1_000_000)
    measurement_noise_std: float = Field(default=0.005, ge=0, le=0.1)
    random_seed: int = Field(default=42, ge=0, le=2**32 - 1)


class DatasetView(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    dataset_type: str
    version: str
    random_seed: int
    generation_config_json: dict[str, Any]
    row_count: int
    file_path: str
    file_hash: str
    created_at: datetime
