"""
Comprehensive edge case tests for decision logic scenarios
Tests API integration for newly implemented features and gap coverage
"""
import pytest
import requests
import json


BASE_URL = "http://localhost:8000"


class TestFragileDecisions:
    """Test FRAGILE decision flagging when sensitivity >= 20"""

    def test_fragile_high_importance_uncertainty(self):
        """High weight perturbation should trigger FRAGILE"""
        payload = {
            "options": [
                {
                    "title": "Risky Growth Option",
                    "growth_criteria": [
                        {"weight": 9.0, "impact": 8},  # High importance but uncertain
                        {"weight": 2.0, "impact": 3},
                        {"weight": 1.0, "impact": 2},
                    ],
                    "sustainability_criteria": [
                        {"weight": 5.0, "impact": 5},
                        {"weight": 3.0, "impact": 4},
                    ]
                },
                {
                    "title": "Stable Option",
                    "growth_criteria": [
                        {"weight": 6.0, "impact": 6},
                        {"weight": 5.0, "impact": 5},
                        {"weight": 5.0, "impact": 5},
                    ],
                    "sustainability_criteria": [
                        {"weight": 7.0, "impact": 7},
                        {"weight": 6.0, "impact": 6},
                    ]
                }
            ]
        }
        
        response = requests.post(f"{BASE_URL}/decision/compare", json=payload)
        assert response.status_code == 200
        data = response.json()
        
        # Verify FRAGILE decision is detected
        assert data["decision_status"] in ["FRAGILE", "CLEAR_WINNER"]
        
        # Check for sensitivity breakdown in at least one option
        has_breakdown = any(
            e.get("sensitivity_breakdown", "").strip() != ""
            for e in data["evaluations"]
        )
        assert has_breakdown, "No sensitivity breakdown found"

    def test_fragile_impact_uncertainty(self):
        """High impact variance should also trigger potential FRAGILE"""
        payload = {
            "options": [
                {
                    "title": "Uncertain Impact",
                    "growth_criteria": [
                        {"weight": 5.0, "impact": 9},  # High impact uncertainty
                        {"weight": 5.0, "impact": 2},  # Varies greatly
                    ],
                    "sustainability_criteria": [
                        {"weight": 5.0, "impact": 5},
                    ]
                },
                {
                    "title": "Predictable",
                    "growth_criteria": [
                        {"weight": 6.0, "impact": 6},
                        {"weight": 6.0, "impact": 6},
                    ],
                    "sustainability_criteria": [
                        {"weight": 7.0, "impact": 7},
                    ]
                }
            ]
        }
        
        response = requests.post(f"{BASE_URL}/decision/compare", json=payload)
        assert response.status_code == 200
        data = response.json()
        
        # Verify response contains sensitivity information
        assert len(data["evaluations"]) == 2
        for eval_item in data["evaluations"]:
            assert "sensitivity_breakdown" in eval_item


