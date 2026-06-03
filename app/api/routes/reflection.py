from fastapi import APIRouter

from app.schemas import ReflectionRequest, ReflectionResponse
from app.services.reflection_service import create_reflection

router = APIRouter()


@router.post("/decision/reflect", response_model=ReflectionResponse)
def reflect(request: ReflectionRequest):
    """
    Get Absolem's philosophical wisdom on the decision.

    This endpoint provides:
    - Philosophical advice specific to the decision choice
    - Burnout prevention guidance
    - Action plan for sustainable decision implementation

    Includes mitigation strategies:
    - Falls back to default wisdom if API unavailable
    - Caches responses to reduce API calls
    - Monitors usage statistics
    """
    return create_reflection(request)
