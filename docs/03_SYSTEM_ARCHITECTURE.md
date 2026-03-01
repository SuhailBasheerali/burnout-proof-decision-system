# System Architecture: Burnout-Proof Decision System

## Overview

The Burnout-Proof Decision System consists of a **FastAPI REST API** backed by a **modular decision engine** that evaluates options across growth and sustainability dimensions through a 8-step evaluation pipeline.

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                      │
│                    (app/main.py)                            │
└────────────────────┬────────────────────────────────────────┘
                     │
         ┌───────────┴──────────┐
         │                      │
    ┌────▼──────┐         ┌────▼──────┐
    │ /decision │         │  /health  │
    │ /compare  │         │  endpoint │
    └────┬──────┘         └───────────┘
         │
┌────────▼──────────────────────────────────────────────────────┐
│              Decision Evaluation Pipeline                      │
│                  (8-step processing)                          │
├──────────────────────────────────────────────────────────────┤
│ 1. Normalize Scores     (0-100)       → engine/evaluator.py   │
│ 2. Calculate Tension    (imbalance)   → evaluator.py          │
│ 3. Classify Zone        (5 zones)     → engine/classifier.py  │
│ 4. Composite Score      (penalized)   → evaluator.py          │
│ 5. Risk Classification  (6 levels)    → engine/classifier.py  │
│ 6. Trigger Messages     (warnings)    → engine/triggers.py    │
│ 7. Sensitivity Analysis (robustness)  → engine/sensitivity.py │
│ 8. Stability Level      (STABLE/etc)  → engine/sensitivity.py │
└────────────────────┬─────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
   ┌────▼─────────┐      ┌───────▼────────┐
   │ Single Option│      │Multiple Options│
   │  Assessment  │      │   Comparison   │
   └──────────────┘      └────────────────┘
        │                         │
   ┌────▼──────────────────────────▼──────────────┐
   │       Response Formatting (app/main.py)      │
   └───────────────────────────────────────────────┘
        │
   ┌────▼────────────────────────────────────────┐
   │    JSON Response (decision_status + data)   │
   └─────────────────────────────────────────────┘
```

---

## Component Architecture

### 1. API Layer (`app/main.py`)

**Responsibility**: Handle HTTP requests, orchestrate evaluation, format responses

**Key Functions**:
- `POST /decision/compare` — Main endpoint
- Validation via Pydantic schemas
- Request parsing and response formatting
- Eight-step evaluation orchestration

**Evaluation Pipeline Flow**:
```python
for each option:
    1. growth_score = normalize_score(growth_criteria)
    2. sustainability_score = normalize_score(sustainability_criteria)
    3. tension_index = abs(growth - sustainability)
    4. zone = classify_zone(growth, sustainability)
    5. composite_score = composite_score_function(growth, sustainability)
    6. risk_level = classify_risk(zone, tension, growth, sustainability)
    7. messages = generate_triggers(growth, sustainability, risk, zone)
    8. sensitivity = analyze_sensitivity(growth_criteria, sustainability_criteria)
    9. stability = classify_stability(sensitivity.variance)
```

**Response Decision Logic**:
```python
if len(options) == 1:
    return SINGLE_OPTION_CLASSIFIED
elif len(options) > 1:
    winner = argmax(composite_scores)
    if max_composite - min_composite > CLEAR_WINNER_THRESHOLD:
        return CLEAR_WINNER
    elif all_composites < POOR_FIT_THRESHOLD:
        return ALL_OPTIONS_POOR_FIT
    else:
        return CLOSE_COMPETITION
```

---

### 2. Validation Layer (`app/schemas.py`)

**Responsibility**: Define request/response schemas with Pydantic validation

**Key Models**:

```python
class Criterion(BaseModel):
    weight: float = Field(..., ge=0, le=10)      # 0-10 scale
    impact: float = Field(..., ge=0, le=10)      # 0-10 scale

class DecisionOption(BaseModel):
    title: str
    growth_criteria: list[Criterion]             # ≥1 required
    sustainability_criteria: list[Criterion]     # ≥1 required

class DecisionRequest(BaseModel):
    options: list[DecisionOption]                # 1-10 options

class EvaluationResult(BaseModel):
    title: str
    growth_score: float
    sustainability_score: float
    tension_index: float
    tension_severity: str
    composite_score: float
    zone: str
    zone_reason: str
    risk_level: str
    stability_level: str
    sensitivity_range: float
    triggered_messages: list[str]

class DecisionResponse(BaseModel):
    decision_status: str
    decision_winner: Optional[str]               # Multi-option only
    winner_idx: Optional[int]                    # Multi-option only
    winner_explanation: Optional[str]            # Multi-option only
    evaluations: list[EvaluationResult]
    all_options_poor_fit: bool
    poor_fit_reason: Optional[str]
