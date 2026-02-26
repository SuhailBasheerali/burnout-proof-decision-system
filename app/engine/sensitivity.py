def perform_sensitivity_analysis(criteria, normalize_fn):
    """
    Performs robustness assessment using ±20% weight perturbations.
    
    Increased from ±10% to better capture structural fragility:
    - ±10% is too small for minor criteria (weight 1-3)
    - ±20% better represents realistic estimation uncertainty
    - Provides stronger signal for stability classification
    """
    if not criteria:
        return 0

    # Increase weights by 20% (capped at 10)
    increased = [
        type(c)(weight=min(c.weight * 1.2, 10), impact=c.impact)
        for c in criteria
    ]

    # Decrease weights by 20% (floored at 0)
    decreased = [
        type(c)(weight=max(c.weight * 0.8, 0), impact=c.impact)
        for c in criteria
    ]

    high_score = normalize_fn(increased)
    low_score = normalize_fn(decreased)

    return round(abs(high_score - low_score), 2)


def classify_stability(sensitivity_range):
    """
    Classifies robustness based on sensitivity range from ±20% perturbations.
    
    - STABLE: variance < 8 (tight, resilient)
    - MODERATELY_STABLE: variance 8-20 (acceptable, normal)
    - FRAGILE: variance >= 20 (high variance, fragile)
    
    Thresholds adjusted for ±20% perturbations (versus prior ±10%).
    """
    if sensitivity_range < 8:
        return "STABLE"
    elif sensitivity_range < 20:
        return "MODERATELY_STABLE"
    return "FRAGILE"