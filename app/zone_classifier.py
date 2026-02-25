def classify_zone(growth, sustainability):
    if growth >= 60 and sustainability >= 60:
        return "EXECUTE_FULLY"
    elif growth >= 60 and sustainability < 60:
        return "TIME_BOX"
    elif growth < 60 and sustainability >= 60:
        return "LIGHT_RECOVERY"
    elif growth < 40 and sustainability < 40:
        return "AVOID"
    else:
        return "STEADY_EXECUTION"