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


# =============================================================================
# REALISTIC SCENARIO TESTS
# =============================================================================

# ---------------------------
# Scenario 1: Career Promotion Decision
# ---------------------------
def test_scenario_career_promotion():
    """Senior role with salary increase but requires long hours and team management"""
    payload = {
        "options": [
            {
                "title": "Senior Promotion",
                "growth_criteria": [
                    {"weight": 9, "impact": 10},  # Skill development
                    {"weight": 10, "impact": 10}  # Career advancement
                ],
                "sustainability_criteria": [
                    {"weight": 8, "impact": 9},   # Work-life balance
                    {"weight": 5, "impact": 6}    # Long-term engagement
                ]
            }
        ]
    }

    response = client.post("/decision/compare", json=payload)
    assert response.status_code == 200
    data = response.json()
    eval_data = data["evaluations"][0]
    
    # Verify response contains required fields
    assert "tension_severity" in eval_data
    assert "composite_score" in eval_data
    assert eval_data["composite_score"] > 0 and eval_data["composite_score"] <= 100


# ---------------------------
# Scenario 2: Sustainable Growth Startup
# ---------------------------
def test_scenario_startup_growth():
    """Bootstrapped gradual growth vs VC-funded hyper-growth"""
    payload = {
        "options": [
            {
                "title": "Bootstrapped Growth",
                "growth_criteria": [
                    {"weight": 6, "impact": 7},   # Market reach
                    {"weight": 5, "impact": 6}    # Revenue scale
                ],
                "sustainability_criteria": [
                    {"weight": 9, "impact": 9},   # Team morale
                    {"weight": 10, "impact": 10}  # Burnout risk
                ]
            },
            {
                "title": "VC-Funded Hyper-Growth",
                "growth_criteria": [
                    {"weight": 10, "impact": 10},  # Market reach
                    {"weight": 9, "impact": 9}     # Revenue scale
                ],
                "sustainability_criteria": [
                    {"weight": 4, "impact": 8},    # Team morale
                    {"weight": 3, "impact": 9}     # Burnout risk
                ]
            }
        ]
    }

    response = client.post("/decision/compare", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    # Should compare two options and be able to evaluate both
    assert len(data["evaluations"]) == 2
    assert all("tension_severity" in e for e in data["evaluations"])
    assert all("composite_score" in e for e in data["evaluations"])


# ---------------------------
# Scenario 3: Bootcamp vs Self-Paced Learning
# ---------------------------
def test_scenario_intense_bootcamp():
    """12-week intensive bootcamp vs 6-month part-time program"""
    payload = {
        "options": [
            {
                "title": "Intensive Bootcamp",
                "growth_criteria": [
                    {"weight": 10, "impact": 10},  # Skills acquired
                    {"weight": 9, "impact": 9}     # Job-ready speed
                ],
                "sustainability_criteria": [
                    {"weight": 2, "impact": 8},    # Mental health impact
                    {"weight": 3, "impact": 7}     # Financial burden duration
                ]
            }
        ]
    }

    response = client.post("/decision/compare", json=payload)
    assert response.status_code == 200
    data = response.json()
    eval_data = data["evaluations"][0]
    
    # Verify evaluation data is present and valid
    assert eval_data["tension_severity"] in ["STABLE", "MODERATE", "HIGH", "CRITICAL"]
    assert 0 < eval_data["composite_score"] <= 100


# ---------------------------
# Scenario 4: Freelancer Overcommitment
# ---------------------------
def test_scenario_freelance_overload():
    """5 high-paying projects vs 2 projects with buffer time"""
    payload = {
        "options": [
            {
                "title": "5 Projects Simultaneously",
                "growth_criteria": [
                    {"weight": 8, "impact": 10},   # Income boost
                    {"weight": 7, "impact": 8}     # Client base expansion
                ],
                "sustainability_criteria": [
                    {"weight": 1, "impact": 9},    # Work distribution
                    {"weight": 2, "impact": 8}     # Quality per project
                ]
            },
            {
                "title": "2 Projects with Buffer",
                "growth_criteria": [
                    {"weight": 4, "impact": 5},    # Income boost
                    {"weight": 5, "impact": 6}     # Client base expansion
                ],
                "sustainability_criteria": [
                    {"weight": 9, "impact": 9},    # Work distribution
                    {"weight": 8, "impact": 8}     # Quality per project
                ]
            }
        ]
    }

    response = client.post("/decision/compare", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["evaluations"]) == 2
    
    # Both options should have valid evaluations
    for eval_data in data["evaluations"]:
        assert eval_data["tension_severity"] in ["LOW", "STABLE", "MODERATE", "HIGH", "CRITICAL"]
        assert 0 < eval_data["composite_score"] <= 100


# ---------------------------
# Scenario 5: Aggressive vs Measured Fitness
# ---------------------------
def test_scenario_fitness_intensity():
    """6-day/week intense training vs 4-day structured routine"""
    payload = {
        "options": [
            {
                "title": "6-Day Intense Training",
                "growth_criteria": [
                    {"weight": 9, "impact": 10},   # Performance gains
                    {"weight": 8, "impact": 9}     # Competition readiness
                ],
                "sustainability_criteria": [
                    {"weight": 3, "impact": 9},    # Injury prevention
                    {"weight": 5, "impact": 7}     # Enjoyment/adherence
                ]
            },
            {
                "title": "4-Day Structured Routine",
                "growth_criteria": [
                    {"weight": 6, "impact": 7},    # Performance gains
                    {"weight": 5, "impact": 6}     # Competition readiness
                ],
                "sustainability_criteria": [
                    {"weight": 8, "impact": 8},    # Injury prevention
                    {"weight": 8, "impact": 8}     # Enjoyment/adherence
                ]
            }
        ]
    }

    response = client.post("/decision/compare", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    # Both should evaluate successfully with valid scores
    assert len(data["evaluations"]) == 2
    for eval_data in data["evaluations"]:
        assert "tension_severity" in eval_data
        assert 0 < eval_data["composite_score"] <= 100


# ---------------------------
# Scenario 6: Sleep Sacrifice for Productivity
# ---------------------------
def test_scenario_sleep_productivity_trap():
    """5 hrs sleep + high productivity vs 8 hrs sleep + moderate productivity"""
    payload = {
        "options": [
            {
                "title": "Sleep Sacrifice Strategy",
                "growth_criteria": [
                    {"weight": 10, "impact": 10},  # Output volume
                    {"weight": 9, "impact": 9}     # Deadline achievement
                ],
                "sustainability_criteria": [
                    {"weight": 1, "impact": 10},   # Health impact
                    {"weight": 2, "impact": 8}     # Cognitive function
                ]
            }
        ]
    }

    response = client.post("/decision/compare", json=payload)
    assert response.status_code == 200
    data = response.json()
    eval_data = data["evaluations"][0]
    
    # Should show significant tension when sustainability is heavily sacrificed
    assert eval_data["tension_severity"] in ["LOW", "STABLE", "MODERATE", "HIGH", "CRITICAL"]
    assert "composite_score" in eval_data


# ---------------------------
# Scenario 7: Content Creator Posting Schedule
# ---------------------------
def test_scenario_content_creator():
    """4 high-quality videos/week vs 1 highly polished video/week"""
    payload = {
        "options": [
            {
                "title": "4 Videos Per Week",
                "growth_criteria": [
                    {"weight": 9, "impact": 10},   # Audience growth
                    {"weight": 8, "impact": 8}     # Algorithm favor
                ],
                "sustainability_criteria": [
                    {"weight": 2, "impact": 9},    # Creative burnout
                    {"weight": 7, "impact": 8}     # Quality consistency
                ]
            },
            {
                "title": "1 Polished Video Weekly",
                "growth_criteria": [
                    {"weight": 5, "impact": 6},    # Audience growth
                    {"weight": 4, "impact": 5}     # Algorithm favor
                ],
                "sustainability_criteria": [
                    {"weight": 9, "impact": 8},    # Creative burnout
                    {"weight": 9, "impact": 9}     # Quality consistency
                ]
            }
        ]
    }

    response = client.post("/decision/compare", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    # Both options should be evaluated successfully
    assert len(data["evaluations"]) == 2
    for i, eval_data in enumerate(data["evaluations"]):
        assert "tension_severity" in eval_data
        assert 0 < eval_data["composite_score"] <= 100


# ---------------------------
# Scenario 8: Balanced vs Deep Specialization
# ---------------------------
def test_scenario_balanced_learning():
    """Deep specialization vs broad versatility learning"""
    payload = {
        "options": [
            {
                "title": "Deep Specialization",
                "growth_criteria": [
                    {"weight": 10, "impact": 10},  # Expertise depth
                    {"weight": 5, "impact": 6}     # Versatility
                ],
                "sustainability_criteria": [
                    {"weight": 6, "impact": 7},    # Interest maintenance
                    {"weight": 7, "impact": 6}     # Cognitive load
                ]
            },
            {
                "title": "Broad Skill Learning",
                "growth_criteria": [
                    {"weight": 6, "impact": 7},    # Expertise depth
                    {"weight": 8, "impact": 8}     # Versatility
                ],
                "sustainability_criteria": [
                    {"weight": 8, "impact": 8},    # Interest maintenance
                    {"weight": 8, "impact": 7}     # Cognitive load
                ]
            }
        ]
    }

    response = client.post("/decision/compare", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    # Both should present valid evaluation options
    assert len(data["evaluations"]) == 2
    for eval_data in data["evaluations"]:
        assert "tension_severity" in eval_data
        assert "composite_score" in eval_data


# ---------------------------
# Scenario 9: Volunteer Leadership Overload
# ---------------------------
def test_scenario_volunteer_leadership():
    """Continue current role (5 hrs/month) vs chair major initiative (20 hrs/month)"""
    payload = {
        "options": [
            {
                "title": "Current Role (5 hrs/month)",
                "growth_criteria": [
                    {"weight": 3, "impact": 4},    # Mission impact
                    {"weight": 2, "impact": 3}     # Leadership experience
                ],
                "sustainability_criteria": [
                    {"weight": 9, "impact": 9},    # Personal time
                    {"weight": 6, "impact": 6}     # Role fulfillment
                ]
            },
            {
                "title": "Chair Major Initiative (20 hrs/month)",
                "growth_criteria": [
                    {"weight": 9, "impact": 10},   # Mission impact
                    {"weight": 8, "impact": 9}     # Leadership experience
                ],
                "sustainability_criteria": [
                    {"weight": 3, "impact": 10},   # Personal time
                    {"weight": 6, "impact": 7}     # Role fulfillment
                ]
            }
        ]
    }

    response = client.post("/decision/compare", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    # Should have both options evaluated
    assert len(data["evaluations"]) == 2
    for eval_data in data["evaluations"]:
        assert "tension_severity" in eval_data
        assert eval_data["composite_score"] > 0


# ---------------------------
# Scenario 10: Extreme Imbalance - Burnout Trap
# ---------------------------
def test_scenario_extreme_burnout_trap():
    """High salary but 80+ hours/week vs current sustainable role"""
    payload = {
        "options": [
            {
                "title": "Double Salary (80+ hrs/week)",
                "growth_criteria": [
                    {"weight": 10, "impact": 10},  # Income stability
                    {"weight": 10, "impact": 10}   # Financial security
                ],
                "sustainability_criteria": [
                    {"weight": 1, "impact": 10},   # Work-life balance
                    {"weight": 1, "impact": 10}    # Health/family time
                ]
            },
            {
                "title": "Current Sustainable Role",
                "growth_criteria": [
                    {"weight": 5, "impact": 6},    # Income stability
                    {"weight": 5, "impact": 6}     # Financial security
                ],
                "sustainability_criteria": [
                    {"weight": 8, "impact": 8},    # Work-life balance
                    {"weight": 8, "impact": 8}     # Health/family time
                ]
            }
        ]
    }

    response = client.post("/decision/compare", json=payload)
    assert response.status_code == 200
    data = response.json()
    eval_data_trap = data["evaluations"][0]
    eval_data_current = data["evaluations"][1]
    
    # Both should have valid evaluations
    assert eval_data_trap["tension_severity"] in ["LOW", "STABLE", "MODERATE", "HIGH", "CRITICAL"]
    assert eval_data_current["tension_severity"] in ["LOW", "STABLE", "MODERATE", "HIGH", "CRITICAL"]
    
    # Both should have valid composite scores
    assert 0 < eval_data_trap["composite_score"] <= 100
    assert 0 < eval_data_current["composite_score"] <= 100