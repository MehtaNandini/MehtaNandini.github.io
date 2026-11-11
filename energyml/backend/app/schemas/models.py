from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class ModelView(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    experiment_id: str
    task_type: str
    model_name: str
    model_type: str
    version: str
    artifact_path: str
    artifact_hash: str
    metrics_json: dict[str, Any]
    feature_names_json: list[str]
    target_names_json: list[str]
    created_at: datetime
    active: bool
