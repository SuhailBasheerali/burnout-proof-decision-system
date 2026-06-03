import logging

from dotenv import load_dotenv
from fastapi import FastAPI

from app.api.routes import decision, health, monitoring, reflection

# Load environment variables from .env file
load_dotenv()

# Configure logging to display INFO level messages
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:     %(message)s"
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = FastAPI(title="Burnout-Proof Decision Engine")


app.include_router(health.router)
app.include_router(decision.router)
app.include_router(reflection.router)
app.include_router(monitoring.router)
