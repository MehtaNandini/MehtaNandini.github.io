import os
import subprocess
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.entities import DatasetRecord, ExperimentRecord, ModelRecord
from app.models.enums import ExperimentStatus
from app.services.artifacts import ArtifactManager


def code_version() -> str | None:
    configured = os.getenv("GIT_COMMIT")
    if configured:
        return configured[:80]
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


class BaseExperimentRunner:
    """Shared, transaction-backed experiment lifecycle."""

    experiment_type: str
    model_type: str

    def __init__(self, session: Session, artifact_manager: ArtifactManager) -> None:
        self.session = session
        self.artifact_manager = artifact_manager

    def start(
        self,
        *,
        name: str,
        dataset: DatasetRecord,
        random_seed: int,
        model_parameters: dict[str, Any],
        feature_config: dict[str, Any],
    ) -> ExperimentRecord:
        experiment = ExperimentRecord(
            id=str(uuid4()),
            name=name,
            experiment_type=self.experiment_type,
            dataset_id=dataset.id,
            dataset_version=dataset.version,
            model_type=self.model_type,
            model_parameters_json=model_parameters,
            feature_config_json=feature_config,
            random_seed=random_seed,
            status=ExperimentStatus.PENDING.value,
            code_version=code_version(),
        )
        self.session.add(experiment)
        self.session.commit()
        experiment.status = ExperimentStatus.RUNNING.value
        experiment.started_at = datetime.now(UTC)
        self.session.commit()
        return experiment

    def complete(
        self,
        experiment: ExperimentRecord,
        *,
        metrics: dict[str, Any],
        performance: dict[str, Any],
        artifact_directory: str,
        artifact_hash: str,
        model_path: str,
        model_hash: str,
        model_name: str,
        feature_names: list[str],
        target_names: list[str],
    ) -> tuple[ExperimentRecord, ModelRecord]:
        experiment.status = ExperimentStatus.COMPLETED.value
        experiment.completed_at = datetime.now(UTC)
        experiment.metrics_json = metrics
        experiment.performance_json = performance
        experiment.artifact_directory = artifact_directory
        experiment.artifact_hash = artifact_hash
        model = ModelRecord(
            id=str(uuid4()),
            experiment_id=experiment.id,
            task_type=self.experiment_type,
            model_name=model_name,
            model_type=self.model_type,
            version="1.0.0",
            artifact_path=model_path,
            artifact_hash=model_hash,
            metrics_json=metrics,
            feature_names_json=feature_names,
            target_names_json=target_names,
            active=False,
        )
        self.session.add(model)
        self.session.commit()
        self.session.refresh(experiment)
        self.session.refresh(model)
        return experiment, model

    def fail(self, experiment: ExperimentRecord, error: Exception) -> None:
        self.session.rollback()
        current = self.session.get(ExperimentRecord, experiment.id)
        if current is not None:
            current.status = ExperimentStatus.FAILED.value
            current.completed_at = datetime.now(UTC)
            current.error_message = f"{type(error).__name__}: {error}"[:1000]
            self.session.commit()
