"""Exercise a running Docker Compose deployment using only the public HTTP API."""

import argparse
import json
import time
import urllib.error
import urllib.request
from typing import Any

BASE_URL = "http://127.0.0.1:8000/api"


def request(method: str, path: str, payload: dict[str, Any] | None = None) -> Any:
    body = json.dumps(payload).encode() if payload is not None else None
    http_request = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=body,
        method=method,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(http_request, timeout=180) as response:
        return json.loads(response.read())


def wait_for_health(timeout_seconds: int = 120) -> None:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        try:
            if request("GET", "/health")["status"] == "healthy":
                return
        except (OSError, KeyError, urllib.error.HTTPError, urllib.error.URLError):
            time.sleep(2)
    raise TimeoutError("EnergyML did not become healthy")


def forecast_payload() -> dict[str, float | int]:
    return {
        "solar_irradiance": 620.5,
        "temperature_c": 23.4,
        "wind_speed_mps": 7.2,
        "humidity_percent": 58,
        "cloud_cover_percent": 25,
        "hour": 14,
        "day_of_week": 2,
        "month": 6,
        "day_of_year": 165,
        "generation_lag_1": 48.2,
        "generation_lag_3": 44.9,
        "generation_lag_6": 36.1,
        "generation_lag_24": 51.7,
        "generation_rolling_mean_3": 46.5,
        "generation_rolling_mean_6": 42.8,
        "generation_rolling_mean_24": 39.2,
    }


def state_measurements(feature_names: list[str]) -> dict[str, float]:
    values: dict[str, float] = {}
    for name in feature_names:
        if name == "load_factor":
            values[name] = 0.8
        elif name == "generation_factor":
            values[name] = 0.3
        elif name == "measurement_noise_std":
            values[name] = 0.005
        elif name.startswith("active_power") or name.startswith("power_flow"):
            values[name] = 0.5
        elif name.startswith("reactive_power"):
            values[name] = 0.15
        elif name.startswith("current_measurement"):
            values[name] = 0.6
        elif name.startswith("selected_voltage"):
            values[name] = 1.0
        else:
            raise ValueError(f"unrecognised state feature: {name}")
    return values


def active_model(task_type: str) -> dict[str, Any]:
    return next(
        model
        for model in request("GET", "/models")
        if model["task_type"] == task_type and model["active"]
    )


def seed_and_verify() -> dict[str, Any]:
    renewable = request(
        "POST",
        "/datasets/generate/renewable",
        {"number_of_days": 40, "random_seed": 42},
    )
    request(
        "POST",
        "/experiments/forecasting",
        {
            "dataset_id": renewable["id"],
            "random_seed": 42,
            "model": {"max_iter": 25, "max_depth": 4, "min_samples_leaf": 8},
        },
    )
    forecast_model = next(
        model for model in request("GET", "/models") if model["task_type"] == "forecasting"
    )
    request("POST", f"/models/{forecast_model['id']}/activate")
    forecast = request("POST", "/inference/forecast", forecast_payload())

    state_dataset = request(
        "POST",
        "/datasets/generate/state-estimation",
        {"network_size": 4, "number_of_samples": 350, "random_seed": 42},
    )
    request(
        "POST",
        "/experiments/state-estimation",
        {
            "dataset_id": state_dataset["id"],
            "random_seed": 42,
            "model": {"n_estimators": 30, "max_depth": 8, "n_jobs": 1},
        },
    )
    state_model = next(
        model for model in request("GET", "/models") if model["task_type"] == "state_estimation"
    )
    request("POST", f"/models/{state_model['id']}/activate")
    state = request(
        "POST",
        "/inference/state-estimation",
        {"measurements": state_measurements(state_model["feature_names_json"])},
    )
    stats = request("GET", "/stats")
    assert stats["datasets_count"] >= 2
    assert stats["completed_experiments"] >= 2
    assert stats["total_inference_requests"] >= 2
    return {"forecast": forecast, "state": state, "stats": stats}


def verify_after_restart() -> dict[str, Any]:
    forecast_model = active_model("forecasting")
    state_model = active_model("state_estimation")
    forecast = request("POST", "/inference/forecast", forecast_payload())
    state = request(
        "POST",
        "/inference/state-estimation",
        {"measurements": state_measurements(state_model["feature_names_json"])},
    )
    stats = request("GET", "/stats")
    assert forecast["model_id"] == forecast_model["id"]
    assert state["model_id"] == state_model["id"]
    assert stats["datasets_count"] >= 2
    assert stats["completed_experiments"] >= 2
    assert stats["total_inference_requests"] >= 4
    return {"forecast": forecast, "state": state, "stats": stats}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["seed", "after-restart"])
    arguments = parser.parse_args()
    wait_for_health()
    result = seed_and_verify() if arguments.mode == "seed" else verify_after_restart()
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
