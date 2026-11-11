from time import perf_counter
from typing import Any

from matplotlib import pyplot as plt
from sqlalchemy.orm import Session

from app.experiments.base import BaseExperimentRunner
from app.features.forecasting import (
    FORECAST_FEATURES,
    TARGET,
    create_forecasting_features,
)
from app.ml.forecasting.pipeline import train_forecasting_pipeline
from app.ml.plots import (
    actual_vs_predicted,
    error_distribution,
    feature_importance_plot,
    forecasting_timeseries,
)
from app.models.entities import ExperimentRecord, ModelRecord
from app.schemas.experiments import ForecastExperimentCreate
from app.services.artifacts import ArtifactManager
from app.services.datasets import DatasetService
from app.utils.hashing import sha256_json


class ForecastingExperimentRunner(BaseExperimentRunner):
    experiment_type = "forecasting"
    model_type = "HistGradientBoostingRegressor"

    def __init__(
        self,
        session: Session,
        dataset_service: DatasetService,
        artifact_manager: ArtifactManager,
    ) -> None:
        super().__init__(session, artifact_manager)
        self.dataset_service = dataset_service

    def run(self, request: ForecastExperimentCreate) -> tuple[ExperimentRecord, ModelRecord]:
        dataset = self.dataset_service.get(request.dataset_id)
        if dataset.dataset_type != "renewable":
            raise ValueError("forecasting requires a renewable dataset")
        model_config = request.model.model_dump(exclude={"type"})
        split_config = request.split.model_dump()
        experiment = self.start(
            name=request.name,
            dataset=dataset,
            random_seed=request.random_seed,
            model_parameters={**model_config, "random_state": request.random_seed},
            feature_config={
                "features": FORECAST_FEATURES,
                "target": TARGET,
                "split": split_config,
            },
        )
        try:
            frame = create_forecasting_features(self.dataset_service.load_frame(dataset))
            started = perf_counter()
            result = train_forecasting_pipeline(
                frame,
                model_config,
                train_ratio=request.split.train,
                validation_ratio=request.split.validation,
                random_seed=request.random_seed,
            )
            training_duration = perf_counter() - started
            directory = self.artifact_manager.experiment_dir(self.experiment_type, experiment.id)
            figures = {
                "actual_vs_predicted.png": actual_vs_predicted(
                    result.actual,
                    result.predicted,
                    "Renewable generation: actual vs forecast",
                ),
                "prediction_timeseries.png": forecasting_timeseries(
                    result.actual, result.predicted
                ),
                "error_distribution.png": error_distribution(
                    result.predicted - result.actual, "Forecast error distribution"
                ),
                "feature_importance.png": feature_importance_plot(
                    FORECAST_FEATURES, result.feature_importances
                ),
            }
            for filename, figure in figures.items():
                self.artifact_manager.save_figure(directory, filename, figure)
                plt.close(figure)
            model_path, model_hash = self.artifact_manager.save_model(directory, result.pipeline)
            performance: dict[str, Any] = {
                "training_duration_seconds": training_duration,
                "dataset_rows": len(frame),
                "feature_count": len(FORECAST_FEATURES),
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
                "split": split_config,
            }
            metadata = {
                "model_type": self.model_type,
                "experiment_id": experiment.id,
                "dataset_id": dataset.id,
                "dataset_version": dataset.version,
                "random_seed": request.random_seed,
                "features": FORECAST_FEATURES,
                "target": TARGET,
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
                model_name="renewable-generation-forecast",
                feature_names=FORECAST_FEATURES,
                target_names=[TARGET],
            )
        except Exception as error:
            self.fail(experiment, error)
            raise
