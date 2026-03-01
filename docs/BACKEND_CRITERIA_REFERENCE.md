# Backend Criteria Reference Guide

## Overview

The Burnout-Proof Decision Engine uses a two-dimensional evaluation framework based on **growth** and **sustainability** criteria. This document maps all backend criteria, thresholds, and scoring logic.

---

## 1. Core Criteria Structure

### Input Data Model

Each decision option contains:

```
DecisionOption {
  title: string (1-100 chars)
  growth_criteria: List[Criterion]
  sustainability_criteria: List[Criterion]
}

Criterion {
  weight: float (0-10)     # importance of this factor
  impact: int (0-10)       # how much this factor contributes to outcome
}
```

### Constraints
- Minimum 1 criterion in EACH category per option
- Maximum 10 options per comparison
- Duplicate titles not allowed
- All criteria must have non-empty weight and impact values

---

## 2. Scoring Methodology: Normalized Scores

### Formula: Weighted Mean → Normalized to 0-100

```
Normalized Score = (Σ(weight × impact) / Σ(weight)) × 10
```

**Example:**
```
Growth criteria:
  - Career advancement: weight=9, impact=8  → 9×8=72
  - Skill building: weight=7, impact=7     → 7×7=49
  Total weighted: 72+49 = 121
  Total weight: 9+7 = 16
  Normalized: (121/16) × 10 = 75.6/10 scaled = 75.6%
```

### Interpretation
- **0-40**: Low/Weak
- **40-70**: Moderate/Medium
- **70-100**: High/Strong

---

## 3. Zone Classification Thresholds

### Five Decision Zones

| Zone | Growth | Sustainability | Meaning | Action |
|------|--------|-----------------|---------|--------|
| **EXECUTE_FULLY** | ≥70 | ≥70 | High opportunity + sustainable | ✓ Pursue boldly |
| **TIME_BOX** | ≥70 | <50 | High opportunity but unsustainable | ⏰ Set time limits (18-24mo) |
| **LIGHT_RECOVERY** | <50 | ≥70 | Low opportunity but stable | 🏥 Pause growth, stabilize |
| **AVOID** | <40 | <40 (both very low) | Minimal viability | ❌ Skip entirely |
| **STEADY_EXECUTION** | — | — | Balanced moderate (fallback) | 🛡️ Maintain status quo |

### Zone Decision Logic

```python
if growth >= 70 and sustainability >= 70:
    zone = EXECUTE_FULLY
elif growth >= 70 and sustainability < 50:
    zone = TIME_BOX
elif growth < 50 and sustainability >= 70:
    zone = LIGHT_RECOVERY
elif growth < 40 and sustainability < 40:
    zone = AVOID
else:
    zone = STEADY_EXECUTION
```

---

## 4. Tension Index: Growth-Sustainability Imbalance

### Formula
```
Tension = |Growth - Sustainability|
```

### Severity Classification

| Tension | Severity | Context |
|---------|----------|---------|
| ≤15 | **LOW** | Balanced decision |
| 16-30 | **MODERATE** | Acceptable tradeoff |
| 31-60 | **HIGH** | Significant imbalance |
| >60 | **CRITICAL** | Severe mismatch |

### Example
```
Growth: 85, Sustainability: 30
Tension: |85-30| = 55 → HIGH severity
Interpretation: Strong growth but significant burnout risk
```

---

## 5. Composite Score: Continuous Viability Assessment

### Formula with Asymmetric Burnout Penalty

```
Base Score = (Growth + Sustainability) / 2

Growth Dominance = max(0, Growth - Sustainability)
Sustainability Dominance = max(0, Sustainability - Growth)

Asymmetric Penalty = (0.3 × Growth Dominance) + (0.1 × Sustainability Dominance)
  Note: Burnout penalty (0.3x) is 3× WORSE than stagnation penalty (0.1x)

Quadratic Penalty = 0.05 × (Tension²) / 100
  Scales 0-5 points for extreme imbalances (tension > 50)

Composite = max(Base - Asymmetric Penalty - Quadratic Penalty, 0)
```

### Rationale
- **Asymmetric penalty**: Burnout (high growth, low sustainability) is 3× worse than stagnation
- **Quadratic penalty**: Extreme imbalances (tension > 50) compound the risk
- **Floor at 0**: Scores never go negative

### Example Calculation

