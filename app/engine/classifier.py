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
    Enhanced risk classification with growth deficit detection.
    
    Priority hierarchy:
    1. Structural rejection (AVOID zone)
    2. Severe burnout imbalance (CRITICAL tension from high growth, low sustainability)
    3. Sustainability deficit (explicit low sustainability)
    4. Growth stagnation deficit (implicit growth risk)
    5. Default stable classification
    
    This hierarchy appropriately penalizes both extreme burnout AND stagnation risks.
    """
    # Highest priority: structural rejection
    if zone == "AVOID":
        return "LOW_STRUCTURAL_VALUE"

    # Critical burnout detection: high growth with critically low sustainability
    if tension_severity == "CRITICAL" and growth > sustainability:
        return "SEVERE_BURNOUT_RISK"

    # General severe imbalance
    if tension_severity == "CRITICAL":
        return "SEVERE_IMBALANCE"

    # Explicit sustainability deficit
    if sustainability < 40:
        return "SUSTAINABILITY_DEFICIT"
    
    # Growth deficit risk: low growth indicates stagnation
    # (especially problematic in LIGHT_RECOVERY zone which suggests low growth)
    if growth < 40 and zone != "STEADY_EXECUTION":
        return "GROWTH_STAGNATION_RISK"

    return "STRUCTURALLY_STABLE"