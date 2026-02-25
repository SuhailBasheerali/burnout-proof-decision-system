def normalize_score(criteria):
    raw = sum(c.weight * c.impact for c in criteria)
    max_possible = len(criteria) * 100
    if max_possible == 0:
        return 0
    return round((raw / max_possible) * 100, 2)