# API Documentation: Burnout-Proof Decision System

## Overview
The Burnout-Proof Decision System is a FastAPI-based service that evaluates decisions across growth and sustainability dimensions, identifying burnout risks and recommending structured decision strategies.

**Base URL**: `http://localhost:8000`

---

## Endpoints

### POST `/decision/compare`

Evaluates one or more decision options against growth and sustainability criteria.

#### Request Schema

```json
{
  "options": [
    {
      "title": "string (required)",
      "growth_criteria": [
        {
          "weight": float (0-10, required),
          "impact": float (0-10, required)
        }
      ],
      "sustainability_criteria": [
        {
          "weight": float (0-10, required),
          "impact": float (0-10, required)
        }
      ]
    }
  ]
}
```

#### Field Descriptions

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| `title` | string | — | Name/description of the option |
| `weight` | float | 0-10 | Importance level (0=not important, 10=critical) |
| `impact` | float | 0-10 | Expected outcome level (0=minimal, 10=maximum) |

#### Validation Rules

- Minimum 1 option required
- Maximum 10 options recommended
- At least 1 growth criterion required per option
- At least 1 sustainability criterion required per option
- Weight and impact must be between 0 and 10 (inclusive)
- Fractional values allowed (e.g., 7.5, 3.2)

---

## Response Schema

### Single Option Response
```json
{
  "decision_status": "SINGLE_OPTION_CLASSIFIED",
  "evaluations": [
    {
      "title": "string",
      "growth_score": 75.38,
      "sustainability_score": 75.38,
      "tension_index": 0.0,
      "tension_severity": "LOW",
      "composite_score": 75.38,
      "zone": "EXECUTE_FULLY",
      "zone_reason": "High growth and sustainable",
      "risk_level": "STRUCTURALLY_STABLE",
      "stability_level": "STABLE",
      "triggered_messages": []
    }
  ]
}
```

### Multiple Options Response
```json
{
  "decision_status": "CLEAR_WINNER",
  "decision_winner": "Option Title",
  "winner_idx": 0,
  "winner_explanation": "Explanation of why this option won",
  "evaluations": [
    {
      "title": "string",
      "growth_score": 75.38,
      "sustainability_score": 75.38,
      "tension_index": 0.0,
      "tension_severity": "LOW",
      "composite_score": 75.38,
      "zone": "EXECUTE_FULLY",
      "zone_reason": "High growth and sustainable",
      "risk_level": "STRUCTURALLY_STABLE",
      "stability_level": "STABLE",
      "sensitivity_range": 2.45,
      "triggered_messages": [
        "Optional warning or insight message"
      ]
    }
  ],
  "all_options_poor_fit": false,
  "poor_fit_reason": "Reason if applicable"
}
```

---

## Response Field Reference

### Numeric Scores

| Field | Range | Meaning |
|-------|-------|---------|
| `growth_score` | 0-100 | How much the option drives forward progress |
| `sustainability_score` | 0-100 | How well it maintains stability long-term |
| `composite_score` | 0-100 | Final viability score (accounts for imbalance) |
| `tension_index` | 0-100 | Absolute difference between growth and sustainability |
| `sensitivity_range` | 0-100 | Variance when varying weights by ±20% |

### Categorical Classifications

#### Tension Severity
- **LOW**: Tension index 0-15 (well-balanced)
- **MODERATE**: Tension index 15-30 (some imbalance)
- **HIGH**: Tension index 30-60 (significant imbalance)
- **CRITICAL**: Tension index 60-100 (severe imbalance, burnout risk)

#### Structural Zones
- **EXECUTE_FULLY**: High growth (≥70) + high sustainability (≥70) → Go ahead
- **TIME_BOX**: High growth (≥70) + low sustainability (<50) → Limited duration
- **LIGHT_RECOVERY**: Low growth (<50) + high sustainability (≥70) → Recovery phase
- **STEADY_EXECUTION**: Moderate balance → Proceed cautiously
- **AVOID**: Low growth (<40) + low sustainability (<40) → Reject/redesign

#### Risk Levels
- **STRUCTURALLY_STABLE**: Balanced, low burnout risk
- **SEVERE_BURNOUT_RISK**: High growth, low sustainability (asymmetric penalty applied)
- **SUSTAINABILITY_DEFICIT**: Sustainability score too low
- **GROWTH_STAGNATION_RISK**: Growth score too low
- **SEVERE_IMBALANCE**: Both growth and sustainability are low
- **LOW_STRUCTURAL_VALUE**: Insufficient viability in both dimensions