```

---

### 3. Evaluator (`app/engine/evaluator.py`)

**Responsibility**: Core numerical calculations (scoring, tension, composite)

**Key Functions**:

#### `normalize_score(criteria_list: list[Criterion]) -> float`
Converts criteria to 0-100 scale:
```
Score = (Σ(weight × impact) / (n × 100)) × 100
```

Example:
```
Criteria: [weight:7, impact:8], [weight:6, impact:7]
Score = ((7×8 + 6×7) / (2×100)) × 100
      = (56 + 42) / 2 / 100 × 100
      = 49 / 100 × 100
      = 49/100
```

#### `composite_score(growth: float, sustainability: float) -> float`
Applies asymmetric burnout penalty:
```
base = (growth + sustainability) / 2

growth_dominant = max(0, growth - sustainability)
sustainability_dominant = max(0, sustainability - growth)

asymmetric_penalty = (0.3 × growth_dominant) + (0.1 × sustainability_dominant)
quadratic_penalty = 0.05 × (tension²) / 100
adjusted = base - asymmetric_penalty - quadratic_penalty

final = round(max(adjusted, 0), 2)
```

**Why this formula?**
- Base is average of both scores
- Burnout (high G, low S) penalized 0.3× per imbalance point
- Stagnation (low G, high S) penalized only 0.1× per imbalance point
- 3:1 ratio reflects burnout being 3x worse than stagnation
- Quadratic term captures catastrophic imbalances

**Example**:
```
Growth: 100, Sustainability: 30
base = (100+30)/2 = 65
growth_dominant = 100-30 = 70
penalty = 0.3 × 70 + 0.05 × 70²/100 = 21 + 2.45 = 23.45
composite = 65 - 23.45 = 41.55 ⚠️ Severe burnout trap
```

---

### 4. Classifier (`app/engine/classifier.py`)

**Responsibility**: Categorize options (zone, risk level)

#### `classify_zone(growth: float, sustainability: float) -> tuple[str, str]`

Decision matrix:
```
┌─────────┬──────────┬──────────┬──────────┬──────────┐
│ Growth  │ S ≥70    │ S 50-70  │ S 30-50  │ S <30    │
├─────────┼──────────┼──────────┼──────────┼──────────┤
│ G ≥70   │ EXECUTE  │ EXECUTE  │ TIME_BOX │ TIME_BOX │
│         │ (healthy)│ (healthy)│ (sprint) │ (sprint) │
├─────────┼──────────┼──────────┼──────────┼──────────┤
│ G 50-70 │ EXECUTE  │ STEADY   │ STEADY   │ LIGHT_   │
│         │ (growth) │ (balance)│ (caution)│ RECOVERY │
├─────────┼──────────┼──────────┼──────────┼──────────┤
│ G 30-50 │ LIGHT_   │ STEADY   │ STEADY   │ AVOID    │
│         │ RECOVERY │ (caution)│ (caution)│ (weak)   │
├─────────┼──────────┼──────────┼──────────┼──────────┤
│ G <30   │ LIGHT_   │ LIGHT_   │ AVOID    │ AVOID    │
│         │ RECOVERY │ RECOVERY │ (weak)   │ (weak)   │
└─────────┴──────────┴──────────┴──────────┴──────────┘
```

#### `classify_risk(zone: str, tension_severity: str, growth: float, sustainability: float) -> str`

Risk decision tree:
```
1. If zone == AVOID → LOW_STRUCTURAL_VALUE
2. Else if growth > sustainability AND tension_severity == CRITICAL
   → SEVERE_BURNOUT_RISK
3. Else if sustainability < 40 → SUSTAINABILITY_DEFICIT
4. Else if growth < 40 AND zone != STEADY_EXECUTION → GROWTH_STAGNATION_RISK
5. Else → STRUCTURALLY_STABLE
```

---

### 5. Triggers (`app/engine/triggers.py`)

**Responsibility**: Generate contextual warning messages

**Trigger Rules**:
```python
triggers = []

# Burnout trap detection
if growth >= 75 and sustainability < 35:
    triggers.append("⚠️ CRITICAL: Burnout trap detected...")

# Sustainability warnings
if sustainability < 40:
    triggers.append("Sustainability below structural stability threshold...")

# Imbalance warnings  
if abs(growth - sustainability) > 40:
    triggers.append("Significant imbalance between growth and sustainability...")

# Growth insufficiency
if growth < 40 and zone != "STEADY_EXECUTION":
    triggers.append("Growth below minimum threshold...")
```

**Example Output**:
```python
[
    "⚠️ CRITICAL: Burnout trap detected - high growth demands exceed sustainability capacity.",
    "Sustainability below structural stability threshold.",
    "Significant imbalance between growth and sustainability."
]
```

---

### 6. Sensitivity Analysis (`app/engine/sensitivity.py`)

**Responsibility**: Assess robustness via weight perturbation

**Algorithm**:
```python
def analyze_sensitivity(growth_criteria, sustainability_criteria):
    results = []
    
    # Perturb each weight by ±20%
    for i, criterion in enumerate(growth_criteria):
        original_weight = criterion.weight
        
        # Test with +20%
        criteria_plus = modify_weight(criteria, i, original_weight * 1.2)
        score_plus = normalize_score(criteria_plus)
        
        # Test with -20%
        criteria_minus = modify_weight(criteria, i, original_weight * 0.8)
        score_minus = normalize_score(criteria_minus)
        
        variance = abs(score_plus - score_minus)
        results.append(variance)
    
    return {
        "growth_variance": max(variance for growth criteria),
        "sustainability_variance": max(variance for sustainability criteria),
        "total_variance": max(all variances)
    }
