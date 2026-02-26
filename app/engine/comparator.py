def detect_close_competition(sorted_options, threshold=5):
    """
    Determines whether the top two options are too close
    in composite score to confidently declare a winner.
    """

    if len(sorted_options) < 2:
        return False

    top_score = sorted_options[0]["composite_score"]
    second_score = sorted_options[1]["composite_score"]

    difference = top_score - second_score

    return difference < threshold