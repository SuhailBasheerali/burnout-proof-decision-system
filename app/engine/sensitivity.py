def perform_sensitivity_analysis(criteria, normalize_fn):
    if not criteria:
        return 0

    increased = [
        type(c)(weight=min(c.weight * 1.1, 10), impact=c.impact)
        for c in criteria
    ]

    decreased = [
        type(c)(weight=max(c.weight * 0.9, 0), impact=c.impact)
        for c in criteria
    ]

    high_score = normalize_fn(increased)
    low_score = normalize_fn(decreased)

    return round(abs(high_score - low_score), 2)


def classify_stability(sensitivity_range):
    if sensitivity_range < 5:
        return "STABLE"
    elif sensitivity_range < 15:
        return "MODERATELY_STABLE"
    return "FRAGILE"