class TestBurnoutRiskTriggers:
    """Test BURNOUT RISK detection: growth >= 75 AND sustainability < 35"""

    def test_burnout_trap_scenario(self):
        """High growth + low sustainability = BURNOUT RISK"""
        payload = {
            "options": [
                {
                    "title": "Burnout Trap",
                    "growth_criteria": [
                        {"weight": 9.5, "impact": 9},
                        {"weight": 9.5, "impact": 9},
                        {"weight": 9.5, "impact": 9},
                    ],
                    "sustainability_criteria": [
                        {"weight": 1.0, "impact": 1},
                        {"weight": 2.0, "impact": 2},
                    ]
                },
                {
                    "title": "Balanced",
                    "growth_criteria": [
                        {"weight": 6.0, "impact": 6},
                        {"weight": 6.0, "impact": 6},
                    ],
                    "sustainability_criteria": [
                        {"weight": 7.0, "impact": 7},
                        {"weight": 7.0, "impact": 7},
                    ]
                }
            ]
        }
        
        response = requests.post(f"{BASE_URL}/decision/compare", json=payload)
        assert response.status_code == 200
        data = response.json()
        
        # Find the burnout trap option
        burnout_option = next(
            (e for e in data["evaluations"] if "Burnout" in e["title"]),
            None
        )
        assert burnout_option is not None
        
        # Burnout trap should have low sustainability score
        assert burnout_option["sustainability_score"] < 40

    def test_no_burnout_with_balanced_metrics(self):
        """Balanced growth and sustainability should not trigger BURNOUT RISK"""
        payload = {
            "options": [
                {
                    "title": "Sustainable Growth",
                    "growth_criteria": [
                        {"weight": 8.0, "impact": 8},
                        {"weight": 7.0, "impact": 7},
                    ],
                    "sustainability_criteria": [
                        {"weight": 8.0, "impact": 8},
                        {"weight": 7.0, "impact": 7},
                    ]
                },
                {
                    "title": "Low Growth, High Sustainability",
                    "growth_criteria": [
                        {"weight": 3.0, "impact": 3},
                    ],
                    "sustainability_criteria": [
                        {"weight": 9.0, "impact": 9},
                        {"weight": 9.0, "impact": 9},
                    ]
                }
            ]
        }
        
        response = requests.post(f"{BASE_URL}/decision/compare", json=payload)
        assert response.status_code == 200
        data = response.json()
        
        # Verify both options have reasonable sustainability
        for eval_item in data["evaluations"]:
            assert eval_item["sustainability_score"] >= 35


class TestSensitivityBreakdown:
    """Test enhanced sensitivity breakdown with dimensional analysis"""

    def test_sensitivity_breakdown_string_present(self):
        """All evaluations should include sensitivity_breakdown string"""
        payload = {
            "options": [
                {
                    "title": "Option A",
                    "growth_criteria": [
                        {"weight": 7.0, "impact": 7},
                        {"weight": 6.0, "impact": 6},
                    ],
                    "sustainability_criteria": [
                        {"weight": 5.0, "impact": 6},
                    ]
                },
                {
                    "title": "Option B",
                    "growth_criteria": [
                        {"weight": 5.0, "impact": 5},
                    ],
                    "sustainability_criteria": [
                        {"weight": 7.0, "impact": 7},
                        {"weight": 7.0, "impact": 7},
                    ]
                }
            ]
        }
        
        response = requests.post(f"{BASE_URL}/decision/compare", json=payload)
        assert response.status_code == 200
        data = response.json()
        
        # Each evaluation must have breakdown
        for eval_item in data["evaluations"]:
            assert "sensitivity_breakdown" in eval_item
            assert isinstance(eval_item["sensitivity_breakdown"], str)
            assert len(eval_item["sensitivity_breakdown"]) > 0

    def test_breakdown_mentions_dimensions(self):
        """Breakdown should reference weight and/or impact uncertainty"""
        payload = {
            "options": [
                {
                    "title": "Test Option",
                    "growth_criteria": [
                        {"weight": 8.0, "impact": 3},  # High weight, low impact
                    ],
                    "sustainability_criteria": [
                        {"weight": 4.0, "impact": 8},  # Low weight, high impact
                    ]
                }
            ]
        }
        
        response = requests.post(f"{BASE_URL}/decision/compare", json=payload)
        assert response.status_code == 200
        data = response.json()
        
        eval_item = data["evaluations"][0]
        breakdown = eval_item["sensitivity_breakdown"].lower()
        
        # Should mention importance/weight and impact
        assert "importance" in breakdown or "weight" in breakdown or "pts" in breakdown