#### Stability Levels
- **STABLE**: Low sensitivity variance (<8) — decisions are robust
- **MODERATELY_STABLE**: Medium sensitivity variance (8-20) — moderately robust
- **FRAGILE**: High sensitivity variance (>20) — vulnerable to criteria changes

### Decision Status

| Status | Meaning | Context |
|--------|---------|---------|
| `SINGLE_OPTION_CLASSIFIED` | One option submitted | Structural viability assessment only |
| `CLEAR_WINNER` | Multi-option, one option clearly better | Composite scores significantly different |
| `CLOSE_COMPETITION` | Multi-option, scores similar | Difficult choice, weigh strategic factors |
| `ALL_OPTIONS_POOR_FIT` | Multi-option, all options weak | Redesign needed; none advisable as-is |

---

## Example Requests

### Example 1: Single Balanced Option
```bash
curl -X POST "http://localhost:8000/decision/compare" \
  -H "Content-Type: application/json" \
  -d '{
    "options": [
      {
        "title": "Launch New Product Line",
        "growth_criteria": [
          {"weight": 7, "impact": 8},
          {"weight": 6, "impact": 7}
        ],
        "sustainability_criteria": [
          {"weight": 7, "impact": 8},
          {"weight": 6, "impact": 7}
        ]
      }
    ]
  }'
```

**Expected Output**: EXECUTE_FULLY zone, STRUCTURALLY_STABLE risk

---

### Example 2: Burnout-Trap Option
```bash
curl -X POST "http://localhost:8000/decision/compare" \
  -H "Content-Type: application/json" \
  -d '{
    "options": [
      {
        "title": "Aggressive Market Expansion",
        "growth_criteria": [
          {"weight": 9, "impact": 10},
          {"weight": 10, "impact": 9}
        ],
        "sustainability_criteria": [
          {"weight": 2, "impact": 3},
          {"weight": 1, "impact": 4}
        ]
      }
    ]
  }'
```

**Expected Output**: TIME_BOX zone, SEVERE_BURNOUT_RISK, triggered warning messages

---

### Example 3: Multiple Options (Comparison)
```bash
curl -X POST "http://localhost:8000/decision/compare" \
  -H "Content-Type: application/json" \
  -d '{
    "options": [
      {
        "title": "Conservative Growth",
        "growth_criteria": [
          {"weight": 5, "impact": 6}
        ],
        "sustainability_criteria": [
          {"weight": 8, "impact": 9}
        ]
      },
      {
        "title": "Balanced Approach",
        "growth_criteria": [
          {"weight": 7, "impact": 8}
        ],
        "sustainability_criteria": [
          {"weight": 7, "impact": 8}
        ]
      },
      {
        "title": "Aggressive Push",
        "growth_criteria": [
          {"weight": 9, "impact": 10}
        ],
        "sustainability_criteria": [
          {"weight": 3, "impact": 4}
        ]
      }
    ]
  }'
```

**Expected Output**: CLEAR_WINNER (Balanced Approach), with rationale

---

## Error Responses

### 422 Validation Error
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "options", 0, "growth_criteria", 0, "weight"],
      "msg": "Input should be a valid number, unable to parse string as a number",
      "input": "invalid"
    }
  ]
}
```

**Common Causes**:
- Weight/impact outside 0-10 range
- Missing required fields
- Wrong data types (string instead of number)
- No options provided

### 400 Bad Request
```json
{
  "detail": "At least one growth_criteria is required"
}
```

---

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 422 | Validation error (invalid input) |
| 400 | Bad request (missing criteria) |
| 500 | Server error |

---

## Usage Guidelines

### When to Use Single Option
- Pre-decision evaluation: "Should we proceed with this plan?"
- Risk assessment: "Is this structurally viable?"
- Viability checking: "Does this make sense?"

### When to Use Multiple Options
- Decision framework: "Which option should we choose?"
- Trade-off analysis: "Growth vs. sustainability"
- Strategic planning: "Multiple paths forward"

### Interpreting Results

**High Composite Score (>60)** + **STABLE**: ✅ Confidence in decision
**Medium Composite Score (40-60)** + **MODERATELY_STABLE**: ⚠️ Proceed with caution
**Low Composite Score (<40)** + **FRAGILE**: ❌ High risk, recommend redesign

---

## Rate Limiting & Best Practices

- No rate limiting currently implemented
- Recommended: Maximum 10 options per request
- Use realistic weights (1-9 range most common)
- Provide descriptive titles for better analysis

---

## Changelog

### Version 1.0 (Current)
- Initial release with asymmetric burnout penalties
- ±20% sensitivity analysis
- 5-zone classification system
- 6 risk level categories
- Enhanced burnout trap detection

