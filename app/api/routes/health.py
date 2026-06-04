from fastapi import APIRouter

from app.schemas import HealthResponse

router = APIRouter()


@router.get(
    "/",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Health check",
    description="Returns a simple status payload confirming that the deterministic backend is running.",
)
def root():
    return {"status": "Deterministic Structural Decision Engine Active"}
