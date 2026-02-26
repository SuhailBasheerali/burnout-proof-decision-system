def generate_triggers(growth, sustainability, tension, tension_severity, zone):
    messages = []

    if growth >= 70 and sustainability < 50:
        messages.append("High growth with sustainability deficit detected.")

    if sustainability < 40:
        messages.append("Sustainability below structural stability threshold.")

    if tension_severity in ["HIGH", "CRITICAL"]:
        messages.append("Significant imbalance between growth and sustainability.")

    if zone == "AVOID":
        messages.append("Low structural value across both dimensions.")

    if growth < 40 and sustainability >= 70:
        messages.append("Recovery-dominant decision structure detected.")

    return messages