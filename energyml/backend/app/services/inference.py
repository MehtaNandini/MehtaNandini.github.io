from datetime import UTC, datetime
from time import perf_counter
from typing import Any
from uuid import uuid4

import numpy as np
import pandas as pd
from sqlalchemy.orm import Session

from app.features.forecasting import FORECAST_FEATURES
from app.models.entities import InferenceRun
from app.schemas.inference import ForecastInferenceRequest, StateInferenceRequest
from app.services.artifacts import ArtifactManager
from app.services.models import ModelService
from app.utils.hashing import sha256_json


class InferenceService:
    def __init__(
        self,
        session: Session,
        model_service: ModelService,
        artifact_manager: ArtifactManager,
    ) -> None:
        self.session = session
        self.model_service = model_service
        self.artifact_manager = artifact_manager

    def forecast(self, request: ForecastInferenceRequest) -> dict[str, Any]:
        model = self.model_service.resolve_for_inference(
            "forecasting", request.model_id
        )
        values = request.model_dump(exclude={"model_id"})
        if model.feature_names_json != FORECAST_FEATURES:
            raise ValueError(
                "registered forecasting model has an incompatible feature schema"
            )
        frame = pd.DataFrame(
            [{name: values[name] for name in model.feature_names_json}]
        )
        pipeline = self.artifact_manager.load_model(
            model.artifact_path, model.artifact_hash
        )
        started = perf_counter()
        prediction = float(pipeline.predict(frame)[0])
        duration = (perf_counter() - started) * 1000
        response: dict[str, Any] = {
            "prediction": prediction,
            "unit": "MW",
            "model_id": model.id,
            "model_version": model.version,
            "experiment_id": model.experiment_id,
            "prediction_timestamp": datetime.now(UTC),
        }
        self._log(
            model.id,
            model.experiment_id,
            "forecasting",
            values,
            {"prediction": prediction},
            duration,
        )
        return response

    def state_estimation(self, request: StateInferenceRequest) -> dict[str, Any]:
        model = self.model_service.resolve_for_inference(
            "state_estimation", request.model_id
        )
        expected = model.feature_names_json
        received = set(request.measurements)
        missing, extra = set(expected) - received, received - set(expected)
        if missing or extra:
            raise ValueError(
                f"measurement schema mismatch; missing={sorted(missing)}, extra={sorted(extra)}"
            )
        values = np.asarray(
            [request.measurements[name] for name in expected], dtype=float
        )
        if not np.all(np.isfinite(values)) or np.any(np.abs(values) > 1_000_000):
            raise ValueError(
                "measurements must be finite and within valid numeric ranges"
            )
        frame = pd.DataFrame([dict(zip(expected, values, strict=True))])
        pipeline = self.artifact_manager.load_model(
            model.artifact_path, model.artifact_hash
        )
        started = perf_counter()
        prediction = np.asarray(pipeline.predict(frame)[0], dtype=float)
        duration = (perf_counter() - started) * 1000
        voltages = {
            name.replace("voltage_magnitude_", ""): float(value)
            for name, value in zip(model.target_names_json, prediction, strict=True)
        }
        response: dict[str, Any] = {
            "voltages": voltages,
            "unit": "p.u.",
            "model_id": model.id,
            "model_version": model.version,
            "experiment_id": model.experiment_id,
            "prediction_timestamp": datetime.now(UTC),
        }
        self._log(
            model.id,
            model.experiment_id,
            "state_estimation",
            request.measurements,
            {"voltages": voltages},
            duration,
        )
        return response

    def _log(
        self,
        model_id: str,
        experiment_id: str,
        task_type: str,
        inputs: dict[str, Any],
        prediction: dict[str, Any],
        duration: float,
    ) -> None:
        self.session.add(
            InferenceRun(
                id=str(uuid4()),
                model_id=model_id,
                experiment_id=experiment_id,
                task_type=task_type,
                input_hash=sha256_json(inputs),
                prediction_json=prediction,
                execution_time_ms=duration,
            )
        )
        self.session.commit()
