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
    
    Returns:
    {
        'weight_sensitivity': variance from weight perturbations,
        'impact_sensitivity': variance from impact perturbations,
        'combined_sensitivity': max of both (worst-case),
        'breakdown': which dimension is more fragile
    }
    """
    if not criteria:
        return {
            'weight_sensitivity': 0,
            'impact_sensitivity': 0,
            'combined_sensitivity': 0,
            'breakdown': 'N/A'
        }

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
    
    # --- DETERMINE WHICH DIMENSION IS MORE FRAGILE ---
    if weight_variance > impact_variance:
        breakdown = f"Importance estimates are less reliable (±{weight_variance:.1f}pts vs ±{impact_variance:.1f}pts)"
    elif impact_variance > weight_variance:
        breakdown = f"Effect/impact estimates are less reliable (±{impact_variance:.1f}pts vs ±{weight_variance:.1f}pts)"
    else:
        breakdown = f"Both dimensions equally fragile (±{weight_variance:.1f}pts)"
    
    # --- COMBINED SENSITIVITY ---
    # Return maximum of weight and impact variances to capture worst-case
    combined_variance = max(weight_variance, impact_variance)
    
    return {
        'weight_sensitivity': round(weight_variance, 2),
        'impact_sensitivity': round(impact_variance, 2),
        'combined_sensitivity': round(combined_variance, 2),
        'breakdown': breakdown
    }


def classify_stability(sensitivity_dict):
    """
    Classifies robustness based on sensitivity range from ±20% perturbations.
    
    Uses combined_sensitivity (worst-case) for classification:
    - STABLE: variance < 8 (tight, resilient)
    - MODERATELY_STABLE: variance 8-20 (acceptable, normal)
    - FRAGILE: variance >= 20 (high variance, fragile)
    
    Args:
        sensitivity_dict: Dict with 'combined_sensitivity' key or legacy float
    """
    if isinstance(sensitivity_dict, dict):
        sensitivity_range = sensitivity_dict.get('combined_sensitivity', 0)
    else:
        # Legacy support for float values
        sensitivity_range = sensitivity_dict
    
    if sensitivity_range < 8:
        return "STABLE"
    elif sensitivity_range < 20:
        return "MODERATELY_STABLE"
    return "FRAGILE"