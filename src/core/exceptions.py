from typing import Any, Dict, Optional
from fastapi import HTTPException, status


class DomainException(Exception):
    """Base exception for all domain business errors."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class EncounterNotFoundException(DomainException):
    """Raised when an encounter ID is invalid or not found."""
    pass


class AIServiceUnavailableException(DomainException):
    """Raised when an external AI service contract fails or times out."""
    pass


class AgentExecutionException(DomainException):
    """Raised when a specific LangGraph agent node fails to process state."""
    pass


class SafetyRedFlagException(DomainException):
    """Raised when emergency symptoms short-circuit normal execution."""
    pass


def setup_exception_handlers(app):
    """Registers global exception handlers for mapping domain exceptions to FastAPI HTTP responses."""
    @app.exception_handler(EncounterNotFoundException)
    async def encounter_not_found_handler(request, exc: EncounterNotFoundException):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "ENCOUNTER_NOT_FOUND", "message": exc.message, "details": exc.details}
        )

    @app.exception_handler(AIServiceUnavailableException)
    async def ai_service_unavailable_handler(request, exc: AIServiceUnavailableException):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"error": "AI_SERVICE_UNAVAILABLE", "message": exc.message, "details": exc.details}
        )

    @app.exception_handler(AgentExecutionException)
    async def agent_execution_handler(request, exc: AgentExecutionException):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "AGENT_EXECUTION_FAILURE", "message": exc.message, "details": exc.details}
        )