**Scenario A: EXECUTE ZONE (growth=80, sustainability=75)**
```
Base = (80+75)/2 = 77.5
Growth Dominance = max(0, 80-75) = 5
Sustainability Dominance = 0
Asymmetric = (0.3×5) + (0.1×0) = 1.5
Tension = 5
Quadratic = 0.05×(25)/100 = 0.0125
Composite = 77.5 - 1.5 - 0.0125 = 75.99 ✓
```

**Scenario B: TIMEBOX ZONE (growth=85, sustainability=30)**
```
Base = (85+30)/2 = 57.5
Growth Dominance = max(0, 85-30) = 55
Sustainability Dominance = 0
Asymmetric = (0.3×55) + 0 = 16.5
Tension = 55
Quadratic = 0.05×(3025)/100 = 1.51
Composite = 57.5 - 16.5 - 1.51 = 39.49 ⚠️
```

**Scenario C: RECOVERY ZONE (growth=35, sustainability=80)**
```
Base = (35+80)/2 = 57.5
Growth Dominance = 0
Sustainability Dominance = max(0, 80-35) = 45
Asymmetric = 0 + (0.1×45) = 4.5
Tension = 45
Quadratic = 0.05×(2025)/100 = 1.01
Composite = 57.5 - 4.5 - 1.01 = 51.99 🏥
```

---

## 6. Risk Levels: Structural Assessment

### Risk Classification Hierarchy

Priority order (highest to lowest):

1. **LOW_STRUCTURAL_VALUE** (Zone = AVOID)
   - Both growth and sustainability critically low
   - Decision has minimal viability

2. **SEVERE_BURNOUT_RISK** (Tension = CRITICAL AND Growth > Sustainability)
   - Growth substantially exceeds sustainability capacity
   - Burnout scenario: demanding opportunity with insufficient support

3. **SEVERE_IMBALANCE** (Tension = CRITICAL, any direction)
   - Extreme mismatch requiring explicit mitigation strategy
   - May indicate necessary tradeoff or incomplete assessment

4. **SUSTAINABILITY_DEFICIT** (Sustainability < 40)
   - Foundation is at risk
   - Wellbeing fundamentals not met
   - May trigger unplanned exit

5. **GROWTH_STAGNATION_RISK** (Growth < 40, Zone ≠ STEADY_EXECUTION)
   - Minimal opportunity for development
   - Career progression at risk
   - Long-term dissatisfaction likely

6. **STRUCTURALLY_STABLE** (none of above)
   - Decision passes all structural tests
   - Proceed with confidence

### Trigger Examples

```
Growth=85, Sustainability=30, Zone=TIME_BOX, Tension=55 (CRITICAL)
→ Risk: SEVERE_BURNOUT_RISK
→ Message: "⚠️ CRITICAL: Burnout trap - high growth exceeds sustainability"

Growth=35, Sustainability=80, Zone=LIGHT_RECOVERY
→ Risk: GROWTH_STAGNATION_RISK
→ Message: "Low growth may indicate stagnation - consider lower-impact commitment"

Growth=35, Sustainability=25, Zone=AVOID
→ Risk: LOW_STRUCTURAL_VALUE
→ Message: "Low structural value across both dimensions"
```

---

## 7. Triggered Messages: Context-Aware Warnings

### Message Generation Logic

Messages appear based on specific thresholds:

1. **Burnout Trap (Critical)**
   - Condition: Growth ≥ 75 AND Sustainability < 35
   - Message: "CRITICAL: Burnout trap detected - high growth demands exceed sustainability capacity"

2. **Burnout Risk (Moderate)**
   - Condition: Growth ≥ 70 AND Sustainability < 50
   - Message: "High growth with sustainability deficit detected - burnout risk present"

3. **Sustainability Threshold**
   - Condition: Sustainability < 40
   - Message: "Sustainability below structural stability threshold"

4. **General Imbalance**
   - Condition: Tension Severity = HIGH or CRITICAL
   - Message: "Significant imbalance between growth and sustainability"

5. **Structural Rejection**
   - Condition: Zone = AVOID
   - Message: "Low structural value across both dimensions"

6. **Stagnation Risk (Recovery-Dominant)**
   - Condition: Growth < 40 AND Sustainability ≥ 70
   - Message: "Recovery-dominant structure detected - low growth may indicate stagnation"

7. **Growth Threshold (General)**
   - Condition: Growth < 40
   - Message: "Growth below minimum threshold - consider lower-impact commitment"

