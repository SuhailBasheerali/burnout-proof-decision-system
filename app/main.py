from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from fastapi import FastAPI, HTTPException
from app.schemas import (
    CompareRequest, 
    CompareResponse, 
    OptionEvaluation,
    ReflectionRequest,
    ReflectionResponse
)

from app.engine.evaluator import normalize_score, composite_score
from app.engine.classifier import (
    classify_zone,
    classify_tension,
    classify_risk,
)
from app.engine.triggers import generate_triggers
from app.engine.sensitivity import (
    perform_sensitivity_analysis,
    classify_stability,
)
from app.engine.comparator import detect_close_competition
from app.engine.ai_reflector import get_absolem_wisdom


app = FastAPI(title="Burnout-Proof Decision Engine")


@app.get("/")
def root():
    return {"status": "Deterministic Structural Decision Engine Active"}


@app.post("/decision/compare", response_model=CompareResponse)
def compare(request: CompareRequest):

    # --------------------------------------------------
    # Defensive Constraint: Duplicate Titles Only
    # (Length constraints handled by schema)
    # --------------------------------------------------
    titles = [o.title for o in request.options]
    if len(set(titles)) != len(titles):
        raise HTTPException(
            status_code=400,
            detail="Duplicate option titles are not allowed."
        )

    evaluations = []

    # --------------------------------------------------
    # Evaluation Loop
    # --------------------------------------------------
    for option in request.options:

        # 1️⃣ Normalized Scores (Weighted Mean → 0-100)
        growth = normalize_score(option.growth_criteria)
        sustainability = normalize_score(option.sustainability_criteria)

        # 2️⃣ Tension & Severity
        tension = abs(growth - sustainability)
        tension_severity = classify_tension(tension)

        # 3️⃣ Zone Classification
        zone, zone_reason = classify_zone(growth, sustainability)

        # 4️⃣ Composite Score (Continuous Imbalance Penalty)
        comp = composite_score(growth, sustainability)

        # 5️⃣ Structural Risk
        risk = classify_risk(zone, tension_severity, growth, sustainability)

        # 6️⃣ Triggered Structural Messages
        triggers = generate_triggers(
            growth,
            sustainability,
            tension,
            tension_severity,
            zone
        )

        # 7️⃣ Sensitivity Analysis (±20% weight perturbation)
        growth_sens = perform_sensitivity_analysis(
            option.growth_criteria,
            normalize_score
        )

        sust_sens = perform_sensitivity_analysis(
            option.sustainability_criteria,
            normalize_score
        )

        # Extract combined sensitivities (worst-case for each dimension)
        growth_combined = growth_sens['combined_sensitivity']
        sust_combined = sust_sens['combined_sensitivity']
        sensitivity_range = round((growth_combined + sust_combined) / 2, 2)
        
        # Build comprehensive breakdown
        sensitivity_breakdown = (
            f"Growth robustness: {growth_sens['breakdown']} | "
            f"Sustainability robustness: {sust_sens['breakdown']}"
        )
        
        stability = classify_stability(sensitivity_range)

        # 8️⃣ Collect Evaluation Result
        evaluations.append(
            OptionEvaluation(
                title=option.title,
                growth_score=growth,
                sustainability_score=sustainability,
                tension_index=tension,
                tension_severity=tension_severity,
                zone=zone,
                zone_reason=zone_reason,
                composite_score=comp,
                risk_level=risk,
                triggered_messages=triggers,
                sensitivity_range=sensitivity_range,
                stability_level=stability,
                sensitivity_breakdown=sensitivity_breakdown
            )
        )

    # --------------------------------------------------
    # Sort by Composite Score (Descending)
    # --------------------------------------------------
    sorted_options = sorted(
        evaluations,
        key=lambda x: x.composite_score,
        reverse=True
    )

    # --------------------------------------------------
    # Single Option Mode
    # --------------------------------------------------
    if len(sorted_options) == 1:
        single = sorted_options[0]

        return CompareResponse(
            evaluations=sorted_options,
            recommended_option=single.title,
            decision_status="SINGLE_OPTION_CLASSIFIED",
            recommendation_reason="Single option structurally evaluated and classified."
        )

    # --------------------------------------------------
    # Multi-Option Mode
    # --------------------------------------------------
    if detect_close_competition(sorted_options):
        return CompareResponse(
            evaluations=sorted_options,
            recommended_option="NO_CLEAR_WINNER",
            decision_status="CLOSE_COMPETITION",
            recommendation_reason="Top options have very similar composite scores."
        )

    winner = sorted_options[0]

    return CompareResponse(
        evaluations=sorted_options,
        recommended_option=winner.title,
        decision_status="CLEAR_WINNER",
        recommendation_reason=f"Highest composite score ({winner.composite_score})."
    )


