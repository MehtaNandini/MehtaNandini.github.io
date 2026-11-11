from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from numpy.typing import NDArray
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from app.features.state_estimation import state_feature_target_columns
from app.ml.metrics import per_target_metrics, regression_metrics


@dataclass
class StateTrainingResult:
    pipeline: Pipeline
    actual: NDArray[np.float64]
    predicted: NDArray[np.float64]
    metrics: dict[str, Any]
    feature_importances: NDArray[np.float64]
    feature_names: list[str]
    target_names: list[str]


def train_state_pipeline(
    frame: pd.DataFrame,
    model_parameters: dict[str, Any],
    test_ratio: float = 0.2,
    random_seed: int = 42,
) -> StateTrainingResult:
    if not 0.05 <= test_ratio <= 0.5:
        raise ValueError("test_ratio must be between 0.05 and 0.5")
    feature_names, target_names = state_feature_target_columns(list(frame.columns))
    train, test = train_test_split(
        frame, test_size=test_ratio, random_state=random_seed, shuffle=True
    )
    defaults: dict[str, Any] = {
        "n_estimators": 200,
        "max_depth": 16,
        "min_samples_split": 2,
        "min_samples_leaf": 1,
        "max_features": 1.0,
        "random_state": random_seed,
        "n_jobs": 1,
    }
    defaults.update(model_parameters)
    pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("model", RandomForestRegressor(**defaults)),
        ]
    )
    pipeline.fit(train[feature_names], train[target_names])
    actual = test[target_names].to_numpy(dtype=float)
    predicted = np.asarray(pipeline.predict(test[feature_names]), dtype=float)
    forest = pipeline.named_steps["model"]
    return StateTrainingResult(
        pipeline=pipeline,
        actual=actual,
        predicted=predicted,
        metrics={
            "aggregate": regression_metrics(actual, predicted),
            "per_bus": per_target_metrics(actual, predicted, target_names),
        },
        feature_importances=np.asarray(forest.feature_importances_, dtype=float),
        feature_names=feature_names,
        target_names=target_names,
    )
