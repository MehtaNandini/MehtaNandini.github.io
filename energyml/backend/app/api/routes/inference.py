from fastapi import APIRouter, Depends

from app.api.dependencies import inference_service
from app.schemas.inference import (
    ForecastInferenceRequest,
    ForecastInferenceResponse,
    StateInferenceRequest,
    StateInferenceResponse,
)
from app.services.inference import InferenceService

router = APIRouter(prefix="/inference", tags=["inference"])


@router.post("/forecast", response_model=ForecastInferenceResponse)
def forecast(
    request: ForecastInferenceRequest,
    service: InferenceService = Depends(inference_service),
) -> object:
    return service.forecast(request)


@router.post("/state-estimation", response_model=StateInferenceResponse)
def state_estimation(
    request: StateInferenceRequest,
    service: InferenceService = Depends(inference_service),
) -> object:
    return service.state_estimation(request)