@app.post("/decision/reflect", response_model=ReflectionResponse)
def reflect(request: ReflectionRequest):
    """
    Get Absolem's reflective wisdom on the decision.
    
    This endpoint provides:
    - Absolem's review of the algorithm's recommendation
    - Consideration of human factors and emotions
    - Burnout prevention action plan
    - Before-you-decide suggestions based on real-life scenarios
    
    Includes mitigation strategies:
    - Falls back to default wisdom if API unavailable
    - Caches responses to reduce API calls
    - Monitors usage statistics
    """
    try:
        # Get Absolem's wisdom using reflection engine
        wisdom = get_absolem_wisdom(
            options=request.options,
            comparison_result=request.comparison_result
        )
        
        return ReflectionResponse(
            algorithm_decision=wisdom.get("algorithm_decision", {}),
            action_plan=wisdom.get("action_plan", []),
            before_you_decide=wisdom.get("before_you_decide", {}),
            source=wisdom.get("source", "Unknown")
        )
    
    except Exception as e:
        # Fallback to default wisdom on any error
        from app.engine.ai_reflector import ABSOLEM_FALLBACK_WISDOM
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Reflection error: {e}. Using fallback wisdom.")
        
        fallback = ABSOLEM_FALLBACK_WISDOM
        return ReflectionResponse(
            algorithm_decision=fallback.get("algorithm_decision", {}),
            action_plan=fallback.get("action_plan", []),
            before_you_decide=fallback.get("before_you_decide", {}),
            source=f"{fallback.get('source', 'Unknown')} (error: {str(e)[:50]})"
        )


@app.get("/stats")
def get_stats():
    """
    Get usage statistics for the AI reflection layer.
    Useful for monitoring API usage and ensuring we stay within free tier limits.
    """
    from app.engine.ai_reflector import get_reflector
    reflector = get_reflector()
    
    return {
        "ai_reflection_stats": reflector.get_usage_stats(),
        "message": "Monitor these stats to ensure you stay within Gemini's free tier (1500 requests/day)"
    }


@app.get("/api/rate-limits")
def get_rate_limits():
    """
    Get daily API call rate limit information.
    
    RATE LIMIT POLICY:
    - Max calls per day: 50 (recommended for smooth operation)
    - Reason: Balances free API tier usage with user experience
    - Caching: Reuses responses for 24 hours (doesn't count against limit)
    - Reset: Daily at 00:00 UTC
    
    Returns:
        {
            "max_calls_per_day": 50,
            "calls_used_today": 3,
            "calls_remaining": 47,
            "percentage_used": 6,
            "reset_time": "2026-03-02T00:00:00Z",
            "status": "OK | WARNING (<=5 left) | EXCEEDED",
            "gemini_available": boolean
        }
    
    Recommendations:
    - Green (OK): No action needed
    - Yellow (WARNING): Approaching limit, encourage caching/reusing decisions
    - Red (EXCEEDED): Use fallback wisdom until tomorrow's reset
    """
    from app.engine.ai_reflector import get_reflector
    reflector = get_reflector()
    
    return reflector.get_daily_limits_info()