from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.base import Base
from app.db.session import get_engine, get_session_factory
from app.services.artifacts import ArtifactManager
from app.services.datasets import DatasetService


def services() -> tuple[Session, DatasetService, ArtifactManager]:
    settings = get_settings()
    Base.metadata.create_all(get_engine())
    session = get_session_factory()()
    return (
        session,
        DatasetService(session, settings.dataset_dir),
        ArtifactManager(settings.artifact_dir),
    )
