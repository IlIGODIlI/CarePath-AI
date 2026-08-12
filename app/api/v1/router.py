"""API Router Aggregator."""
from fastapi import APIRouter
from app.api.v1.ocr import router as ocr_router
from app.api.v1.vision import router as vision_router
from app.api.v1.nlp import router as nlp_router
from app.api.v1.rag import router as rag_router
from app.api.v1.diagnosis import router as diagnosis_router

api_router = APIRouter()

api_router.include_router(ocr_router)
api_router.include_router(vision_router)
api_router.include_router(nlp_router)
api_router.include_router(rag_router)
api_router.include_router(diagnosis_router)


@api_router.get("/status", tags=["Health"])
async def get_status():
    return {
        "status": "healthy",
        "service": "CarePath AI API v1",
        "version": "0.1.0"
    }
