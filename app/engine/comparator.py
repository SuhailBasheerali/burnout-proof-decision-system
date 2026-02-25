def composite_score(growth, sustainability, tension_severity):
    score = (growth * 0.5) + (sustainability * 0.5)

    if tension_severity == "HIGH":
        score *= 0.9
    elif tension_severity == "CRITICAL":
        score *= 0.8

    return round(score, 2)


def detect_close_competition(sorted_options, threshold=5):
    if len(sorted_options) < 2:
        return False

    diff = sorted_options[0]["composite_score"] - sorted_options[1]["composite_score"]
    return diff < threshold