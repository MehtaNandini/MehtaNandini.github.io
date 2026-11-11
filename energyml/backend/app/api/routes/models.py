from fastapi import APIRouter, Depends

from app.api.dependencies import model_service
from app.schemas.models import ModelView
from app.services.models import ModelService

router = APIRouter(prefix="/models", tags=["models"])


@router.get("", response_model=list[ModelView])
def list_models(service: ModelService = Depends(model_service)) -> object:
    return service.list()


@router.get("/{model_id}", response_model=ModelView)
def get_model(model_id: str, service: ModelService = Depends(model_service)) -> object:
    return service.get(model_id)


@router.post("/{model_id}/activate", response_model=ModelView)
def activate_model(
    model_id: str, service: ModelService = Depends(model_service)
) -> object:
    return service.activate(model_id)