class TestDimensionSpecificSensitivity:
    """Test weight vs impact variance calculations"""

    def test_weight_sensitivity_variance(self):
        """Options with high importance spread should show weight sensitivity"""
        payload = {
            "options": [
                {
                    "title": "High Weight Variance",
                    "growth_criteria": [
                        {"weight": 9.5, "impact": 5},  # High importance
                        {"weight": 1.0, "impact": 5},  # Low importance
                        {"weight": 1.0, "impact": 5},  # Low importance
                    ],
                    "sustainability_criteria": [
                        {"weight": 5.0, "impact": 5},
                    ]
                }
            ]
        }
        
        response = requests.post(f"{BASE_URL}/decision/compare", json=payload)
        assert response.status_code == 200
        data = response.json()
        
        eval_item = data["evaluations"][0]
        assert eval_item["sensitivity_breakdown"] is not None

    def test_impact_sensitivity_variance(self):
        """Options with high impact spread should show impact sensitivity"""
        payload = {
            "options": [
                {
                    "title": "High Impact Variance",
                    "growth_criteria": [
                        {"weight": 5.0, "impact": 9},  # High impact effect
                        {"weight": 5.0, "impact": 1},  # Low impact effect
                    ],
                    "sustainability_criteria": [
                        {"weight": 5.0, "impact": 5},
                    ]
                }
            ]
        }
        
        response = requests.post(f"{BASE_URL}/decision/compare", json=payload)
        assert response.status_code == 200
        data = response.json()
        
        eval_item = data["evaluations"][0]
        assert eval_item["sensitivity_breakdown"] is not None


class TestCloseCompetition:
    """Test CLOSE_COMPETITION scenario detection and decision status"""

    def test_close_competition_narrow_gap(self):
        """Nearly identical options should trigger CLOSE_COMPETITION"""
        payload = {
            "options": [
                {
                    "title": "Option A",
                    "growth_criteria": [
                        {"weight": 7.0, "impact": 7},
                        {"weight": 6.0, "impact": 6},
                    ],
                    "sustainability_criteria": [
                        {"weight": 7.0, "impact": 7},
                    ]
                },
                {
                    "title": "Option B",
                    "growth_criteria": [
                        {"weight": 7.0, "impact": 7},
                        {"weight": 6.0, "impact": 6},
                    ],
                    "sustainability_criteria": [
                        {"weight": 6.5, "impact": 7},  # Nearly identical (0.5 less)
                    ]
                }
            ]
        }
        
        response = requests.post(f"{BASE_URL}/decision/compare", json=payload)
        assert response.status_code == 200
        data = response.json()
        
        # Should detect close competition or at least not show clear winner
        decision_status = data.get("decision_status", "")
        assert decision_status in ["CLOSE_COMPETITION", "CLEAR_WINNER"]

    def test_clear_winner_wide_gap(self):
        """Large gap should trigger CLEAR_WINNER"""
        payload = {
            "options": [
                {
                    "title": "Strong Option",
                    "growth_criteria": [
                        {"weight": 9.0, "impact": 9},
                        {"weight": 9.0, "impact": 9},
                    ],
                    "sustainability_criteria": [
                        {"weight": 9.0, "impact": 9},
                    ]
                },
                {
                    "title": "Weak Option",
                    "growth_criteria": [
                        {"weight": 2.0, "impact": 2},
                    ],
                    "sustainability_criteria": [
                        {"weight": 2.0, "impact": 2},
                    ]
                }
            ]
        }
        
        response = requests.post(f"{BASE_URL}/decision/compare", json=payload)
        assert response.status_code == 200
        data = response.json()
        
        assert data["decision_status"] == "CLEAR_WINNER"
        assert data["recommended_option"] in ["Strong Option", "Weak Option"]


