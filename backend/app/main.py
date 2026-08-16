"""
CarePath AI - Main FastAPI Application Entry Point
=================================================
Configures Middlewares, CORS, Structured Logging, Health Check, and mounts API v1 Routers.
"""

import sys
import os
# Add the project root (CarePath-AI) to sys.path so it can resolve the 'database' package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging, logger
from app.api.v1.endpoints.agents import router as agents_router
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.patients import router as patients_router
from app.api.v1.endpoints.analysis import router as analysis_router
from app.api.v1.endpoints.timeline import router as timeline_router
from app.api.v1.endpoints.followup import router as followup_router
from app.api.v1.endpoints.notifications import router as notifications_router
from app.api.v1.endpoints.upload import router as upload_router
from app.api.v1.endpoints.medications import router as medications_router
from app.api.v1.endpoints.careplans import router as careplans_router
from app.api.v1.endpoints.memory import router as memory_router
from app.api.v1.endpoints.doctor import router as doctor_router
from app.api.v1.endpoints.analytics import router as analytics_router

setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    debug=settings.DEBUG,
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(agents_router, prefix=settings.API_V1_STR)
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(patients_router, prefix=settings.API_V1_STR)
app.include_router(analysis_router, prefix=settings.API_V1_STR)
app.include_router(timeline_router, prefix=settings.API_V1_STR)
app.include_router(followup_router, prefix=settings.API_V1_STR)
app.include_router(notifications_router, prefix=settings.API_V1_STR)
app.include_router(upload_router, prefix=settings.API_V1_STR)
app.include_router(medications_router, prefix=settings.API_V1_STR)
app.include_router(careplans_router, prefix=settings.API_V1_STR)
app.include_router(memory_router, prefix=settings.API_V1_STR)
app.include_router(doctor_router, prefix=settings.API_V1_STR)
app.include_router(analytics_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {
        "app_name": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
        "status": "online",
        "docs_url": "/docs"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "CarePath AI Backend & Multi-Agent Engine",
        "version": "2.0.0"
    }
