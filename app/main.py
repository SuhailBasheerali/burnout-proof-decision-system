import logging

from fastapi import FastAPI

from app.api.routes import decision, health, monitoring, reflection
from app.config import settings

# Configure logging to display INFO level messages
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:     %(message)s"
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = FastAPI(
    title=settings.app_title,
    summary="Deterministic decision support API with an optional AI reflection layer.",
    description=(
        "Evaluate academic or burnout-sensitive decisions using explainable structural scoring. "
        "The comparison engine is deterministic and available without AI. "
        "An optional reflection layer can add qualitative guidance with graceful fallback behavior."
    ),
    version="1.0.0",
    contact={
        "name": "Burnout-Proof Decision System",
    },
    openapi_tags=[
        {"name": "Health", "description": "Service health and basic availability checks."},
        {"name": "Decision", "description": "Deterministic option comparison and recommendation endpoints."},
        {"name": "Reflection", "description": "Optional AI-assisted reflection and burnout-prevention guidance."},
        {"name": "Monitoring", "description": "Usage and rate-limit visibility for the optional reflection layer."},
    ],
)


app.include_router(health.router)
app.include_router(decision.router)
app.include_router(reflection.router)
app.include_router(monitoring.router)