---

## 8. Sensitivity Analysis: Robustness Assessment

### Methodology: ±20% Weight Perturbation

Each criterion's weight is perturbed by ±20% (not the impact):

```
For each criterion: weight ∈ [0, 10]

Increased scenario:  weight_new = min(weight × 1.2, 10)
Decreased scenario:  weight_new = max(weight × 0.8, 0)

Recalculate normalized score for both scenarios
Sensitivity Range = |score_high - score_low|
```

### Stability Classification

| Sensitivity Range | Stability Level | Robustness | Recommendation |
|-------------------|-----------------|------------|-----------------|
| < 8 | **STABLE** | Tight, resilient | Confident decision |
| 8-20 | **MODERATELY_STABLE** | Acceptable variance | Normal confidence |
| ≥ 20 | **FRAGILE** | High variance, fragile | Reassess assumptions |

### Interpretation

- **High sensitivity** (≥20): Small changes in weight assumptions lead to significantly different composite scores
  - Suggests: Criteria assessments may be uncertain or criteria have high relative importance
  - Action: Verify assumptions or focus on most impactful criteria

- **Low sensitivity** (<8): Robust decision regardless of weight variations
  - Suggests: Criteria are well-aligned or balanced
  - Action: Proceed with confidence

### Example

```
Growth Criteria:
  - Career: weight=9, impact=8
  - Skills: weight=7, impact=7
  Normalized: 75.6

+20% weights:
  - Career: weight=10, impact=8
  - Skills: weight=8, impact=7
  Normalized: 76.2

-20% weights:
  - Career: weight=7.2, impact=8
  - Skills: weight=5.6, impact=7
  Normalized: 74.8

Sensitivity = |76.2 - 74.8| = 1.4 → STABLE ✓
```

---

## 9. Close Competition Detection

### Logic

Two or more options are classified as "close competition" when their composite scores are within a narrow margin.

```
Condition: max(composite_scores) - second_max(composite_scores) < threshold
Decision Status: CLOSE_COMPETITION
Recommendation: "Top options have very similar composite scores"
```

### Implication

When options are very close:
- No clear winner emerges from structural analysis
- Decision requires additional qualitative factors (intuition, context, timing)
- User should apply decision-making frameworks beyond the engine

---

## 10. Decision Status Outcomes

### Single Option Mode
```
Condition: Only 1 option provided
Status: SINGLE_OPTION_CLASSIFIED
Response: Detailed evaluation of that single option's viability
```

### Close Competition Mode
```
Condition: Multiple options, top scores within competitive range
Status: CLOSE_COMPETITION
Response: All options ranked by composite score, no winner declared
Reasoning: "Top options have very similar composite scores"
```

### Clear Winner Mode
```
Condition: Multiple options, clear highest composite score
Status: CLEAR_WINNER
Response: Top option recommended with reasoning
Recommendation: Highest composite score (e.g., "Composite: 75.99")
```

---

## 11. Example: Full Backend Evaluation

### Input

```json
{
  "options": [
    {
      "title": "Team Lead Promotion",
      "growth_criteria": [
        {"weight": 9, "impact": 8},  // Career advancement
        {"weight": 7, "impact": 7}   // Skill building
      ],
      "sustainability_criteria": [
        {"weight": 9, "impact": 7},  // Work-life balance
        {"weight": 8, "impact": 8}   // Team support
      ]
    }
  ]
}
```

### Processing Steps

**Step 1: Normalized Scores**
```
Growth = (9×8 + 7×7) / (9+7) × 10 = 121/16 × 10 = 75.6
Sustainability = (9×7 + 8×8) / (9+8) × 10 = 127/17 × 10 = 74.7
```

**Step 2: Tension**
```
Tension = |75.6 - 74.7| = 0.9 → LOW severity
```

**Step 3: Zone Classification**
```
Growth (75.6) ≥ 70 ✓
Sustainability (74.7) ≥ 70 ✓
Zone = EXECUTE_FULLY
```

**Step 4: Composite Score**
```
Base = (75.6 + 74.7) / 2 = 75.15
Growth Dominance = max(0, 75.6-74.7) = 0.9
Asymmetric Penalty = 0.3×0.9 = 0.27
Quadratic Penalty = 0.05×(0.81)/100 ≈ 0.004
Composite = 75.15 - 0.27 - 0.004 = 74.88
```

