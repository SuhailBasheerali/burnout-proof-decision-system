def detect_close_competition(sorted_options, threshold=5):
    """
    Determines whether the top two options are too close in composite score
    to confidently declare a winner. Adjusts threshold based on stability levels.
    
    Logic:
    - Both STABLE: Use normal threshold (5 points) - scores are reliable
    - Mixed stability: Use higher threshold (8 points) - one is unreliable
    - Either FRAGILE: Use highest threshold (12 points) - top choice is shaky
    """

    if len(sorted_options) < 2:
        return False

    top_option = sorted_options[0]
    second_option = sorted_options[1]
    
    top_score = top_option.composite_score
    second_score = second_option.composite_score
    difference = top_score - second_score
    
    # Determine stability context
    top_stable = top_option.stability_level
    second_stable = second_option.stability_level
    
    # Adjust threshold based on stability context
    if top_stable == "FRAGILE" or second_stable == "FRAGILE":
        adjusted_threshold = 12  # Very conservative when fragile option involved
    elif top_stable != second_stable:  # Mixed (one STABLE, one not)
        adjusted_threshold = 8  # More conservative with mixed stability
    else:  # Both same stability level
        if top_stable == "STABLE":
            adjusted_threshold = 5  # Normal threshold for stable decisions
        else:  # Both MODERATELY_STABLE or worse
            adjusted_threshold = 8  # More conservative for moderate areas
    
    return difference < adjusted_threshold