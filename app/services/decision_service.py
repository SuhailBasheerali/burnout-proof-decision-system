from fastapi import HTTPException

from app.engine.classifier import (
    classify_risk,
    classify_tension,
    classify_zone,
)
from app.engine.comparator import detect_close_competition
from app.engine.evaluator import composite_score, normalize_score
from app.engine.sensitivity import (
    classify_stability,
    perform_sensitivity_analysis,
)
from app.engine.triggers import generate_triggers
from app.schemas import CompareRequest, CompareResponse, OptionEvaluation


def compare_decision_options(request: CompareRequest) -> CompareResponse:

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
    # Check if all options are below viability threshold (40) FIRST
    # This is more critical than CLOSE_COMPETITION
    if all(opt.composite_score < 40 for opt in sorted_options):
        return CompareResponse(
            evaluations=sorted_options,
            recommended_option="NONE_VIABLE",
            decision_status="ALL_OPTIONS_POOR_FIT",
            recommendation_reason="All options score below viability threshold (40). No viable option exists—consider redesigning the problem."
        )

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
