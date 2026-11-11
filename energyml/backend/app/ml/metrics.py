from typing import Any

import numpy as np
from numpy.typing import NDArray
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def regression_metrics(
    actual: NDArray[np.floating[Any]], predicted: NDArray[np.floating[Any]]
) -> dict[str, float]:
    actual_array = np.asarray(actual, dtype=float)
    predicted_array = np.asarray(predicted, dtype=float)
    metrics = {
        "mae": float(mean_absolute_error(actual_array, predicted_array)),
        "rmse": float(np.sqrt(mean_squared_error(actual_array, predicted_array))),
        "r2": float(r2_score(actual_array, predicted_array)),
    }
    safe = np.abs(actual_array) > 1e-6
    if actual_array.ndim == 1 and np.any(safe):
        metrics["mape_percent"] = float(
            np.mean(
                np.abs(
                    (actual_array[safe] - predicted_array[safe]) / actual_array[safe]
                )
            )
            * 100
        )
    return metrics


def per_target_metrics(
    actual: NDArray[np.floating[Any]],
    predicted: NDArray[np.floating[Any]],
    target_names: list[str],
) -> dict[str, dict[str, float]]:
    return {
        name: regression_metrics(actual[:, index], predicted[:, index])
        for index, name in enumerate(target_names)
    }