```

**Interpretation**:
- Small variance (<8) = STABLE → Robust to changes
- Medium variance (8-20) = MODERATELY_STABLE → Watch key metrics
- Large variance (>20) = FRAGILE → Risky, verify assumptions

---

## Data Flow

### Request Flow
```
Raw JSON Request
    ↓
[Pydantic Validation] - schemas.py
    ↓
[Criteria Parsing]
    ↓
For Each Option:
    ├─ [Normalize] → growth_score, sustainability_score
    ├─ [Tension] → tension_index, tension_severity
    ├─ [Zone] → zone, zone_reason
    ├─ [Composite] → composite_score
    ├─ [Risk] → risk_level
    ├─ [Triggers] → triggered_messages
    ├─ [Sensitivity] → sensitivity_range
    └─ [Stability] → stability_level
    ↓
[Decision Logic]
    ├─ If single: SINGLE_OPTION_CLASSIFIED
    └─ If multiple: CLEAR_WINNER / CLOSE_COMPETITION / ALL_OPTIONS_POOR_FIT
    ↓
Response Formatting
    ↓
JSON Response to Client
```

---

## Module Dependencies

```
app/main.py (FastAPI app)
    ├── app/schemas.py (Pydantic models)
    └── app/engine/ (Decision engine)
        ├── evaluator.py (scoring, tension, composite)
        ├── classifier.py (zone, risk)
        ├── triggers.py (warning messages)
        └── sensitivity.py (robustness analysis)
```

**Dependency Graph**:
```
main.py
  ├─→ schemas.py (validation)
  ├─→ evaluator.py (normalize, composite_score)
  ├─→ classifier.py (classify_zone, classify_risk)
  ├─→ triggers.py (generate_triggers)
  └─→ sensitivity.py (analyze_sensitivity)

No circular dependencies
Clean separation of concerns
```

---

## Performance Characteristics

### Time Complexity
- Single option: O(n) where n = total criteria count
- Multiple options: O(m × n) where m = option count, n = criteria
- Typical: m ≤ 10, n ≤ 8 → ~80 operations

### Space Complexity
- Request: O(m × n)
- Response: O(m) for results + O(m × t) for triggered messages where t ≈ 3

### Latency Expectations
- P50: <50ms
- P95: <100ms
- P99: <200ms

### Bottlenecks
None identified. Sensitivity analysis (8 perturbations per option) is the most expensive operation but still negligible.

---

## Extensibility

### Adding New Zone Types
Edit [classifier.py](../app/engine/classifier.py):
```python
def classify_zone(...):
    # Add new condition
    if growth > 80 and sustainability > 80 and tension < 5:
        return "RAPID_SCALING_WITH_HEALTH", "Rare state..."
```

### Adding New Risk Levels
Edit [classifier.py](../app/engine/classifier.py):
```python
def classify_risk(...):
    # Add new priority
    if specific_condition:
        return "NEW_RISK_TYPE"
```

### Adding New Trigger Messages
Edit [triggers.py](../app/engine/triggers.py):
```python
def generate_triggers(...):
    if new_condition:
        messages.append("Custom warning message")
```

### Adjusting Penalty Weights
Edit [evaluator.py](../app/engine/evaluator.py):
```python
# Change asymmetric penalty ratio
asymmetric_penalty = (0.4 * growth_dominant) + (0.1 * sustainability_dominant)
```

### Adding New Criteria Dimensions
Would require schema updates (add new dimension with its own criteria) and updating the composite score function.

---

## Testing Structure

**Test Files**:
- `tests/test_api.py` — 15 endpoint tests (realistic scenarios)
- `tests/test_engine_logic.py` — 7 unit tests (scoring functions)
- `tests/test_validation.py` — 3 validation tests (schema constraints)

**Total Coverage**: 25 tests, all passing

---

## Deployment

### Local Development
```bash
python -m uvicorn app.main:app --reload --port 8000
```

### Production
```bash
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

### Docker
```dockerfile
FROM python:3.13
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app/ app/
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Web Framework | FastAPI | Latest |
| Validation | Pydantic | Latest |
| Server | Uvicorn | Latest |
| Language | Python | 3.13 |
| Testing | pytest | Latest |

---

## Future Enhancements

1. **Empirical Calibration**: Threshold tuning based on historical data
2. **Machine Learning**: Learn penalty weights from past decisions
3. **Scenario Analysis**: "What-if" tools for criteria changes
4. **Integration**: Slack/Teams bot for quick decisions
5. **Dashboard**: UI for scenario building and visualization
6. **A/B Testing**: Compare decision effectiveness over time

