def generate_triggers(growth, sustainability, tension, tension_severity, zone):
    """
    Generates contextual warning messages based on decision structure.
    Prioritizes burnout detection (high growth + low sustainability).
    Uses deduplication to avoid message overlap.
    """
    messages = []
    sustainability_flagged = False  # Track if we've already flagged sustainability
    growth_flagged = False          # Track if we've already flagged growth

    # BURNOUT TRAP DETECTION - PRIMARY (highest concern)
    if growth >= 75 and sustainability < 35:
        messages.append("⚠️ CRITICAL: Burnout trap detected - high growth demands exceed sustainability capacity.")
        sustainability_flagged = True
        growth_flagged = True
    elif growth >= 70 and sustainability < 50:
        messages.append("⚠️ HIGH BURNOUT RISK: Growth demands exceed sustainability capacity - monitoring required.")
        sustainability_flagged = True
        growth_flagged = True

    # SUSTAINABILITY DEFICIT (only if not already covered by burnout trap)
    if not sustainability_flagged and sustainability < 40:
        messages.append("⚠️ Sustainability below structural stability threshold.")
        sustainability_flagged = True

    # SEVERE IMBALANCE (HIGH or CRITICAL tension, excluding already-covered cases)
    if not sustainability_flagged and not growth_flagged and tension_severity in ["HIGH", "CRITICAL"]:
        messages.append("⚠️ Significant imbalance between growth and sustainability - verify trade-off acceptance.")

    # STRUCTURAL REJECTION
    if zone == "AVOID":
        messages.append("🛑 Low structural value across both dimensions - reconsider option fundamentally.")

    # SEVERE STAGNATION (opposite of burnout)
    if not growth_flagged and growth < 40 and sustainability >= 70:
        messages.append("⚠️ Stagnation risk: High sustainability with low growth may indicate missed opportunities.")
        growth_flagged = True
    elif not growth_flagged and growth < 40:
        messages.append("⚠️ Growth threshold concern: Below optimal growth level - consider impact scope.")
        growth_flagged = True

    return messages