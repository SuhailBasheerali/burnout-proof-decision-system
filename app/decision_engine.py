def calculate_score(criteria):
    return sum(c.weight * c.impact for c in criteria)