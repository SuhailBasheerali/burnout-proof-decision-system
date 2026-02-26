from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def valid_payload():
    return {
        "options": [
            {
                "title": "Test Option",
                "growth_criteria": [{"weight": 8, "impact": 9}],
                "sustainability_criteria": [{"weight": 6, "impact": 7}]
            }
        ]
    }


# ---------------------------
# Basic Success Case
# ---------------------------
def test_single_option_success():
    response = client.post("/decision/compare", json=valid_payload())
    assert response.status_code == 200

    data = response.json()
    assert "evaluations" in data
    assert data["decision_status"] == "SINGLE_OPTION_CLASSIFIED"


# ---------------------------
# Duplicate Title
# ---------------------------
def test_duplicate_titles():
    payload = {
        "options": [
            valid_payload()["options"][0],
            valid_payload()["options"][0],
        ]
    }

    response = client.post("/decision/compare", json=payload)
    assert response.status_code == 400


# ---------------------------
# Close Competition
# ---------------------------
def test_close_competition():
    payload = {
        "options": [
            {
                "title": "A",
                "growth_criteria": [{"weight": 8, "impact": 8}],
                "sustainability_criteria": [{"weight": 8, "impact": 8}]
            },
            {
                "title": "B",
                "growth_criteria": [{"weight": 8, "impact": 8}],
                "sustainability_criteria": [{"weight": 8, "impact": 8}]
            }
        ]
    }

    response = client.post("/decision/compare", json=payload)
    assert response.status_code == 200
    assert response.json()["decision_status"] == "CLOSE_COMPETITION"


# ---------------------------
# Extreme Imbalance
# ---------------------------
def test_extreme_imbalance():
    payload = {
        "options": [
            {
                "title": "Extreme",
                "growth_criteria": [{"weight": 10, "impact": 10}],
                "sustainability_criteria": [{"weight": 1, "impact": 1}]
            }
        ]
    }

    response = client.post("/decision/compare", json=payload)
    data = response.json()

    eval_data = data["evaluations"][0]
    assert eval_data["tension_severity"] in ["HIGH", "CRITICAL"]
    assert eval_data["composite_score"] <= 100


# ---------------------------
# Boundary 40
# ---------------------------
def test_boundary_40():
    payload = {
        "options": [
            {
                "title": "Boundary",
                "growth_criteria": [{"weight": 4, "impact": 10}],
                "sustainability_criteria": [{"weight": 4, "impact": 10}]
            }
        ]
    }

    response = client.post("/decision/compare", json=payload)
    assert response.status_code == 200