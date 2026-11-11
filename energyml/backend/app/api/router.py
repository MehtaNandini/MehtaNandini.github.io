from fastapi import APIRouter

from app.api.routes import datasets, experiments, inference, models, system

api_router = APIRouter()
api_router.include_router(system.router)
api_router.include_router(datasets.router)
api_router.include_router(experiments.router)
api_router.include_router(models.router)
api_router.include_router(inference.router)
