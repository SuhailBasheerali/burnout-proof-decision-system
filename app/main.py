from fastapi import FastAPI

app = FastAPI(title="Burnout-Proof Decision Engine")

@app.get("/")
def root():
    return {"status": "Deterministic Core Active"}

from .database import engine
from .models import Base

Base.metadata.create_all(bind=engine)

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import Base, Decision
from .schemas import DecisionCreate, DecisionResponse
from .decision_engine import calculate_score
from .zone_classifier import classify_zone

app = FastAPI(title="Burnout-Proof Decision Engine")

Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/decision/evaluate", response_model=DecisionResponse)
def evaluate_decision(decision: DecisionCreate, db: Session = Depends(get_db)):

    if len(decision.growth_criteria) < 1 or len(decision.sustainability_criteria) < 1:
        raise HTTPException(status_code=400, detail="Must include at least one criterion in both categories.")

    growth_score = calculate_score(decision.growth_criteria)
    sustainability_score = calculate_score(decision.sustainability_criteria)
    tension_index = abs(growth_score - sustainability_score)

    zone = classify_zone(growth_score, sustainability_score)

    db_decision = Decision(
        title=decision.title,
        growth_score=growth_score,
        sustainability_score=sustainability_score,
        tension_index=tension_index,
        zone=zone,
    )

    db.add(db_decision)
    db.commit()
    db.refresh(db_decision)

    return db_decision