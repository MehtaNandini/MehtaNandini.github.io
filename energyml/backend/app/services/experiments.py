from pathlib import Path
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entities import ExperimentRecord
from app.services.artifacts import ArtifactManager


class ExperimentService:
    def __init__(self, session: Session, artifact_manager: ArtifactManager) -> None:
        self.session = session
        self.artifact_manager = artifact_manager

    def list_all(self) -> list[ExperimentRecord]:
        return list(
            self.session.scalars(
                select(ExperimentRecord).order_by(ExperimentRecord.created_at.desc())
            )
        )

    def get(self, experiment_id: str) -> ExperimentRecord:
        experiment = self.session.get(ExperimentRecord, experiment_id)
        if experiment is None:
            raise LookupError("experiment not found")
        return experiment

    def metrics(self, experiment_id: str) -> dict[str, Any]:
        experiment = self.get(experiment_id)
        return experiment.metrics_json or {}

    def artifacts(self, experiment_id: str) -> list[dict[str, Any]]:
        experiment = self.get(experiment_id)
        if not experiment.artifact_directory:
            return []
        return self.artifact_manager.manifest(Path(experiment.artifact_directory))

    def compare(self, experiment_ids: list[str]) -> list[dict[str, Any]]:
        if not 2 <= len(experiment_ids) <= 20:
            raise ValueError("compare requires between 2 and 20 experiment IDs")
        comparisons = []
        for experiment_id in experiment_ids:
            experiment = self.get(experiment_id)
            metrics = experiment.metrics_json or {}
            primary = metrics.get("model", metrics.get("aggregate", {}))
            performance = experiment.performance_json or {}
            comparisons.append(
                {
                    "experiment_id": experiment.id,
                    "name": experiment.name,
                    "experiment_type": experiment.experiment_type,
                    "model_type": experiment.model_type,
                    "model_parameters": experiment.model_parameters_json,
                    "dataset_version": experiment.dataset_version,
                    "random_seed": experiment.random_seed,
                    "mae": primary.get("mae"),
                    "rmse": primary.get("rmse"),
                    "r2": primary.get("r2"),
                    "training_duration_seconds": performance.get(
                        "training_duration_seconds"
                    ),
                    "artifact_version": experiment.artifact_hash,
                }
            )
        return comparisons
