from fastapi import FastAPI

app = FastAPI(title="Burnout-Proof Decision Engine")

@app.get("/")
def root():
    return {"status": "Deterministic Core Active"}

from .database import engine
from .models import Base

Base.metadata.create_all(bind=engine)