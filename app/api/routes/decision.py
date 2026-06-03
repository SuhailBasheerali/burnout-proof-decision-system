from fastapi import APIRouter

from app.schemas import CompareRequest, CompareResponse
from app.services.decision_service import compare_decision_options

router = APIRouter()


@router.post("/decision/compare", response_model=CompareResponse)
def compare(request: CompareRequest):
    return compare_decision_options(request)
