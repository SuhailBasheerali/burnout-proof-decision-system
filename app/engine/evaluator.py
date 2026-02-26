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
    base = (growth + sustainability) / 2
    tension = abs(growth - sustainability)

    imbalance_penalty = tension * 0.2
    adjusted = base - imbalance_penalty

    return round(max(adjusted, 0), 2)