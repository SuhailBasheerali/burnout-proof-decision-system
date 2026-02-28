def normalize_score(criteria):
    if not criteria:
        return 0

    total_weighted = sum(c.weight * c.impact for c in criteria)
    total_weight = sum(c.weight for c in criteria)

    if total_weight == 0:
        return 0

    weighted_avg = total_weighted / total_weight
    return round(weighted_avg * 10, 2)

def composite_score(growth, sustainability):
    """
    Computes composite viability score with asymmetric burnout penalty.
    
    Mathematical formulation:
    - Base score: arithmetic mean of growth and sustainability
    - Asymmetric penalty: 0.3x for growth > sustainability (burnout trap)
                         0.1x for sustainability > growth (stagnation)
    - Quadratic penalty: additional penalty for extreme imbalances
    
    This ensures growth-dominant imbalances are penalized 3x more severely,
    addressing the critical burnout risk of high growth + low sustainability.
    
    INTERPRETATION NOTE:
    This formula prioritizes BALANCE. A 50/50 option scores higher than 90/10 because:
    - Perfect balance at 50: Composite = 50 (reliable)
    - High imbalance (90/10): Composite ≈ 25 (risky)
    
    This is INTENTIONAL - the system avoids high-risk, high-reward patterns.
    Use sensitivity_range/stability_level to understand confidence in any decision.
    """
    base = (growth + sustainability) / 2
    
    # Asymmetric penalty: burnout (high growth, low sustainability) is worse
    growth_dominant = max(0, growth - sustainability)
    sustainability_dominant = max(0, sustainability - growth)
    
    asymmetric_penalty = (0.3 * growth_dominant) + (0.1 * sustainability_dominant)
    
    # Quadratic penalty for extreme imbalances (tension > 50)
    tension = abs(growth - sustainability)
    quadratic_penalty = 0.05 * (tension ** 2) / 100  # Scales 0-5 points for extreme cases
    
    adjusted = base - asymmetric_penalty - quadratic_penalty
    
    return round(max(adjusted, 0), 2)