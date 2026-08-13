from fastapi import APIRouter
from src.api.v1.endpoints import encounters, health

api_v1_router = APIRouter()
api_v1_router.include_router(health.router)
api_v1_router.include_router(encounters.router)
