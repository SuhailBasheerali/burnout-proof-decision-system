from app.engine.evaluator import normalize_score, composite_score
from app.engine.classifier import classify_zone, classify_tension
from app.engine.sensitivity import classify_stability


class Dummy:
    def __init__(self, weight, impact):
        self.weight = weight
        self.impact = impact


def test_normalization_weighted_mean():
    criteria = [Dummy(10, 10)]
    score = normalize_score(criteria)
    assert score == 100


def test_zero_weight():
    criteria = [Dummy(0, 10)]
    score = normalize_score(criteria)
    assert score == 0


def test_composite_penalty():
    comp = composite_score(100, 0)
    assert comp < 50  # heavy imbalance penalty


def test_zone_execute():
    zone, _ = classify_zone(80, 80)
    assert zone == "EXECUTE_FULLY"


def test_zone_avoid():
    zone, _ = classify_zone(10, 10)
    assert zone == "AVOID"


def test_tension_classification():
    severity = classify_tension(70)
    assert severity == "CRITICAL"


def test_stability_classification():
    assert classify_stability(3) == "STABLE"
    assert classify_stability(10) == "MODERATELY_STABLE"
    assert classify_stability(20) == "FRAGILE"