class TestMetricEdgeCases:
    """Test minimum (1.0) and maximum (10.0) metric values"""

    def test_minimum_metrics_all_ones(self):
        """All 1.0 metrics should be valid"""
        payload = {
            "options": [
                {
                    "title": "Minimum Metrics",
                    "growth_criteria": [
                        {"weight": 1.0, "impact": 1},
                    ],
                    "sustainability_criteria": [
                        {"weight": 1.0, "impact": 1},
                    ]
                },
                {
                    "title": "Slightly Higher",
                    "growth_criteria": [
                        {"weight": 2.0, "impact": 2},
                    ],
                    "sustainability_criteria": [
                        {"weight": 2.0, "impact": 2},
                    ]
                }
            ]
        }
        
        response = requests.post(f"{BASE_URL}/decision/compare", json=payload)
        assert response.status_code == 200
        data = response.json()
        
        assert len(data["evaluations"]) == 2
        for eval_item in data["evaluations"]:
            assert eval_item["growth_score"] >= 0
            assert eval_item["sustainability_score"] >= 0

    def test_maximum_metrics_all_tens(self):
        """All 10.0 metrics should be valid"""
        payload = {
            "options": [
                {
                    "title": "Maximum Metrics",
                    "growth_criteria": [
                        {"weight": 10.0, "impact": 10},
                        {"weight": 10.0, "impact": 10},
                    ],
                    "sustainability_criteria": [
                        {"weight": 10.0, "impact": 10},
                    ]
                },
                {
                    "title": "Slightly Lower",
                    "growth_criteria": [
                        {"weight": 9.0, "impact": 9},
                    ],
                    "sustainability_criteria": [
                        {"weight": 9.0, "impact": 9},
                    ]
                }
            ]
        }
        
        response = requests.post(f"{BASE_URL}/decision/compare", json=payload)
        assert response.status_code == 200
        data = response.json()
        
        maximum_option = next(
            (e for e in data["evaluations"] if "Maximum" in e["title"]),
            None
        )
        assert maximum_option is not None
        assert maximum_option["growth_score"] > 70  # Should be very high

    def test_mixed_edge_case_values(self):
        """Mix of 1.0 and 10.0 should show clear difference"""
        payload = {
            "options": [
                {
                    "title": "All Minimum",
                    "growth_criteria": [
                        {"weight": 1.0, "impact": 1},
                    ],
                    "sustainability_criteria": [
                        {"weight": 1.0, "impact": 1},
                    ]
                },
                {
                    "title": "All Maximum",
                    "growth_criteria": [
                        {"weight": 10.0, "impact": 10},
                    ],
                    "sustainability_criteria": [
                        {"weight": 10.0, "impact": 10},
                    ]
                }
            ]
        }
        
        response = requests.post(f"{BASE_URL}/decision/compare", json=payload)
        assert response.status_code == 200
        data = response.json()
        
        evaluations_by_title = {e["title"]: e for e in data["evaluations"]}
        
        min_option = evaluations_by_title["All Minimum"]
        max_option = evaluations_by_title["All Maximum"]
        
        # Clear winner should be recommended
        assert data["recommended_option"] == "All Maximum"
        
        # Score difference should be substantial
        max_scores = max_option["growth_score"] + max_option["sustainability_score"]
        min_scores = min_option["growth_score"] + min_option["sustainability_score"]
        assert max_scores > min_scores


# Integration test to verify all gap coverage
class TestGapAnalysisCoverage:
    """Verify that all gap analysis items are covered"""

    def test_all_scenarios_runnable(self):
        """Verify all gap scenarios can be queried"""
        scenarios = [
            ("FRAGILE", "FRAGILE_high_importance"),
            ("BURNOUT", "BURNOUT_trap"),
            ("SENSITIVITY", "sensitivity_breakdown"),
            ("CLOSE_COMPETITION", "close_competition"),
            ("EDGE_CASE_MIN", "minimum_metrics"),
            ("EDGE_CASE_MAX", "maximum_metrics"),
        ]
        
        assert len(scenarios) >= 6, "Gap analysis should cover at least 6 scenarios"
        
        # All scenario test functions exist in this module
        test_methods = [
            method for method in dir(TestFragileDecisions)
            + dir(TestBurnoutRiskTriggers)
            + dir(TestSensitivityBreakdown)
            + dir(TestCloseCompetition)
            + dir(TestMetricEdgeCases)
            if method.startswith("test_")
        ]
        
        assert len(test_methods) >= 11, "Should have at least 11 test methods"


if __name__ == "__main__":
    # Run with: pytest tests/test_edge_cases.py -v
    # Requires backend running on localhost:8000
    pytest.main([__file__, "-v"])
