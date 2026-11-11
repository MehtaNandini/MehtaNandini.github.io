import numpy as np

from app.datasets.renewable import RenewableDatasetConfig, generate_renewable_dataset
from app.datasets.state_estimation import StateDatasetConfig, generate_state_dataset
from app.features.forecasting import FORECAST_FEATURES, create_forecasting_features
from app.ml.forecasting.pipeline import train_forecasting_pipeline
from app.ml.metrics import regression_metrics
from app.ml.state_estimation.pipeline import train_state_pipeline


def test_regression_metrics_are_calculated() -> None:
    actual = np.array([1.0, 2.0, 3.0])
    predicted = np.array([1.0, 2.5, 2.5])
    metrics = regression_metrics(actual, predicted)
    assert metrics["mae"] == 1 / 3
    assert 0 < metrics["rmse"] < 1
    assert metrics["r2"] < 1
    assert metrics["mape_percent"] > 0


def test_forecasting_training_prediction_baseline_and_reproducibility() -> None:
    frame = create_forecasting_features(
        generate_renewable_dataset(RenewableDatasetConfig(number_of_days=60, random_seed=42))
    )
    parameters = {"max_iter": 40, "max_depth": 5, "min_samples_leaf": 10}
    first = train_forecasting_pipeline(frame, parameters, random_seed=42)
    second = train_forecasting_pipeline(frame, parameters, random_seed=42)
    np.testing.assert_allclose(first.predicted, second.predicted)
    assert first.predicted.shape == first.actual.shape
    assert set(first.metrics) == {
        "model",
        "persistence_baseline",
        "improvement_over_baseline",
    }
    assert first.feature_importances.shape == (len(FORECAST_FEATURES),)
    assert np.isfinite(first.metrics["model"]["rmse"])


def test_state_estimation_training_multi_output_and_per_bus_metrics() -> None:
    frame = generate_state_dataset(
        StateDatasetConfig(network_size=4, number_of_samples=350, random_seed=42)
    )
    result = train_state_pipeline(frame, {"n_estimators": 30, "max_depth": 8}, random_seed=42)
    assert result.predicted.shape[1] == 4
    assert result.predicted.shape == result.actual.shape
    assert len(result.metrics["per_bus"]) == 4
    assert result.metrics["aggregate"]["mae"] < 0.02
