from typing import Any

import matplotlib
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

matplotlib.use("Agg")
from matplotlib import pyplot as plt  # noqa: E402


def actual_vs_predicted(
    actual: NDArray[np.floating[Any]], predicted: NDArray[np.floating[Any]], title: str
) -> Figure:
    figure, axis = plt.subplots(figsize=(6, 5))
    axis.scatter(actual, predicted, alpha=0.35, s=12, color="#0f766e")
    bounds = [
        float(min(np.min(actual), np.min(predicted))),
        float(max(np.max(actual), np.max(predicted))),
    ]
    axis.plot(bounds, bounds, "--", color="#f97316", label="Ideal")
    axis.set(xlabel="Actual", ylabel="Predicted", title=title)
    axis.legend()
    figure.tight_layout()
    return figure


def error_distribution(errors: NDArray[np.floating[Any]], title: str) -> Figure:
    figure, axis = plt.subplots(figsize=(6, 4))
    axis.hist(np.ravel(errors), bins=35, color="#0f766e", alpha=0.82)
    axis.axvline(0, color="#f97316", linestyle="--")
    axis.set(xlabel="Prediction error", ylabel="Count", title=title)
    figure.tight_layout()
    return figure


def forecasting_timeseries(
    actual: NDArray[np.floating[Any]], predicted: NDArray[np.floating[Any]]
) -> Figure:
    figure, axis = plt.subplots(figsize=(10, 4))
    count = min(336, len(actual))
    axis.plot(np.arange(count), actual[:count], label="Actual", linewidth=1.5)
    axis.plot(np.arange(count), predicted[:count], label="Forecast", linewidth=1.2)
    axis.set(
        xlabel="Held-out test hour",
        ylabel="Generation (MW)",
        title="Two-week forecast window",
    )
    axis.legend()
    figure.tight_layout()
    return figure


def feature_importance_plot(
    names: list[str], importances: NDArray[np.floating[Any]]
) -> Figure:
    order = np.argsort(importances)[-12:]
    figure, axis = plt.subplots(figsize=(7, 5))
    axis.barh(np.asarray(names)[order], importances[order], color="#0f766e")
    axis.set(xlabel="Permutation importance", title="Feature importance")
    figure.tight_layout()
    return figure


def per_bus_errors(names: list[str], errors: list[float]) -> Figure:
    short_names = [name.replace("voltage_magnitude_", "") for name in names]
    figure, axis = plt.subplots(figsize=(8, 4))
    axis.bar(short_names, errors, color="#0f766e")
    axis.set(xlabel="Bus", ylabel="MAE (p.u.)", title="Per-bus voltage error")
    axis.tick_params(axis="x", rotation=45)
    figure.tight_layout()
    return figure
