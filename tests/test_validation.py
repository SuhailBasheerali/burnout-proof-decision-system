from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_empty_options():
    response = client.post("/decision/compare", json={"options": []})
    assert response.status_code == 422


def test_weight_out_of_range():
    payload = {
        "options": [
            {
                "title": "Invalid",
                "growth_criteria": [{"weight": 15, "impact": 5}],
                "sustainability_criteria": [{"weight": 5, "impact": 5}]
            }
        ]
    }

    response = client.post("/decision/compare", json=payload)
    assert response.status_code == 422


def test_missing_growth():
    payload = {
        "options": [
            {
                "title": "Invalid",
                "sustainability_criteria": [{"weight": 5, "impact": 5}]
            }
        ]
    }

    response = client.post("/decision/compare", json=payload)
    assert response.status_code == 422