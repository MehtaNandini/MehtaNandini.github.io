import os
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.db.session import get_db
from app.services.stats import platform_stats

router = APIRouter(tags=["system"])


@router.get("/health")
def health(
    session: Session = Depends(get_db), settings: Settings = Depends(get_settings)
) -> dict[str, str]:
    session.execute(text("SELECT 1"))
    artifact_root = Path(settings.artifact_dir)
    artifact_root.mkdir(parents=True, exist_ok=True)
    if not os.access(artifact_root, os.W_OK):
        raise RuntimeError("artifact storage is unavailable")
    return {
        "status": "healthy",
        "database": "connected",
        "artifact_storage": "available",
    }


@router.get("/stats")
def stats(session: Session = Depends(get_db)) -> dict[str, Any]:
    return platform_stats(session)
