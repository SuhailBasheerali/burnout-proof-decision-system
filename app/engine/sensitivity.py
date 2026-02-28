def perform_sensitivity_analysis(criteria, normalize_fn):
    """
    Performs comprehensive robustness assessment using ±20% weight & ±15% impact perturbations.
    
    Tests BOTH weight and impact variations to catch multiple failure modes:
    - ±20% weight changes: Tests importance estimation accuracy
    - ±15% impact changes: Tests magnitude/effect estimation accuracy
    
    Why both?
    - A decision could be robust to weight changes but fragile to impact misestimation
    - Example: Task importance (weight) estimated correctly, but actual impact (complexity/effect) underestimated
    - Testing both provides holistic robustness assessment
    
    Thresholds chosen to represent realistic estimation uncertainty:
    - ±20% weight: Accounts for importance/priority misjudgment
    - ±15% impact: Accounts for effect/magnitude misjudgment
    - Returns worst-case variance to be conservative
    """
    if not criteria:
        return 0

    # --- WEIGHT PERTURBATIONS (±20%) ---
    # Increase weights by 20% (capped at 10)
    increased_weight = [
        type(c)(weight=min(c.weight * 1.2, 10), impact=c.impact)
        for c in criteria
    ]

    # Decrease weights by 20% (floored at 0)
    decreased_weight = [
        type(c)(weight=max(c.weight * 0.8, 0), impact=c.impact)
        for c in criteria
    ]

    weight_high = normalize_fn(increased_weight)
    weight_low = normalize_fn(decreased_weight)
    weight_variance = abs(weight_high - weight_low)
    
    # --- IMPACT PERTURBATIONS (±15%) ---
    # Increase impact by 15% (capped at 10)
    increased_impact = [
        type(c)(weight=c.weight, impact=min(int(c.impact * 1.15), 10))
        for c in criteria
    ]

    # Decrease impact by 15% (floored at 0)
    decreased_impact = [
        type(c)(weight=c.weight, impact=max(int(c.impact * 0.85), 0))
        for c in criteria
    ]

    impact_high = normalize_fn(increased_impact)
    impact_low = normalize_fn(decreased_impact)
    impact_variance = abs(impact_high - impact_low)
    
    # --- COMBINED SENSITIVITY ---
    # Return maximum of weight and impact variances to capture worst-case
    # If decision fails with either weight OR impact perturbations, it's fragile
    combined_variance = max(weight_variance, impact_variance)
    
    return round(combined_variance, 2)


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