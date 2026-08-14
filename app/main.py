"""Main FastAPI Application Entrypoint."""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import MedicalAIException, http_status_for
from app.api.v1.router import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Enterprise Multi-Modal Medical Intelligence Platform API",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Enable CORS for Streamlit UI & external consumers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


# ---------------------------------------------------------------------------
# Global Exception Handler — converts MedicalAIException → structured JSON
# ---------------------------------------------------------------------------

@app.exception_handler(MedicalAIException)
async def medical_ai_exception_handler(request: Request, exc: MedicalAIException) -> JSONResponse:
    """Return a structured error response for all CarePath AI typed exceptions.

    The response body contains:
    - ``error_code``: machine-readable snake_case error category.
    - ``detail``: human-readable error description.

    HTTP status is determined by :func:`~app.core.exceptions.http_status_for`.
    """
    status_code = http_status_for(exc)
    logger.warning(
        "MedicalAIException: code=%s status=%d path=%s msg=%s",
        exc.error_code,
        status_code,
        request.url.path,
        exc.message,
    )
    return JSONResponse(
        status_code=status_code,
        content={
            "error_code": exc.error_code,
            "detail": exc.message,
        },
    )


@app.get("/", tags=["Health"])
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting CarePath AI application server...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

