from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.db.session import get_db
from app.services.artifacts import ArtifactManager
from app.services.datasets import DatasetService
from app.services.experiments import ExperimentService
from app.services.inference import InferenceService
from app.services.models import ModelService


def dataset_service(
    session: Session = Depends(get_db), settings: Settings = Depends(get_settings)
) -> DatasetService:
    return DatasetService(session, settings.dataset_dir)


def artifact_manager(settings: Settings = Depends(get_settings)) -> ArtifactManager:
    return ArtifactManager(settings.artifact_dir)


def model_service(session: Session = Depends(get_db)) -> ModelService:
    return ModelService(session)


def experiment_service(
    session: Session = Depends(get_db),
    manager: ArtifactManager = Depends(artifact_manager),
) -> ExperimentService:
    return ExperimentService(session, manager)


def inference_service(
    session: Session = Depends(get_db),
    models: ModelService = Depends(model_service),
    manager: ArtifactManager = Depends(artifact_manager),
) -> InferenceService:
    return InferenceService(session, models, manager)
