from pydantic import BaseModel, Field
from typing import List

class Criterion(BaseModel):
    weight: int = Field(..., ge=0, le=10)
    impact: int = Field(..., ge=0, le=10)

class DecisionCreate(BaseModel):
    title: str
    growth_criteria: List[Criterion]
    sustainability_criteria: List[Criterion]

class DecisionResponse(BaseModel):
    id: int
    title: str
    growth_score: float
    sustainability_score: float
    tension_index: float
    zone: str

    class Config:
        orm_mode = True