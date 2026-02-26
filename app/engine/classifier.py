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

def classify_risk(zone, tension_severity, sustainability):
    if zone == "AVOID":
        return "LOW_STRUCTURAL_VALUE"

    if tension_severity == "CRITICAL":
        return "SEVERE_IMBALANCE"

    if sustainability < 40:
        return "SUSTAINABILITY_DEFICIT"

    return "STRUCTURALLY_STABLE"