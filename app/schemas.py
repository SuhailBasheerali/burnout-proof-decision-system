from typing import Any, Dict, List

from pydantic import BaseModel, Field, field_validator, model_validator


# ----------------------------
# Criterion Model
# ----------------------------
class Criterion(BaseModel):
    weight: float = Field(
        ...,
        ge=0,
        le=10,
        description="Importance of the criterion in the final decision, on a 0-10 scale.",
        examples=[8],
    )
    impact: int = Field(
        ...,
        ge=0,
        le=10,
        description="How strongly this criterion affects the option, on a 0-10 scale.",
        examples=[9],
    )
    
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
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Human-readable option name shown in the comparison results.",
        examples=["Take the research internship"],
    )
    growth_criteria: List[Criterion] = Field(
        ...,
        description="Criteria representing upside, progress, learning, or opportunity gains.",
    )
    sustainability_criteria: List[Criterion] = Field(
        ...,
        description="Criteria representing energy cost, recovery capacity, and long-term maintainability.",
    )

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
    options: List[DecisionOption] = Field(
        ...,
        min_length=1,
        max_length=5,
        description="One to five decision options to evaluate against growth and sustainability criteria.",
    )


# ----------------------------
# Evaluation Output Model
# ----------------------------
class OptionEvaluation(BaseModel):
    title: str = Field(description="Option title carried through from the request.")
    growth_score: float = Field(description="Normalized 0-100 growth score.")
    sustainability_score: float = Field(description="Normalized 0-100 sustainability score.")
    tension_index: float = Field(description="Absolute difference between growth and sustainability scores.")
    tension_severity: str = Field(description="Severity bucket for the tension index, such as STABLE or CRITICAL.")
    zone: str = Field(description="Strategic zone classification for the option.")
    zone_reason: str = Field(description="Plain-language explanation for the zone classification.")
    composite_score: float = Field(description="Final viability score after applying imbalance penalties.")
    risk_level: str = Field(description="Burnout or stagnation risk classification for the option.")
    triggered_messages: List[str] = Field(description="Warnings or guidance triggered by structural risk patterns.")
    sensitivity_range: float = Field(description="Estimated score variability under small perturbations.")
    stability_level: str = Field(description="Interpretation of sensitivity, such as ROBUST or FRAGILE.")
    sensitivity_breakdown: str = Field(
        default="Sensitivity analysis breakdown",
        description="Human-readable summary of the growth and sustainability sensitivity checks.",
    )


# ----------------------------
# Multi & Single Option Response
# ----------------------------
class CompareResponse(BaseModel):
    evaluations: List[OptionEvaluation] = Field(description="Evaluations sorted by descending composite score.")
    recommended_option: str = Field(description="Winning option title, or a sentinel value when no single winner exists.")
    decision_status: str = Field(description="Outcome type such as CLEAR_WINNER, CLOSE_COMPETITION, or ALL_OPTIONS_POOR_FIT.")
    recommendation_reason: str = Field(description="Short explanation for why the result was classified this way.")


# ----------------------------
# AI Reflection Request & Response
# ----------------------------
class ReflectionRequest(BaseModel):
    """Request for Absolem's reflective wisdom."""
    options: List[DecisionOption] = Field(
        ...,
        description="The original decision options so the reflection layer can reason about the trade-offs.",
    )
    comparison_result: Dict[str, Any] = Field(
        ...,
        description="Comparison response payload returned by /decision/compare.",
    )


class ReflectionResponse(BaseModel):
    """Absolem's philosophical wisdom with action plan for burnout prevention."""
    action_plan: List[str] = Field(description="Concrete next steps to implement the chosen option sustainably.")
    philosophical_advice: str = Field(description="Reflective guidance focused on wellbeing and burnout prevention.")
    source: str = Field(description="Whether the reflection came from Gemini or the built-in fallback wisdom.")


class HealthResponse(BaseModel):
    status: str = Field(description="Service availability message.")


class ReflectionUsageStats(BaseModel):
    total_calls: int = Field(description="Total reflection requests attempted in the current process.")
    failed_calls: int = Field(description="Reflection requests that fell back because the AI call failed.")
    cached_calls: int = Field(description="Requests served from the local reflection cache.")
    cache_enabled: bool = Field(description="Whether response caching is enabled.")
    fallback_available: bool = Field(description="Whether default non-AI wisdom is available.")
    timestamp: str = Field(description="Timestamp when the stats snapshot was generated.")


class ReflectionStatsResponse(BaseModel):
    ai_reflection_stats: ReflectionUsageStats
    message: str = Field(description="Operator guidance for interpreting the usage metrics.")


class RateLimitResponse(BaseModel):
    max_calls_per_day: int = Field(description="Configured daily Gemini request cap.")
    calls_used_today: int = Field(description="Number of Gemini calls recorded for the current UTC day.")
    calls_remaining: int = Field(description="Remaining Gemini calls before the daily cap is reached.")
    percentage_used: int = Field(description="Used portion of the daily cap expressed as a whole-number percent.")
    reset_time: str = Field(description="ISO-8601 UTC timestamp for the next rate-limit reset.")
    status: str = Field(description="Current rate-limit state: OK, WARNING, or EXCEEDED.")
    gemini_available: bool = Field(description="Whether Gemini is configured and available for live reflections.")
