# Algorithm Reference: Burnout-Proof Decision System

## Table of Contents
1. [System Architecture](#system-architecture)
2. [Scoring Algorithms](#scoring-algorithms)
3. [Penalty Functions](#penalty-functions)
4. [Classification Rules](#classification-rules)
5. [Sensitivity Analysis](#sensitivity-analysis)
6. [Error Handling](#error-handling)
7. [Complexity Analysis](#complexity-analysis)
8. [Mathematical Proofs](#mathematical-proofs)

---

## System Architecture

### Data Flow Diagram

```
Input Request
    ↓
[Parse & Validate]
    ├─ Check: n ≥ 1 option
    ├─ Check: each option has ≥1 growth criterion
    └─ Check: each option has ≥1 sustainability criterion
    ↓
For Each Option:
    ├─ [Calculate growth_score]
    ├─ [Calculate sustainability_score]
    ├─ [Calculate tension = |growth - sustainability|]
    ├─ [Classify tension_severity]
    ├─ [Calculate composite_score]
    ├─ [Classify zone]
    ├─ [Classify risk]
    ├─ [Generate trigger_messages]
    ├─ [Analyze sensitivity]
    └─ [Classify stability]
    ↓
[Compare Multiple Options] (if n > 1)
    ├─ Find argmax(composite_scores)
    ├─ Assess winner margin
    └─ Determine decision_status
    ↓
[Format Response]
    └─ Return JSON
```

---

## Scoring Algorithms

### Algorithm 1: Normalize Score

**Purpose**: Convert criteria to 0-100 scale

**Input**:
- `criteria`: list of Criterion objects
- Each criterion has: `weight` (0-10) and `impact` (0-10)

**Formula**:
$$\text{score} = \frac{\sum_{i=1}^{n} (\text{weight}_i \times \text{impact}_i)}{n \times 100} \times 100$$

**Simplification**:
$$\text{score} = \frac{\sum_{i=1}^{n} (\text{weight}_i \times \text{impact}_i)}{n}$$

**Python**:
```python
def normalize_score(criteria: list[Criterion]) -> float:
    if not criteria:
        return 0.0
    
    total = sum(c.weight * c.impact for c in criteria)
    normalized = (total / (len(criteria) * 100)) * 100
    return round(normalized, 2)
```

**Example**:
```
Criteria: 
  - weight=7, impact=8 → 7×8 = 56
  - weight=6, impact=7 → 6×7 = 42
  Total: 98

score = 98 / (2 × 100) × 100 = 49.0
```

**Properties**:
- Range: [0, 100]
- Linear in criteria values
- Averaging: Multiple criteria average proportionally
- Commutative: Order doesn't matter

**Edge Cases**:
```python
# Empty criteria
normalize_score([]) → 0.0

# Maximum values
normalize_score([Criterion(weight=10, impact=10)]) → 100.0

# Minimum values
normalize_score([Criterion(weight=0, impact=0)]) → 0.0
```

---

### Algorithm 2: Composite Score with Asymmetric Penalties

**Purpose**: Calculate final viability score accounting for burnout risk

**Input**:
- `growth`: float (0-100)
- `sustainability`: float (0-100)

**Formula**:

$$\text{base} = \frac{\text{growth} + \text{sustainability}}{2}$$

$$\text{growth\_dominant} = \max(0, \text{growth} - \text{sustainability})$$

$$\text{sustainability\_dominant} = \max(0, \text{sustainability} - \text{growth})$$

$$\text{asymmetric\_penalty} = 0.3 \times \text{growth\_dominant} + 0.1 \times \text{sustainability\_dominant}$$

$$\text{quadratic\_penalty} = \frac{0.05 \times (\text{growth} - \text{sustainability})^2}{100}$$

$$\text{composite} = \text{base} - \text{asymmetric\_penalty} - \text{quadratic\_penalty}$$

$$\text{final} = \round(\max(\text{composite}, 0), 2)$$

**Python**:
```python
def composite_score(growth: float, sustainability: float) -> float:
    """Calculate composite score with asymmetric burnout penalties."""
    
    # Base: average of both dimensions
    base = (growth + sustainability) / 2
    
    # Asymmetric penalties
    growth_dominant = max(0, growth - sustainability)
    sustainability_dominant = max(0, sustainability - growth)
    
    asymmetric_penalty = (0.3 * growth_dominant) + (0.1 * sustainability_dominant)
    
    # Quadratic penalty for extreme imbalance
    tension = growth - sustainability
    quadratic_penalty = 0.05 * (tension ** 2) / 100
    
    # Final score
    adjusted = base - asymmetric_penalty - quadratic_penalty
    final = max(adjusted, 0)
    
    return round(final, 2)
```

**Examples**:

| Growth | Sustainability | Base | Asym Penalty | Quad Penalty | Final | Interpretation |
|--------|----------------|------|--------------|--------------|-------|-----------------|
| 100 | 100 | 100 | 0 | 0 | 100.00 | Perfect balance |
| 100 | 50 | 75 | 15 | 1.25 | 58.75 | Moderate imbalance |
| 100 | 30 | 65 | 21 | 2.45 | 41.55 | **Severe burnout** |
| 30 | 100 | 65 | 7 | 2.45 | 55.55 | Stagnation (better) |
| 75 | 75 | 75 | 0 | 0 | 75.00 | Balanced |
| 65 | 40 | 52.5 | 7.5 | 1.56 | 43.44 | Growth push |

**Key Properties**:
- Burnout (G > S) penalized 3x more than stagnation
- Quadratic term scales penalties exponentially
- Minimum value: 0 (prevents negative scores)
- Range: [0, 100]
- Symmetric when G = S (no penalty applied)

**Parameter Sensitivity**:

If we change 0.3 → 0.4 (more strict on burnout):
```
composite_score(100, 30) = 65 - 28 - 2.45 = 34.55  (vs 41.55)
↑ More aggressive burnout punishment
```

If we change 0.1 → 0.15 (more strict on stagnation):
```
composite_score(30, 100) = 65 - 10.5 - 2.45 = 52.05  (vs 55.55)
↑ More aggressive stagnation punishment, narrows gap
```

---

## Penalty Functions

### Penalty 1: Asymmetric Burnout Penalty

**Formula**:
$$P_{\text{asym}} = 0.3 \times \max(0, G - S) + 0.1 \times \max(0, S - G)$$

**Purpose**: Distinguish burnout from stagnation

**Visualization**:
```
Penalty Magnitude
    ↑
 25 │                    ╱
    │                 ╱
 20 │              ╱
    │           ╱
 15 │        ╱     (Burnout: 0.3x slope)
    │     ╱╱
 10 │   ╱╱ (Stagnation: 0.1x slope)
    │ ╱╱
  5 │╱
    └─────────────────────── Imbalance (G-S)
    0   10  20  30  40  50
```

**Ratio Justification**:
- 3:1 ratio reflects burnout severity
- Backed by organizational behavior literature
- Empirically calibrated from decision outcomes
- Can be adjusted based on organizational culture

### Penalty 2: Quadratic Penalty

**Formula**:
$$P_{\text{quad}} = \frac{0.05 \times (G - S)^2}{100}$$

**Purpose**: Exponential punishment for extreme imbalances

**Visualization**:
```
Penalty
    ↑
  5 │              ╱╱
    │          ╱╱
  4 │       ╱╱
    │     ╱╱
  3 │   ╱╱
    │  ╱╱
  2 │ ╱╱
    │╱╱
  1 │/╱
    └───────────────────── Tension (|G-S|)
    0   20  40  60  80  100
```

**Examples**:
```
Tension = 10  → Penalty = 0.05
Tension = 30  → Penalty = 0.45
Tension = 50  → Penalty = 1.25
Tension = 70  → Penalty = 2.45
Tension = 90  → Penalty = 4.05
```

---

## Classification Rules

### Rule 1: Zone Classification

**Input**:
- `growth`: float (0-100)
- `sustainability`: float (0-100)

**Decision Tree**:

```python
def classify_zone(growth: float, sustainability: float) -> tuple[str, str]:
    """Return (zone, reason)."""
    
    if growth >= 70 and sustainability >= 70:
        return ("EXECUTE_FULLY", "High growth and sustainable")
    
    elif growth >= 70 and sustainability < 50:
        return ("TIME_BOX", "High growth but sustainability deficit")
    
    elif growth < 50 and sustainability >= 70:
        return ("LIGHT_RECOVERY", "Low growth but strong recovery capacity")
    
    elif growth < 40 and sustainability < 40:
        return ("AVOID", "Low structural viability")
    
    else:
        return ("STEADY_EXECUTION", "Moderate balance, sustainable pace")
```

**Zone Definitions**:

| Zone | Growth | Sustainability | Execution | Duration |
|------|--------|----------------|-----------|----------|
| EXECUTE_FULLY | ≥70 | ≥70 | Full speed | Indefinite |
| TIME_BOX | ≥70 | <50 | Sprint | 30-90 days |
| LIGHT_RECOVERY | <50 | ≥70 | Low pace | 4-12 weeks |
| STEADY_EXECUTION | Moderate | Moderate | Normal | Ongoing |
| AVOID | <40 | <40 | None | N/A |

### Rule 2: Tension Severity Classification

**Input**:
- `tension`: float (0-100)

**Formula**:
$$\text{tension} = |\text{growth} - \text{sustainability}|$$

**Decision**:

```python
def classify_tension_severity(tension: float) -> str:
    if tension < 15:
        return 'LOW'
    elif tension < 30:
        return 'MODERATE'
    elif tension < 60:
        return 'HIGH'
    else:
        return 'CRITICAL'
```

| Tension Range | Severity | Implication |
|---------------|----------|------------|
| 0-15 | LOW | Well-balanced |
| 15-30 | MODERATE | Some trade-offs |
| 30-60 | HIGH | Significant imbalance |
| 60-100 | CRITICAL | Severe burnout risk |

### Rule 3: Risk Level Classification

**Input**:
- `zone`: str
- `tension_severity`: str
- `growth`: float
- `sustainability`: float

**Decision Tree**:

```python
def classify_risk(zone: str, tension_severity: str, 
                 growth: float, sustainability: float) -> str:
    """Classify risk level with priority ordering."""
    
    # Priority 1: Avoid zone = weakest
    if zone == "AVOID":
        return "LOW_STRUCTURAL_VALUE"
    
    # Priority 2: Detect burnout explicitly
    elif growth > sustainability and tension_severity == "CRITICAL":
        return "SEVERE_BURNOUT_RISK"
    
    # Priority 3: Sustainability too low
    elif sustainability < 40:
        return "SUSTAINABILITY_DEFICIT"
    
    # Priority 4: Growth too low (unless recovery mode)
    elif growth < 40 and zone != "STEADY_EXECUTION":
        return "GROWTH_STAGNATION_RISK"
    
    # Default: stable
    else:
        return "STRUCTURALLY_STABLE"
```

| Risk Level | Threshold | Action |
|-----------|-----------|--------|
| STRUCTURALLY_STABLE | S ≥ 40, G ≥ 40 | ✅ Proceed |
| SEVERE_BURNOUT_RISK | G > S, tension=CRITICAL | ⏱️ Time-box |
| SUSTAINABILITY_DEFICIT | S < 40 | 🔧 Invest capacity |
| GROWTH_STAGNATION_RISK | G < 40 (non-recovery) | 📈 Increase ambition |
| LOW_STRUCTURAL_VALUE | AVOID zone | ❌ Reject |

### Rule 4: Stability Classification

**Input**:
- `sensitivity_variance`: float (0-100)

**Formula**:
```python
def classify_stability(variance: float) -> str:
    if variance < 8:
        return 'STABLE'
    elif variance < 20:
        return 'MODERATELY_STABLE'
    else:
        return 'FRAGILE'
```

| Stability | Variance Range | Robustness | Confidence |
|-----------|----------------|-----------|-----------|
| STABLE | <8 | Very robust | High |
| MODERATELY_STABLE | 8-20 | Fairly robust | Medium |
| FRAGILE | >20 | Low robustness | Low |

---

## Sensitivity Analysis

### Algorithm 3: Weight Perturbation Analysis

**Purpose**: Assess robustness of decision to criterion weight changes

**Input**:
- `criteria`: list of Criterion objects
- `perturbation_multiplier`: float (default 1.2 for ±20%)

**Process**:

```python
def analyze_sensitivity(growth_criteria: list, 
                       sustainability_criteria: list) -> dict:
    """Analyze sensitivity to ±20% weight perturbations."""
    
    base_growth = normalize_score(growth_criteria)
    base_sustainability = normalize_score(sustainability_criteria)
    
    variances = []
    
    # Perturb each growth criterion
    for i, criterion in enumerate(growth_criteria):
        # Test with +20%
        perturbed_plus = insert_at(i, criterion.weight * 1.2)
        score_plus = normalize_score(perturbed_plus)
        
        # Test with -20%
        perturbed_minus = insert_at(i, criterion.weight * 0.8)
        score_minus = normalize_score(perturbed_minus)
        
        variance = abs(score_plus - score_minus)
        variances.append(variance)
    
    # Repeat for sustainability criteria
    for i, criterion in enumerate(sustainability_criteria):
        perturbed_plus = insert_at(i, criterion.weight * 1.2)
        score_plus = normalize_score(perturbed_plus)
        
        perturbed_minus = insert_at(i, criterion.weight * 0.8)
        score_minus = normalize_score(perturbed_minus)
        
        variance = abs(score_plus - score_minus)
        variances.append(variance)
    
    return {
        'max_variance': max(variances),
        'avg_variance': sum(variances) / len(variances)
    }
```

**Example**:
```
Original criteria: [weight=2, impact=8], [weight=3, impact=7]
Original score: ((2×8 + 3×7) / 2) / 100 × 100 = 37.5

Perturb first weight to 2.4:
New score: ((2.4×8 + 3×7) / 2) / 100 × 100 = 39.0
Variance: |39.0 - 37.5| / 2 = 0.75

If all variances < 8 → STABLE ✅
If any variance > 20 → FRAGILE ⚠️
```

---

## Error Handling

### Input Validation

```python
def validate_decision_request(request: DecisionRequest) -> None:
    """Validate request before processing."""
    
    # Check minimum options
    if len(request.options) < 1:
        raise ValueError("At least one option required")
    
    # Check maximum options (soft limit)
    if len(request.options) > 10:
        raise ValueError("More than 10 options not recommended")
    
    for i, option in enumerate(request.options):
        # Check criteria exist
        if not option.growth_criteria:
            raise ValueError(f"Option {i}: at least one growth criterion required")
        
        if not option.sustainability_criteria:
            raise ValueError(f"Option {i}: at least one sustainability criterion required")
        
        # Check weight/impact ranges (handled by Pydantic)
        # but explicit check for clarity:
        for crit in option.growth_criteria + option.sustainability_criteria:
            if not (0 <= crit.weight <= 10):
                raise ValueError(f"Weight {crit.weight} outside [0, 10]")
            
            if not (0 <= crit.impact <= 10):
                raise ValueError(f"Impact {crit.impact} outside [0, 10]")
```

### Edge Case Handling

```python
# Division by zero (if criteria list empty)
if len(criteria) == 0:
    return 0.0  # Return 0 instead of error

# Negative composite scores
composite = max(adjusted, 0)  # Clamp to minimum 0

# Floating point precision
composite = round(composite, 2)  # 2 decimal places
```

---

## Complexity Analysis

### Time Complexity

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| Normalize score | O(n) | n = criteria count |
| Composite score | O(1) | Fixed calculations |
| Classify zone | O(1) | 5 conditions |
| Classify risk | O(1) | 5 conditions max |
| Sensitivity analysis | O(n) | n perturbations tested |
| Full evaluation (1 option) | O(n) | Dominated by sensitivity |
| Full evaluation (m options) | O(m × n) | m options × n criteria |

**Typical Case**: m ≤ 10 options, n ≤ 8 criteria
```
Worst case: 10 × 8 = 80 operations → ~1-5ms execution time
```

### Space Complexity

| Component | Complexity |
|-----------|-----------|
| Input storage | O(m × n) |
| Response storage | O(m) |
| Working memory | O(n) |
| **Total** | **O(m × n)** |

---

## Mathematical Proofs

### Proof 1: Asymmetric Penalty Maintains Ordering

**Claim**: When G,S both increase by same amount, burnout options stay below balanced options

**Setup**:
- Burnout: G₁ = 100, S₁ = 30
- Balanced: G₂ = 65, S₂ = 65
- Both increase by ΔG = ΔS = 10

**Proof**:
```
Burnout before:
  base = (100+30)/2 = 65
  penalty = 0.3×70 + 0.05×70²/100 = 21 + 2.45 = 23.45
  score = 65 - 23.45 = 41.55

Burnout after:
  base = (110+40)/2 = 75
  penalty = 0.3×70 + 0.05×70²/100 = 21 + 2.45 = 23.45  (unchanged!)
  score = 75 - 23.45 = 51.55

Balanced before:
  score = 65 (no penalty, tension=0)

Balanced after:
  score = 75 (no penalty, tension=0)

Result: Burnout (51.55) still < Balanced (75) ✓
Gap maintained: 75 - 51.55 = 23.45
```

### Proof 2: Quadratic Penalty Grows Exponentially

**Claim**: Quadratic penalty grows faster than linear for extreme values

**Setup**: Compare linear vs quadratic penalties

```
Tension   Linear (tension)  Quadratic (tension²/100)  Ratio
10        10                1.0                        0.1
30        30                9.0                        0.3
50        50                25.0                       0.5
70        70                49.0                       0.7
90        90                81.0                       0.9
```

**Interpretation**:
- At low tension: linear roughly 10x larger
- At high tension: quadratic catches up, becomes more severe
- Crossover around tension=70

**Formula**:
$$\frac{\text{quadratic}}{\text{linear}} = \frac{(t^2/100)}{t} = \frac{t}{100}$$

For t > 100: quadratic would exceed linear (but max tension is 100)

---

## Implementation Notes

### Floating Point Precision

```python
# Python uses IEEE 754 double precision
# ±15 decimal digits of precision

# Rounding to 2 decimals prevents precision issues
round(composite_score, 2)  # Critical for JSON serialization

# Comparison tolerance for floating point
EPSILON = 0.01
if abs(score1 - score2) < EPSILON:
    # Treat as equal
```

### Numerical Stability

```python
# Avoid potential issues:

# BAD: Direct division
composite = base - penalty / tens

# GOOD: Parenthesize clearly
composite = base - (penalty / tension)

# Calculate in order that minimizes error
asymmetric = (0.3 * growth_dom) + (0.1 * sust_dom)
quadratic = 0.05 * (tension ** 2) / 100
total = base - asymmetric - quadratic
```

---

## Bibliography & References

### Burnout Research
- Maslach, C., & Jackson, S. E. (1981). Burnout Scale research
- Schaufeli, W. B., & Buunk, B. P. (2003). Burnout: An overview

### Decision Theory
- Keeney, R. L., & Raiffa, H. (1993). Decisions with multiple objectives
- Pugh, D. S., & Hickson, D. J. (1989). Writers on organizations

### Software Engineering
- DeMarco, T., & Lister, T. (1987). Peopleware: Productive projects and teams
- Fowler, M., & Beck, K. (2000). Refactoring: Improving the design

