def generate_triggers(growth, sustainability, tension, tension_severity, zone):
    """
    Generates contextual warning messages based on decision structure.
    Prioritizes burnout detection (high growth + low sustainability).
    """
    messages = []

    # Burnout trap detection: extreme growth-to-sustainability gap
    if growth >= 75 and sustainability < 35:
        messages.append("⚠️ CRITICAL: Burnout trap detected - high growth demands exceed sustainability capacity.")
    elif growth >= 70 and sustainability < 50:
        messages.append("High growth with sustainability deficit detected - burnout risk present.")

    # Sustainability deficit coverage
    if sustainability < 40:
        messages.append("Sustainability below structural stability threshold.")

    # General severe imbalance
    if tension_severity in ["HIGH", "CRITICAL"] and not any("CRITICAL" in m for m in messages):
        messages.append("Significant imbalance between growth and sustainability.")

    # Structural rejection
    if zone == "AVOID":
        messages.append("Low structural value across both dimensions.")

    # Growth stagnation risk (opposite of burnout)
    if growth < 40 and sustainability >= 70:
        messages.append("Recovery-dominant decision structure detected - low growth may indicate stagnation.")
    elif growth < 40:
        messages.append("Growth below minimum threshold - consider lower-impact commitment.")

    return messages