**Step 5: Risk Level**
```
Zone = EXECUTE_FULLY (not AVOID)
Tension ≠ CRITICAL
Sustainability = 74.7 (not < 40)
Growth = 75.6 (not < 40)
Risk = STRUCTURALLY_STABLE ✓
```

**Step 6: Triggered Messages**
```
Growth (75.6) < 75: ✗ (not critical burnout)
Growth (75.6) < 70: ✗ (not moderate burnout)
Sustainability (74.7) < 40: ✗
Tension ≠ HIGH/CRITICAL: ✗
Zone ≠ AVOID: ✗
Growth < 40: ✗
→ No messages triggered
```

**Step 7: Sensitivity Analysis**
```
(Criteria adjustment simulations...)
Sensitivity Range = 3.5 → STABLE
```

### Output

```json
{
  "title": "Team Lead Promotion",
  "growth_score": 75.6,
  "sustainability_score": 74.7,
  "tension_index": 0.9,
  "tension_severity": "LOW",
  "zone": "EXECUTE_FULLY",
  "zone_reason": "High growth and sustainable",
  "composite_score": 74.88,
  "risk_level": "STRUCTURALLY_STABLE",
  "triggered_messages": [],
  "sensitivity_range": 3.5,
  "stability_level": "STABLE",
  "decision_status": "SINGLE_OPTION_CLASSIFIED",
  "recommendation_reason": "Single option structurally evaluated and classified"
}
```

---

## 12. Criteria Reference Checklist

### For Growth Assessment

Typical growth criteria include:
- Career advancement / progression opportunity
- Skill/capability building
- Market value increase
- Domain expertise expansion
- Leadership experience
- Equity/financial upside
- Network expansion
- Credential value

### For Sustainability Assessment

Typical sustainability criteria include:
- Work-life balance / time availability
- Physical & mental health impact
- Relationship/family support
- Financial security / income stability
- Team/community support
- Rest & recovery opportunity
- Clarity & predictability
- Personal value alignment

---

## 13. Backend API Contract

### Request Format

```json
{
  "options": [
    {
      "title": "Option Name",
      "growth_criteria": [
        {"weight": 0-10, "impact": 0-10},
        ...
      ],
      "sustainability_criteria": [
        {"weight": 0-10, "impact": 0-10},
        ...
      ]
    },
    ...
  ]
}
```

### Response Format

```json
{
  "evaluations": [
    {
      "title": "Option Name",
      "growth_score": 0-100,
      "sustainability_score": 0-100,
      "tension_index": 0-100,
      "tension_severity": "LOW|MODERATE|HIGH|CRITICAL",
      "zone": "EXECUTE_FULLY|TIME_BOX|LIGHT_RECOVERY|STEADY_EXECUTION|AVOID",
      "zone_reason": "string",
      "composite_score": 0-100,
      "risk_level": "STRUCTURALLY_STABLE|...",
      "triggered_messages": ["string", ...],
      "sensitivity_range": 0-50,
      "stability_level": "STABLE|MODERATELY_STABLE|FRAGILE"
    }
  ],
  "recommended_option": "string or NO_CLEAR_WINNER",
  "decision_status": "SINGLE_OPTION_CLASSIFIED|CLOSE_COMPETITION|CLEAR_WINNER",
  "recommendation_reason": "string"
}
```

---

## 14. Key Insights

### 1. Asymmetric Penalty Philosophy
Burnout (high growth, low sustainability) is penalized **3× more** than stagnation. This reflects the psychological reality: burnout is an emergency, stagnation is a slow leak.

### 2. Composite Score as Viability Measure
The composite score captures both absolute performance AND the balance between growth and sustainability. It's the single number to compare options fairly.

### 3. Sensitivity as Decision Confidence
High sensitivity suggests your assessment assumptions are fragile. It doesn't mean the decision is wrong—it means you should verify your rate or importance estimates.

### 4. Zones as Strategy Frameworks
Zones are not "good vs. bad"—they're strategy types:
- **EXECUTE**: Do it wholeheartedly
- **TIME_BOX**: Do it temporarily with explicit exit
- **LIGHT_RECOVERY**: Pause growth, focus on foundation
- **STEADY_EXECUTION**: Maintain and explore
- **AVOID**: Skip it entirely

### 5. Triggers as Red Flags
Triggered messages highlight decision hazards. They're not deal-breakers—they're "pay attention here."

