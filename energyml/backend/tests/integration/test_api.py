import pandas as pd
from fastapi.testclient import TestClient

from app.features.forecasting import FORECAST_FEATURES, create_forecasting_features
from app.features.state_estimation import state_feature_target_columns


def _forecast_request(client: TestClient) -> tuple[dict[str, object], pd.DataFrame]:
    dataset_response = client.post(
        "/api/datasets/generate/renewable",
        json={"number_of_days": 40, "random_seed": 42},
    )
    assert dataset_response.status_code == 201
    dataset = dataset_response.json()
    frame = create_forecasting_features(pd.read_csv(dataset["file_path"]))
    experiment_response = client.post(
        "/api/experiments/forecasting",
        json={
            "dataset_id": dataset["id"],
            "model": {
                "type": "HistGradientBoostingRegressor",
                "learning_rate": 0.08,
                "max_iter": 25,
                "max_depth": 4,
                "min_samples_leaf": 8,
            },
        },
    )
    assert experiment_response.status_code == 201, experiment_response.text
    return experiment_response.json(), frame


def test_health_stats_validation_and_missing_model(client: TestClient) -> None:
    assert client.get("/api/health").json()["status"] == "healthy"
    stats = client.get("/api/stats").json()
    assert stats["datasets_count"] == 0
    assert client.post("/api/inference/forecast", json={}).status_code == 422
    valid_payload = {
        "solar_irradiance": 500,
        "temperature_c": 20,
        "wind_speed_mps": 5,
        "humidity_percent": 50,
        "cloud_cover_percent": 30,
        "hour": 12,
        "day_of_week": 1,
        "month": 6,
        "day_of_year": 160,
        "generation_lag_1": 20,
        "generation_lag_3": 20,
        "generation_lag_6": 20,
        "generation_lag_24": 20,
        "generation_rolling_mean_3": 20,
        "generation_rolling_mean_6": 20,
        "generation_rolling_mean_24": 20,
    }
    assert client.post("/api/inference/forecast", json=valid_payload).status_code == 404


def test_forecasting_end_to_end_comparison_and_deletion_protection(
    client: TestClient,
) -> None:
    first, frame = _forecast_request(client)
    model = client.get("/api/models").json()[0]
    assert client.post(f"/api/models/{model['id']}/activate").status_code == 200
    payload = {name: float(frame.iloc[-1][name]) for name in FORECAST_FEATURES}
    inference = client.post("/api/inference/forecast", json=payload)
    assert inference.status_code == 200, inference.text
    assert inference.json()["model_id"] == model["id"]
    second_response = client.post(
        "/api/experiments/forecasting",
        json={
            "dataset_id": first["dataset_id"],
            "random_seed": 43,
            "model": {"max_iter": 20, "max_depth": 3, "min_samples_leaf": 8},
        },
    )
    assert second_response.status_code == 201
    comparison = client.get(
        "/api/experiments/compare",
        params=[("ids", first["id"]), ("ids", second_response.json()["id"])],
    )
    assert comparison.status_code == 200
    assert len(comparison.json()) == 2
    artifacts = client.get(f"/api/experiments/{first['id']}/artifacts").json()
    assert {item["name"] for item in artifacts} >= {"model.joblib", "metrics.json"}
    assert client.delete(f"/api/datasets/{first['dataset_id']}").status_code == 409


def test_state_estimation_end_to_end_and_shape_validation(client: TestClient) -> None:
    dataset = client.post(
        "/api/datasets/generate/state-estimation",
        json={
            "network_size": 4,
            "number_of_samples": 350,
            "measurement_noise_std": 0.005,
            "random_seed": 42,
        },
    ).json()
    experiment = client.post(
        "/api/experiments/state-estimation",
        json={
            "dataset_id": dataset["id"],
            "model": {"n_estimators": 30, "max_depth": 8, "n_jobs": 1},
        },
    )
    assert experiment.status_code == 201, experiment.text
    model = next(
        item for item in client.get("/api/models").json() if item["task_type"] == "state_estimation"
    )
    assert client.post(f"/api/models/{model['id']}/activate").status_code == 200
    frame = pd.read_csv(dataset["file_path"])
    feature_names, _ = state_feature_target_columns(list(frame.columns))
    measurements = {name: float(frame.iloc[-1][name]) for name in feature_names}
    response = client.post("/api/inference/state-estimation", json={"measurements": measurements})
    assert response.status_code == 200, response.text
    assert len(response.json()["voltages"]) == 4
    measurements.pop(feature_names[0])
    invalid = client.post("/api/inference/state-estimation", json={"measurements": measurements})
    assert invalid.status_code == 400
    assert "missing" in invalid.json()["detail"]
