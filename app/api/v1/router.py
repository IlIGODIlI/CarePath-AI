"""API Router Aggregator."""
from fastapi import APIRouter
from app.api.v1.ocr import router as ocr_router
from app.api.v1.vision import router as vision_router
from app.api.v1.nlp import router as nlp_router
from app.api.v1.rag import router as rag_router
from app.api.v1.diagnosis import router as diagnosis_router
from app.api.v1.patient_summary import router as summary_router
from app.api.v1.case_questions import router as questions_router
from app.api.v1.clinical_extraction import router as extraction_router
from app.api.v1.doctor_feedback import router as feedback_router
from app.api.v1.treatment_response import router as treatment_response_router
from app.api.v1.follow_up_intelligence import router as follow_up_router
from app.api.v1.personalized_care_plan import router as care_plan_router

api_router = APIRouter()

api_router.include_router(ocr_router)
api_router.include_router(vision_router)
api_router.include_router(nlp_router)
api_router.include_router(rag_router)
api_router.include_router(diagnosis_router)
api_router.include_router(summary_router)
api_router.include_router(questions_router)
api_router.include_router(extraction_router)
api_router.include_router(feedback_router)
api_router.include_router(treatment_response_router)
api_router.include_router(follow_up_router)
api_router.include_router(care_plan_router)


@api_router.get("/status", tags=["Health"])
async def get_status():
    return {
        "status": "healthy",
        "service": "CarePath AI API v1",
        "version": "0.1.0"
    }
