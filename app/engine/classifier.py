def classify_zone(growth, sustainability):
    if growth >= 70 and sustainability >= 70:
        return "EXECUTE_FULLY", "High growth and sustainable"

    if growth >= 70 and sustainability < 50:
        return "TIME_BOX", "High growth but sustainability deficit"

    if growth < 50 and sustainability >= 70:
        return "LIGHT_RECOVERY", "Low growth but strong recovery capacity"

    if growth < 40 and sustainability < 40:
        return "AVOID", "Low structural viability"

    return "STEADY_EXECUTION", "Balanced moderate scores"


def classify_tension(tension):
    if tension <= 15:
        return "LOW"
    elif tension <= 30:
        return "MODERATE"
    elif tension <= 60:
        return "HIGH"
    return "CRITICAL"

def classify_risk(zone, tension_severity, growth, sustainability):
    """
    Enhanced risk classification with burnout ratio detection and growth deficit handling.
    
    Priority hierarchy:
    1. Structural rejection (AVOID zone)
    2. Severe burnout imbalance (CRITICAL tension OR high ratio from growth > sustainability)
    3. Sustainability deficit (explicit low sustainability)
    4. Growth stagnation deficit (implicit growth risk)
    5. Severe stagnation (low sustainability with high sustainability-dominant tension)
    6. Default stable classification
    
    This hierarchy catches both extreme imbalances (CRITICAL) and sneaky imbalances
    (HIGH tension with dangerous ratios like 80 growth, 30 sustainability).
    """
    # Highest priority: structural rejection
    if zone == "AVOID":
        return "STRUCTURALLY_UNSALVAGEABLE"

    # BURNOUT DETECTION - Two pathways:
    # Pathway 1: CRITICAL tension with growth dominance
    if tension_severity == "CRITICAL" and growth > sustainability:
        return "SEVERE_BURNOUT_RISK"
    
    # Pathway 2: HIGH tension with dangerous growth ratio (>2x sustainability)
    # Catches: Growth 80, Sustainability 30 (ratio 2.67x, tension 50=HIGH)
    if tension_severity == "HIGH" and growth > sustainability:
        ratio = growth / max(sustainability, 1)  # Avoid division by zero
        if ratio >= 2.0:  # Growth is 2x or more than sustainability
            return "SEVERE_BURNOUT_RISK"

    # General severe imbalance (non-burnout orientation)
    if tension_severity == "CRITICAL":
        return "SEVERE_IMBALANCE"

    # Explicit sustainability deficit
    if sustainability < 40:
        return "SUSTAINABILITY_DEFICIT"
    
    # Severe stagnation: High tension with sustainability dominance
    if tension_severity == "HIGH" and sustainability > growth:
        ratio = sustainability / max(growth, 1)
        if ratio >= 1.5:  # Sustainability is 1.5x+ more than growth
            return "SEVERE_STAGNATION_RISK"
    
    # Growth deficit risk: low growth indicates stagnation
    # (especially problematic in LIGHT_RECOVERY zone which suggests low growth)
    if growth < 40 and zone != "STEADY_EXECUTION":
        return "GROWTH_STAGNATION_RISK"

    return "STRUCTURALLY_STABLE"