from time import perf_counter
from typing import Any

from matplotlib import pyplot as plt
from sqlalchemy.orm import Session

from app.experiments.base import BaseExperimentRunner
from app.ml.plots import (
    actual_vs_predicted,
    error_distribution,
    feature_importance_plot,
    per_bus_errors,
)
from app.ml.state_estimation.pipeline import train_state_pipeline
from app.models.entities import ExperimentRecord, ModelRecord
from app.schemas.experiments import StateExperimentCreate
from app.services.artifacts import ArtifactManager
from app.services.datasets import DatasetService
from app.utils.hashing import sha256_json


class StateEstimationExperimentRunner(BaseExperimentRunner):
    experiment_type = "state_estimation"
    model_type = "RandomForestRegressor"

    def __init__(
        self,
        session: Session,
        dataset_service: DatasetService,
        artifact_manager: ArtifactManager,
    ) -> None:
        super().__init__(session, artifact_manager)
        self.dataset_service = dataset_service

    def run(self, request: StateExperimentCreate) -> tuple[ExperimentRecord, ModelRecord]:
        dataset = self.dataset_service.get(request.dataset_id)
        if dataset.dataset_type != "state_estimation":
            raise ValueError("state estimation requires a state-estimation dataset")
        model_config = request.model.model_dump(exclude={"type"})
        experiment = self.start(
            name=request.name,
            dataset=dataset,
            random_seed=request.random_seed,
            model_parameters={**model_config, "random_state": request.random_seed},
            feature_config={"test_ratio": request.test_ratio},
        )
        try:
            frame = self.dataset_service.load_frame(dataset)
            started = perf_counter()
            result = train_state_pipeline(
                frame,
                model_config,
                test_ratio=request.test_ratio,
                random_seed=request.random_seed,
            )
            training_duration = perf_counter() - started
            directory = self.artifact_manager.experiment_dir(self.experiment_type, experiment.id)
            bus_mae = [result.metrics["per_bus"][name]["mae"] for name in result.target_names]
            figures = {
                "voltage_estimation.png": actual_vs_predicted(
                    result.actual.ravel(),
                    result.predicted.ravel(),
                    "True vs estimated voltage",
                ),
                "bus_errors.png": per_bus_errors(result.target_names, bus_mae),
                "error_distribution.png": error_distribution(
                    result.predicted - result.actual, "Voltage estimation error"
                ),
                "feature_importance.png": feature_importance_plot(
                    result.feature_names, result.feature_importances
                ),
            }
            for filename, figure in figures.items():
                self.artifact_manager.save_figure(directory, filename, figure)
                plt.close(figure)
            model_path, model_hash = self.artifact_manager.save_model(directory, result.pipeline)
            performance: dict[str, Any] = {
                "training_duration_seconds": training_duration,
                "dataset_rows": len(frame),
                "feature_count": len(result.feature_names),
                "target_count": len(result.target_names),
                "test_rows": len(result.actual),
                "model_size_bytes": model_path.stat().st_size,
            }
            config = {
                "experiment_id": experiment.id,
                "dataset_id": dataset.id,
                "dataset_version": dataset.version,
                "dataset_hash": dataset.file_hash,
                "random_seed": request.random_seed,
                "model": request.model.model_dump(),
                "test_ratio": request.test_ratio,
            }
            metadata = {
                "model_type": self.model_type,
                "experiment_id": experiment.id,
                "dataset_id": dataset.id,
                "dataset_version": dataset.version,
                "random_seed": request.random_seed,
                "features": result.feature_names,
                "targets": result.target_names,
                "metrics": result.metrics,
            }
            self.artifact_manager.save_json(directory, "metrics.json", result.metrics)
            self.artifact_manager.save_json(directory, "config.json", config)
            self.artifact_manager.save_json(directory, "model_metadata.json", metadata)
            artifact_hash = sha256_json(self.artifact_manager.manifest(directory))
            return self.complete(
                experiment,
                metrics=result.metrics,
                performance=performance,
                artifact_directory=str(directory),
                artifact_hash=artifact_hash,
                model_path=str(model_path),
                model_hash=model_hash,
                model_name="voltage-state-estimator",
                feature_names=result.feature_names,
                target_names=result.target_names,
            )
        except Exception as error:
            self.fail(experiment, error)
            raise
