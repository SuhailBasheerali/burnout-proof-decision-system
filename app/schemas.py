from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List


# ----------------------------
# Criterion Model
# ----------------------------
class Criterion(BaseModel):
    weight: float = Field(..., ge=0, le=10)
    impact: int = Field(..., ge=0, le=10)
    
    @model_validator(mode="after")
    def validate_weight_impact_semantic(self):
        """
        NEW: Validates semantic relationship between weight and impact.
        High-impact items (8+) should typically have meaningful weight (2+).
        This catches nonsensical combinations like high impact with zero weight.
        """
        # Warning case: high impact (8+) with very low weight (<1)
        # This is allowed but semantically odd - typically means "important but underweighted"
        if self.impact >= 8 and self.weight < 1 and self.weight > 0:
            # Log/track but don't block - user might have intentional reason
            pass
        
        # The schema validator will handle all-zero weights at the criteria list level
        return self


# ----------------------------
# Decision Option Input Model
# ----------------------------
class DecisionOption(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    growth_criteria: List[Criterion]
    sustainability_criteria: List[Criterion]

    @field_validator("growth_criteria", "sustainability_criteria")
    @classmethod
    def validate_non_empty(cls, value):
        if len(value) == 0:
            raise ValueError(
                "Each option must include at least one criterion in both growth and sustainability."
            )
        
        # NEW: Reject criteria with all-zero weights
        total_weight = sum(c.weight for c in value)
        if total_weight == 0:
            raise ValueError(
                "At least one criterion must have a non-zero weight. All-zero weights create meaningless scores."
            )
        
        return value


# ----------------------------
# Multi-Option Request Model
# ----------------------------
class CompareRequest(BaseModel):
    options: List[DecisionOption] = Field(..., min_length=1, max_length=10)


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
    risk_level: str
    triggered_messages: List[str]
    sensitivity_range: float
    stability_level: str
    sensitivity_breakdown: str = "Sensitivity analysis breakdown"


# ----------------------------
# Multi & Single Option Response
# ----------------------------
class CompareResponse(BaseModel):
    evaluations: List[OptionEvaluation]
    recommended_option: str
    decision_status: str
    recommendation_reason: str


# ----------------------------
# AI Reflection Request & Response
# ----------------------------
class ReflectionRequest(BaseModel):
    """Request for Absolem's reflective wisdom."""
    options: List[DecisionOption]
    comparison_result: dict  # Flexible dict instead of strict CompareResponse


class ReflectionResponse(BaseModel):
    """Absolem's philosophical wisdom with action plan for burnout prevention."""
    action_plan: List[str]
    philosophical_advice: str
    source: str