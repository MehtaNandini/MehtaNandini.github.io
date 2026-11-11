from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.entities import (
    DatasetRecord,
    ExperimentRecord,
    InferenceRun,
    ModelRecord,
)
from app.models.enums import ExperimentStatus


def platform_stats(session: Session) -> dict[str, Any]:
    def count(model: Any, *conditions: Any) -> int:
        return int(
            session.scalar(select(func.count()).select_from(model).where(*conditions))
            or 0
        )

    active_forecast = session.scalar(
        select(ModelRecord.id).where(
            ModelRecord.task_type == "forecasting", ModelRecord.active.is_(True)
        )
    )
    active_state = session.scalar(
        select(ModelRecord.id).where(
            ModelRecord.task_type == "state_estimation", ModelRecord.active.is_(True)
        )
    )
    return {
        "datasets_count": count(DatasetRecord),
        "experiments_count": count(ExperimentRecord),
        "completed_experiments": count(
            ExperimentRecord,
            ExperimentRecord.status == ExperimentStatus.COMPLETED.value,
        ),
        "failed_experiments": count(
            ExperimentRecord, ExperimentRecord.status == ExperimentStatus.FAILED.value
        ),
        "forecasting_models": count(
            ModelRecord, ModelRecord.task_type == "forecasting"
        ),
        "state_estimation_models": count(
            ModelRecord, ModelRecord.task_type == "state_estimation"
        ),
        "total_inference_requests": count(InferenceRun),
        "active_forecasting_model": active_forecast,
        "active_state_estimation_model": active_state,
    }
