from fastapi import FastAPI, HTTPException
from app.schemas import CompareRequest, CompareResponse
from typing import List


app = FastAPI(title="Burnout-Proof Decision Engine")


@app.get("/")
def root():
    return {"status": "Deterministic Multi-Option Core Active"}


# ----------------------------
# Utility Functions
# ----------------------------

def normalize_score(criteria):
    raw = sum(c.weight * c.impact for c in criteria)
    max_possible = len(criteria) * 100
    if max_possible == 0:
        return 0
    return round((raw / max_possible) * 100, 2)


def classify_zone(growth, sustainability):
    if growth >= 70 and sustainability >= 70:
        return "EXECUTE_FULLY", "High growth and sustainable"
    elif growth >= 70 and sustainability < 50:
        return "TIME_BOX", "High growth but low sustainability"
    elif growth < 50 and sustainability >= 70:
        return "LIGHT_RECOVERY", "Low growth but strong sustainability"
    elif growth < 40 and sustainability < 40:
        return "AVOID", "Low growth and low sustainability"
    else:
        return "STEADY_EXECUTION", "Balanced moderate scores"


def classify_tension(tension):
    if tension <= 10:
        return "LOW"
    elif tension <= 25:
        return "MODERATE"
    elif tension <= 50:
        return "HIGH"
    return "CRITICAL"


def composite_score(growth, sustainability, tension_severity):
    score = (growth * 0.5) + (sustainability * 0.5)

    if tension_severity == "HIGH":
        score *= 0.9
    elif tension_severity == "CRITICAL":
        score *= 0.8

    return round(score, 2)


def detect_close_competition(sorted_options, threshold=5):
    if len(sorted_options) < 2:
        return False
    diff = sorted_options[0]["composite_score"] - sorted_options[1]["composite_score"]
    return diff < threshold


# ----------------------------
# Multi-Option Comparison Endpoint
# ----------------------------

@app.post("/decision/compare", response_model=CompareResponse)
def compare(request: CompareRequest):

    if len(request.options) < 2:
        raise HTTPException(
            status_code=400,
            detail="At least two options required for comparison."
        )

    evaluations = []

    for option in request.options:

        growth = normalize_score(option.growth_criteria)
        sustainability = normalize_score(option.sustainability_criteria)

        tension = abs(growth - sustainability)
        tension_severity = classify_tension(tension)

        zone, reason = classify_zone(growth, sustainability)

        comp = composite_score(growth, sustainability, tension_severity)

        evaluations.append({
            "title": option.title,
            "growth_score": growth,
            "sustainability_score": sustainability,
            "tension_index": tension,
            "tension_severity": tension_severity,
            "zone": zone,
            "zone_reason": reason,
            "composite_score": comp
        })

    sorted_options = sorted(
        evaluations,
        key=lambda x: x["composite_score"],
        reverse=True
    )

    if detect_close_competition(sorted_options):
        return {
            "evaluations": sorted_options,
            "recommended_option": "NO_CLEAR_WINNER",
            "decision_status": "CLOSE_COMPETITION",
            "recommendation_reason": "Top options have very similar composite scores."
        }

    winner = sorted_options[0]

    return {
        "evaluations": sorted_options,
        "recommended_option": winner["title"],
        "decision_status": "CLEAR_WINNER",
        "recommendation_reason": f"Highest composite score ({winner['composite_score']})."
    }