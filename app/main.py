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

app = FastAPI(title=settings.app_title)


app.include_router(health.router)
app.include_router(decision.router)
app.include_router(reflection.router)
app.include_router(monitoring.router)
