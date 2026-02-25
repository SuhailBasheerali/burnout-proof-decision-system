from pydantic import BaseModel, Field
from typing import List


# ----------------------------
# Criterion Model
# ----------------------------
class Criterion(BaseModel):
    weight: int = Field(..., ge=0, le=10)
    impact: int = Field(..., ge=0, le=10)


# ----------------------------
# Decision Option Input Model
# ----------------------------
class DecisionOption(BaseModel):
    title: str
    growth_criteria: List[Criterion]
    sustainability_criteria: List[Criterion]


# ----------------------------
# Multi-Option Request Model
# ----------------------------
class CompareRequest(BaseModel):
    options: List[DecisionOption]


# ----------------------------
# Evaluation Output Model
# ----------------------------
class OptionEvaluation(BaseModel):
    title: str
    growth_score: float
    sustainability_score: float
    tension_index: float
    tension_severity: str
    zone: str
    zone_reason: str
    composite_score: float


# ----------------------------
# Multi and single-Option Response Model
# ----------------------------
class CompareResponse(BaseModel):
    evaluations: List[OptionEvaluation]
    recommended_option: str
    decision_status: str
    recommendation_reason: str
    risk_awareness: str | None = None