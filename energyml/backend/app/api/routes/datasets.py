from fastapi import APIRouter, Depends, Response, status

from app.api.dependencies import dataset_service
from app.schemas.datasets import DatasetView, RenewableDatasetCreate, StateDatasetCreate
from app.services.datasets import DatasetService

router = APIRouter(prefix="/datasets", tags=["datasets"])


@router.post(
    "/generate/renewable",
    response_model=DatasetView,
    status_code=status.HTTP_201_CREATED,
)
def generate_renewable(
    request: RenewableDatasetCreate, service: DatasetService = Depends(dataset_service)
) -> object:
    return service.generate_renewable(request)


@router.post(
    "/generate/state-estimation",
    response_model=DatasetView,
    status_code=status.HTTP_201_CREATED,
)
def generate_state(
    request: StateDatasetCreate, service: DatasetService = Depends(dataset_service)
) -> object:
    return service.generate_state(request)


@router.get("", response_model=list[DatasetView])
def list_datasets(service: DatasetService = Depends(dataset_service)) -> object:
    return service.list()


@router.get("/{dataset_id}", response_model=DatasetView)
def get_dataset(
    dataset_id: str, service: DatasetService = Depends(dataset_service)
) -> object:
    return service.get(dataset_id)


@router.delete("/{dataset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dataset(
    dataset_id: str, service: DatasetService = Depends(dataset_service)
) -> Response:
    service.delete(dataset_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
