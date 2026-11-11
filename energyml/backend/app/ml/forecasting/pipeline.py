from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from numpy.typing import NDArray
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from app.features.forecasting import FORECAST_FEATURES, TARGET, chronological_split
from app.ml.metrics import regression_metrics


@dataclass
class ForecastTrainingResult:
    pipeline: Pipeline
    actual: NDArray[np.float64]
    predicted: NDArray[np.float64]
    metrics: dict[str, Any]
    feature_importances: NDArray[np.float64]
    test_frame: pd.DataFrame


def train_forecasting_pipeline(
    frame: pd.DataFrame,
    model_parameters: dict[str, Any],
    train_ratio: float = 0.7,
    validation_ratio: float = 0.15,
    random_seed: int = 42,
) -> ForecastTrainingResult:
    split = chronological_split(frame, train_ratio, validation_ratio)
    fit_frame = pd.concat([split.train, split.validation], ignore_index=True)
    defaults: dict[str, Any] = {
        "learning_rate": 0.08,
        "max_iter": 250,
        "max_depth": 8,
        "min_samples_leaf": 20,
        "random_state": random_seed,
    }
    defaults.update(model_parameters)
    pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scale", StandardScaler()),
            ("model", HistGradientBoostingRegressor(**defaults)),
        ]
    )
    pipeline.fit(fit_frame[FORECAST_FEATURES], fit_frame[TARGET])
    actual = split.test[TARGET].to_numpy(dtype=float)
    predicted = np.asarray(pipeline.predict(split.test[FORECAST_FEATURES]), dtype=float)
    model_metrics = regression_metrics(actual, predicted)
    baseline = split.test["generation_lag_24"].to_numpy(dtype=float)
    baseline_metrics = regression_metrics(actual, baseline)
    sample = split.test.iloc[: min(600, len(split.test))]
    importance = permutation_importance(
        pipeline,
        sample[FORECAST_FEATURES],
        sample[TARGET],
        n_repeats=3,
        random_state=random_seed,
        scoring="neg_mean_absolute_error",
    ).importances_mean
    return ForecastTrainingResult(
        pipeline=pipeline,
        actual=actual,
        predicted=predicted,
        metrics={
            "model": model_metrics,
            "persistence_baseline": baseline_metrics,
            "improvement_over_baseline": {
                "mae_percent": float(
                    (baseline_metrics["mae"] - model_metrics["mae"]) / baseline_metrics["mae"] * 100
                ),
                "rmse_percent": float(
                    (baseline_metrics["rmse"] - model_metrics["rmse"])
                    / baseline_metrics["rmse"]
                    * 100
                ),
            },
        },
        feature_importances=np.asarray(importance, dtype=float),
        test_frame=split.test,
    )
