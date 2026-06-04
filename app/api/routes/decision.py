from fastapi import APIRouter

from app.schemas import CompareRequest, CompareResponse
from app.services.decision_service import compare_decision_options

router = APIRouter()


@router.post(
    "/decision/compare",
    response_model=CompareResponse,
    tags=["Decision"],
    summary="Compare decision options",
    description=(
        "Runs the deterministic decision engine against one to five options, "
        "scores growth and sustainability, applies burnout-aware penalties, "
        "and returns a recommendation with sensitivity analysis."
    ),
    response_description="Structured comparison result with sorted evaluations and overall decision status.",
)
def compare(request: CompareRequest):
    return compare_decision_options(request)
