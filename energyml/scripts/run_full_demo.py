import json
from pathlib import Path
from typing import Any

from _common import services

from app.experiments.forecasting import ForecastingExperimentRunner
from app.experiments.state_estimation import StateEstimationExperimentRunner
from app.features.forecasting import FORECAST_FEATURES, create_forecasting_features
from app.features.state_estimation import state_feature_target_columns
from app.schemas.datasets import RenewableDatasetCreate, StateDatasetCreate
from app.schemas.experiments import ForecastExperimentCreate, StateExperimentCreate
from app.schemas.inference import ForecastInferenceRequest, StateInferenceRequest
from app.services.inference import InferenceService
from app.services.models import ModelService


def run_demo() -> dict[str, Any]:
    session, datasets, artifacts = services()
    try:
        renewable = datasets.generate_renewable(RenewableDatasetCreate(random_seed=42))
        forecast_experiment, forecast_model = ForecastingExperimentRunner(
            session, datasets, artifacts
        ).run(ForecastExperimentCreate(dataset_id=renewable.id, random_seed=42))
        models = ModelService(session)
        models.activate(forecast_model.id)
        forecast_frame = create_forecasting_features(datasets.load_frame(renewable))
        forecast_values = {name: float(forecast_frame.iloc[-1][name]) for name in FORECAST_FEATURES}
        inference = InferenceService(session, models, artifacts)
        forecast_prediction = inference.forecast(ForecastInferenceRequest(**forecast_values))

        state_dataset = datasets.generate_state(StateDatasetCreate(random_seed=42))
        state_experiment, state_model = StateEstimationExperimentRunner(
            session, datasets, artifacts
        ).run(StateExperimentCreate(dataset_id=state_dataset.id, random_seed=42))
        models.activate(state_model.id)
        state_frame = datasets.load_frame(state_dataset)
        state_features, _ = state_feature_target_columns(list(state_frame.columns))
        measurements = {name: float(state_frame.iloc[-1][name]) for name in state_features}
        state_prediction = inference.state_estimation(
            StateInferenceRequest(measurements=measurements)
        )
        return {
            "seed": 42,
            "renewable_dataset": {
                "id": renewable.id,
                "version": renewable.version,
                "rows": renewable.row_count,
                "sha256": renewable.file_hash,
            },
            "forecasting": {
                "experiment_id": forecast_experiment.id,
                "model_id": forecast_model.id,
                "metrics": forecast_experiment.metrics_json,
                "sample_inference": forecast_prediction,
            },
            "state_dataset": {
                "id": state_dataset.id,
                "version": state_dataset.version,
                "rows": state_dataset.row_count,
                "sha256": state_dataset.file_hash,
            },
            "state_estimation": {
                "experiment_id": state_experiment.id,
                "model_id": state_model.id,
                "metrics": state_experiment.metrics_json,
                "sample_inference": state_prediction,
            },
        }
    finally:
        session.close()


def main() -> None:
    results = run_demo()
    output = Path(__file__).parents[1] / "docs" / "demo_results.json"
    output.write_text(json.dumps(results, indent=2, default=str) + "\n")
    print(json.dumps(results, indent=2, default=str))
    print(f"\nVerified results written to {output}")


if __name__ == "__main__":
    main()
