from typing import Any

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import artifact_manager, dataset_service, experiment_service
from app.db.session import get_db
from app.experiments.forecasting import ForecastingExperimentRunner
from app.experiments.state_estimation import StateEstimationExperimentRunner
from app.schemas.experiments import (
    ExperimentView,
    ForecastExperimentCreate,
    StateExperimentCreate,
)
from app.services.artifacts import ArtifactManager
from app.services.datasets import DatasetService
from app.services.experiments import ExperimentService

router = APIRouter(prefix="/experiments", tags=["experiments"])


@router.post("/forecasting", response_model=ExperimentView, status_code=status.HTTP_201_CREATED)
def run_forecasting(
    request: ForecastExperimentCreate,
    session: Session = Depends(get_db),
    datasets: DatasetService = Depends(dataset_service),
    artifacts: ArtifactManager = Depends(artifact_manager),
) -> object:
    experiment, _ = ForecastingExperimentRunner(session, datasets, artifacts).run(request)
    return experiment


@router.post(
    "/state-estimation",
    response_model=ExperimentView,
    status_code=status.HTTP_201_CREATED,
)
def run_state_estimation(
    request: StateExperimentCreate,
    session: Session = Depends(get_db),
    datasets: DatasetService = Depends(dataset_service),
    artifacts: ArtifactManager = Depends(artifact_manager),
) -> object:
    experiment, _ = StateEstimationExperimentRunner(session, datasets, artifacts).run(request)
    return experiment


@router.get("", response_model=list[ExperimentView])
def list_experiments(
    service: ExperimentService = Depends(experiment_service),
) -> object:
    return service.list_all()


@router.get("/compare")
def compare_experiments(
    ids: list[str] = Query(...),
    service: ExperimentService = Depends(experiment_service),
) -> list[dict[str, Any]]:
    return service.compare(ids)


@router.get("/{experiment_id}", response_model=ExperimentView)
def get_experiment(
    experiment_id: str, service: ExperimentService = Depends(experiment_service)
) -> object:
    return service.get(experiment_id)


@router.get("/{experiment_id}/metrics")
def get_metrics(
    experiment_id: str, service: ExperimentService = Depends(experiment_service)
) -> dict[str, Any]:
    return service.metrics(experiment_id)


@router.get("/{experiment_id}/artifacts")
def get_artifacts(
    experiment_id: str, service: ExperimentService = Depends(experiment_service)
) -> list[dict[str, Any]]:
    return service.artifacts(experiment_id)
