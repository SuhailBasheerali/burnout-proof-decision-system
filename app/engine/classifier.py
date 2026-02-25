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