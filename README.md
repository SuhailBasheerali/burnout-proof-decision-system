# 🧠 Burnout-Proof Decision Companion System

**A deterministic, explainable decision support system designed to help users make better choices while recognizing cognitive fatigue and decision quality trade-offs.**

---

## 📋 Table of Contents

1. [Problem Statement & Motivation](#problem-statement--motivation)
2. [Conceptual Interpretation](#conceptual-interpretation)
3. [System Architecture](#system-architecture)
4. [Design Principles](#design-principles)
5. [Design Decisions & Rationale](#design-decisions--rationale)
6. [Mathematical Foundations](#mathematical-foundations)
7. [Assumptions Made](#assumptions-made)
8. [Edge Cases & Handling](#edge-cases--handling)
9. [How to Run the Project](#how-to-run-the-project)
10. [Project Structure](#project-structure)
11. [Future Improvements](#future-improvements)
12. [Technical Stack](#technical-stack)

---

## 🎯 Problem Statement & Motivation

### The Challenge
Design a **Decision Companion System** that helps users evaluate options against multiple criteria without relying entirely on AI. The system must:
- Accept multiple options
- Accept criteria with different weights/importance
- Process and evaluate objectively
- Provide ranked recommendations with clear explanations
- Work deterministically, not as a black box

### Why "Burnout-Proof"?
The unique angle of this implementation is recognizing that **decision quality degrades under cognitive fatigue**. When burned out:
- Users make impulsive choices
- They over-weight short-term gains
- They underestimate long-term sustainability
- They rationalize poor decisions post-hoc

Therefore, the system explicitly penalizes **high-growth, low-sustainability** combinations (classic burnout traps) and prioritizes **balance** over extreme outcomes.

---

## 🧩 Conceptual Interpretation

### What This Problem Really Tests
From my understanding, this assignment evaluates:

✅ **Ability to model real-world trade-offs** — Most decisions involve compromises, not clear winners
✅ **Weighted multi-criteria evaluation** — Not all criteria are equally important
✅ **Transparent reasoning** — Users need to understand *why*, not just get an answer
✅ **Logical decision flow** — Structured reasoning, not black-box opaqueness
✅ **System design thinking** — Separating concerns, designing for explainability, handling edge cases
✅ **Separation of layers** — Core deterministic logic vs. optional enhancements

### NOT Testing
❌ ML expertise or fancy AI models
❌ Hardcoded decision rules
❌ Fully automated decision-making

### My Core Insight
**The real problem is not ranking options—it's modeling *rational decision-making under constraints*.**

In real-world decisions:
- Options are rarely absolutely good or bad
- Trade-offs **always** exist
- Importance varies by user context
- Decision quality depends on clarity of reasoning
- Users need to trust the system enough to act on it

Therefore, a proper system must:
1. **Quantify trade-offs** — Show growth vs. sustainability, tension, risk
2. **Respect user weights** — Let users define what matters
3. **Filter infeasible options** — Eliminate non-viable choices early
4. **Explain reasoning** — Every output must be justifiable
5. **Adapt to context** — Handle 1 option differently from 5

---

## 🏗️ System Architecture

### Three-Tier Design

```
TIER 1: DETERMINISTIC CORE (100% AI-Free) ✅
  ├─ Evaluation Engine (6 components)
  │  ├─ Score normalization
  │  ├─ Zone classification (EXECUTE_FULLY → AVOID)
  │  ├─ Tension detection (growth vs. sustainability imbalance)
  │  ├─ Risk assessment (6 risk levels including burnout pathways)
  │  ├─ Sensitivity analysis (±20% weight perturbations)
  │  └─ Stability grading (STABLE → MODERATELY_STABLE → FRAGILE)
  │
  └─ Comparison Logic (8-step pipeline)
     ├─ Input validation
     ├─ Individual option evaluation
     ├─ Multi-option ranking
     ├─ Decision status classification
     └─ Output composition

TIER 2: API LAYER (FastAPI)
  ├─ /decision/compare — Deterministic decision evaluation
  └─ /decision/reflect — Optional wisdom with 4-layer fallback

TIER 3: FRONTEND (Streamlit)
  ├─ Interactive option builder
  ├─ Criteria weight visualization
  ├─ Real-time evaluation dashboard
  └─ Decision history tracking
```

### Why This Architecture?

**Separation of Concerns:**
- Core logic is **completely decoupled** from API/UI
- Can be tested independently, called by different interfaces
- Deterministic core never makes external API calls

**Modularity:**
- Each component (evaluator, classifier, etc.) is a self-contained function
- Easy to unit test, modify, or replace
- Clear responsibility boundaries

**Resilience:**
- Optional AI layer (wisdom reflection) has 4-layer fallback
- System works perfectly without Gemini API
- Graceful degradation when quota exhausted

---

## 🎓 Design Principles

### 1. **Deterministic > Probabilistic**
The core evaluation engine uses pure logic, not ML models. This ensures:
- **Reproducibility**: Same inputs → same outputs, always
- **Explainability**: Every decision can be traced and justified
- **Reliability**: Works offline, no dependency on external services
- **Auditability**: Academic and professional trust

### 2. **Explainability > Accuracy**
A system users don't understand is useless, even if technically correct. Therefore:
- Every numeric output has a justification
- All thresholds are documented (why 8 points? why 5 for STABLE?)
- Sensitivity analysis shows which criteria matter most
- Users see the "why", not just the "what"

### 3. **Asymmetric Penalty for Burnout**
Trade-offs are not symmetrical. This is key:
- **High growth + Low sustainability** (burnout trap): 3x penalty
- **Low growth + High sustainability** (stagnation): 0.3x penalty

Rationale: Growth-dominant imbalances are more damaging to humans than sustainability-dominant ones. A person in a dead-end job can recover; someone in a burnout spiral often cannot.

### 4. **Balance Over Extremes**
The composite score formula ensures:
- A balanced 50/50 option scores higher than 90/10
- Counterintuitive but correct for human welfare optimization
- Prevents the system from recommending obviously unsustainable choices

### 5. **Context-Aware Thresholds**
Thresholds adjust based on decision stability (from sensitivity analysis):
- **STABLE scores** (<8% variance): ±5 point margin = clear winner
- **Mixed stability** (one STABLE, one MODERATELY_STABLE): ±8 point margin
- **MODERATELY_STABLE or both** (8-20% variance): ±8 point margin
- **FRAGILE scores** (≥20% variance): ±12 point margin = requires higher confidence
- Prevents overconfident decisions on shaky foundations by raising thresholds for uncertain evaluations

---

## ⚙️ Design Decisions & Rationale

### Decision 1: Weighted Normalization Over Absolute Scores
**Choice:** Allow users to define criteria weights, then normalize each option's performance on each criterion
**Why:** 
- Different users care about different things
- A "perfect" option doesn't exist in complex decisions
- Weights encode user preferences objectively

### Decision 2: Zone Classification (5 Strategic Categories)
**Choice:** Classify options into strategic zones before evaluating risk
```
EXECUTE_FULLY       → High growth, high sustainability
TIME_BOX            → High growth, low sustainability (burnout trap)
LIGHT_RECOVERY      → Low growth, high sustainability (safe recovery)
STEADY_EXECUTION    → Moderate both (balanced)
AVOID               → Low growth, low sustainability (non-viable)
```
**Why:**
- Users intuitively understand "zones" vs. abstract scores
- Helps identify option type at a glance
- Enables zone-specific risk assessment

### Decision 3: Asymmetric Composite Score Penalty
**Choice:** Apply 3x penalty to growth-dominant imbalances, 0.1x to sustainability-dominant
**Formula:**
```
base_score = (growth + sustainability) / 2
penalty = 0.3 * growth_dominant + 0.1 * sustainability_dominant
composite = base - penalty - quadratic_tail
```
**Why:**
- Empirically, high growth + low sustainability (burnout) is more damaging
- Gradient descent toward balance, not symmetrically
- Explains why system recommends "boring" balanced options

### Decision 4: 6-Level Risk Classification System
**Choice:** Identify specific risk pathways, not generic "risk score"
```
Risk Levels:
1. STRUCTURALLY_UNSALVAGEABLE  → In AVOID zone
2. SEVERE_BURNOUT_RISK          → CRITICAL tension + growth dominance
3. SUSTAINABILITY_DEFICIT       → Sustainability < 40
4. SEVERE_STAGNATION_RISK       → High tension + growth dominance
5. GROWTH_STAGNATION_RISK       → Growth < 40
6. STRUCTURALLY_STABLE          → All other cases
```
**Why:**
- Generic "risk score" is meaningless
- Specific pathways explain *how* things can go wrong
- Users can mitigate specific risks differently
- Enables targeted guidance via triggers

### Decision 5: Sensitivity Analysis via Weight & Impact Perturbations
**Choice:** Vary criteria weights ±20% AND impacts ±15%, measure worst-case score variance
**Why:**
- Shows which criteria are "critical" vs. "cosmetic"
- Tests both importance estimates AND effect magnitude estimates
- Quantifies decision confidence without being overconfident
- Identifies fragile decisions (depend on 1-2 criteria)
- Stability grading (STABLE/MODERATELY_STABLE/FRAGILE) based on variance
- Uses combined sensitivity (worst-case) for most conservative assessment

### Decision 6: Multi-Level Decision Status Classification
**Choice:** Don't just rank—classify the *decision type*
```
SINGLE_OPTION_CLASSIFIED      → 1 option only
CLEAR_WINNER                  → >8 point margin (deterministic)
CLOSE_COMPETITION             → ≤8 point margin (tough choice)
ALL_OPTIONS_POOR_FIT          → All score <40 (no viable option)
RANKED_COMPARISON             → Clear ranking exists
```
**Why:**
- Users need different guidance per scenario
- CLEAR_WINNER: "Go ahead, confident choice"
- CLOSE_COMPETITION: "Hard decision, consider soft factors"
- ALL_OPTIONS_POOR_FIT: "None are good; reframe the problem"

### Decision 7: Optional AI Layer with 4-Layer Fallback
**Choice:** AI wisdom is optional, with graceful degradation
```
Layer 1: 24-hour cache         (fastest, free)
Layer 2: Daily rate limit check (100 calls/day)
Layer 3: Gemini API call       (if quota available)
Layer 4: Fallback wisdom       (hardcoded, always works)
```
**Why:**
- Core decision logic never depends on AI
- AI adds perspective, not decision-making
- Always returns HTTP 200, never fails
- Works offline if cache available
- Demonstrates layered resilience

### Decision 8: Streamlit Frontend (Not REST-only)
**Choice:** Built interactive dashboard w/ Streamlit, not just API
**Why:**
- Shows system in action, not just engineering
- Users prefer visual feedback
- Real-time evaluation, weight adjustment
- History tracking helps users learn patterns
- Academic presentation value

---

## 🔢 Mathematical Foundations

### Score Normalization
```
score = (∑ weight_i × impact_i) / (∑ weight_i) × 10
```
Normalized to 0-100 scale, weighted by criteria importance.

### Composite Viability Score
```
base = (growth + sustainability) / 2

growth_dominant = max(0, growth - sustainability)
sustainability_dominant = max(0, sustainability - growth)

asymmetric_penalty = 0.3 × growth_dominant + 0.1 × sustainability_dominant
quadratic_penalty = 0.05 × (tension²) / 100

composite = max(base - asymmetric_penalty - quadratic_penalty, 0)
```

**Key insight:** This formula is **not symmetric**. It treats burnout (high growth, low sustainability) as 3x worse than stagnation.

### Tension Index
```
tension = |growth - sustainability|

severity:
  tension ≤ 15     → LOW
  tension ≤ 30     → MODERATE
  tension ≤ 60     → HIGH
  tension > 60     → CRITICAL
```

### Sensitivity Range (%)
```
variation = max(weight_variance, impact_variance) from ±20% weight & ±15% impact perturbations

stability:
  variation < 8%   → STABLE              (robust to parameter changes)
  variation 8-20%  → MODERATELY_STABLE   (some critical factors, acceptable)
  variation >= 20% → FRAGILE             (highly dependent on assumptions)
```

---

## 📌 Assumptions Made

### 1. **User-Defined Weights Are Rational**
- Assumption: Users can meaningfully assign importance weights
- Treatment: Validate weights sum >0, normalize, but don't question rationale
- Risk: Garbage in = garbage out (mitigated by sensitivity analysis showing critical criteria)

### 2. **Criteria Scores Are Comparable (After Normalization)**
- **Assumption**: After normalization, scores from different criteria dimensions are structurally comparable and can be arithmetically combined
- **Rationale**: Both growth and sustainability criteria go through identical `normalize_score()` function:
  - Formula: `(∑ weight_i × impact_i) / (∑ weight_i) × 10` 
  - Both scaled to 0-100 range
  - Weighted by user-specified importance
- **Semantic caveat**: A 70 in "growth" and 70 in "sustainability" use the same numerical scale but represent different concepts
- **Mitigation**: 
  - Sensitivity analysis tests robustness to ±20% weight changes, revealing if one dimension dominates
  - `breakdown` field shows which dimension is more fragile ("weights less reliable" vs. "impacts less reliable")
  - Users assign weights explicitly, accounting for domain-specific value differences
  - Tension index (|growth - sustainability|) makes imbalances transparent
- **Remaining risk**: Domain-specific criteria may have inherently different variance ranges (e.g., "salary" may naturally vary 10-90, while "culture fit" varies 30-70), but this is mitigated by user-defined weights encoding their preferences

### 3. **Options Are Stable (Not Changing)**
- Assumption: Option characteristics don't change mid-evaluation
- Treatment: Evaluate at point-in-time
- Risk: Real-world options evolve (mitigated by sensitivity analysis showing fragility)

### 4. **Burnout Risk > Stagnation Risk**
- Assumption: Growth-dominant imbalance is worse for human welfare than sustainability-dominant
- Treatment: 3x penalty asymmetry
- Justification: Burnout leads to health crises; stagnation allows recovery
- Caveat: True for most use cases, but not all (caveat in output)

### 5. **8-Point Margin Is "Clear Winner" Threshold**
- Assumption: >8 points difference is meaningful, ≤8 is ambiguous
- Treatment: Hardcoded, with adjustment for stability
- Risk: Domain-dependent (mitigated by dynamic adjustment based on stability)
- Rationale: Chose 8 as ~10% of typical score range (0-100)

### 6. **Single Evaluation Is Independent**
- Assumption: Evaluating option X doesn't affect evaluation of option Y
- Treatment: Each option evaluated in isolation, then compared
- Risk: Interactive effects ignored (acceptable for initial system)

### 7. **User Makes Final Decision**
- Assumption: System recommends, user decides
- Treatment: Never auto-decide, always provide explanation
- Principle: Transparency, not automation

---

## 🚨 Edge Cases & How They're Handled

### Edge Case 1: Single Option
**Scenario:** User provides only 1 option to evaluate
**Handling:**
```
decision_status = "SINGLE_OPTION_CLASSIFIED"
→ Fully evaluate the option (score, zone, risk, stability)
→ No comparison ranking (nothing to compare)
→ Result: "Here's what you're looking at" not "This is best"
```

### Edge Case 2: All Options Are Poor Fit
**Scenario:** All options score <40 viability
**Handling:**
```
decision_status = "ALL_OPTIONS_POOR_FIT"
→ Recommend best-of-worst
→ Trigger: "None of these are viable. Consider reframing."
→ Suggest: "What criteria are too strict? What options exist outside this set?"
```

### Edge Case 3: Close Competition (Tied Top Options)
**Scenario:** Top 2 options within ≤8 points
**Handling:**
```
decision_status = "CLOSE_COMPETITION"
→ Stability: Show how sensitive this is (STABLE/MODERATELY_STABLE/FRAGILE?)
→ Advice: "Neither is clearly better. Consider soft factors."
→ Trigger: "This is a genuinely difficult choice."
```

### Edge Case 4: Zero Weights on Criteria
**Scenario:** User marks criteria weight = 0
**Handling:**
```
validation → reject: "At least one criterion must have weight > 0"
User must fix: Either assign weight or remove criterion
Prevents: Undefined scores
```

### Edge Case 5: FRAGILE Decision (High Sensitivity Variance)
**Scenario:** Sensitivity analysis shows ≥20% variance across perturbations
**Handling:**
```
stability_level = "FRAGILE"
→ Threshold adjusted from ±5 to ±12 points for "clear winner"
→ Trigger: "This decision is fragile. Check critical factors."
→ Advice: Show which criteria cause variance
```

### Edge Case 6: Extreme Imbalance (Tension > 60)
**Scenario:** Option has growth=90, sustainability=20 (tension=70)
**Handling:**
```
tension_severity = "CRITICAL"
zone = "TIME_BOX" (high growth, low sustainability)
risk_level = "SEVERE_BURNOUT_RISK"
composite_score ≈ 25-30 (despite high growth)
→ Output: "Avoid this pattern. Unsustainable."
```

### Edge Case 7: Gemini API Quota Exhausted
**Scenario:** User calls /decision/reflect and daily quota hit
**Handling:**
```
Layer 1: Check cache    → if hit, return cached
Layer 2: Check limit    → if exhausted, skip API
Layer 3: Skip Gemini    (quota exceeded)
Layer 4: Fallback       → Return hardcoded ABSOLEM_FALLBACK_WISDOM
Result: HTTP 200 with wisdom from Layer 4
User: Sees complete response, no awareness of quota
```

### Edge Case 8: Floating-Point Precision
**Scenario:** Weights don't sum to exactly 1.0 (due to rounding), or FP arithmetic causes cumulative errors
**Handling:**
```
total_weight = sum(weights)
if total_weight == 0:
    return 0 (avoid division by zero)
else:
    weighted_avg = (sum(weight×impact)) / total_weight
    normalized_score = round(weighted_avg × 10, 2)
Result: Robust FP handling via rounding to 2 decimal places
```
**Why this works:**
- Exact equality check (`== 0`) catches zero-division edge case
- Rounding to 2 decimals prevents FP cumulation errors (e.g., 0.1 + 0.2 ≠ 0.3 in binary FP)
- All scores normalized to 2-decimal precision ensures consistent arithmetic

---

## 🚀 How to Run the Project

### Prerequisites
- Python 3.9+
- pip or poetry
- (Optional) Gemini API key for AI wisdom layer

### Installation

1. **Clone or extract the project**
```bash
cd Burnout_proof_system
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment (optional, for AI wisdom)**
```bash
# Create .env file in root directory
echo GOOGLE_GEMINI_API_KEY=your_key_here > .env
```

### Running the System

#### Option A: FastAPI Backend Only
```bash
python -m uvicorn app.main:app --reload
# API available at: http://localhost:8000
# Docs at: http://localhost:8000/docs
```

#### Option B: Streamlit Frontend (Recommended)
```bash
streamlit run frontend/app.py
# Opens interactive dashboard at: http://localhost:8501
```

#### Option C: Both Backend & Frontend
```bash
# Terminal 1
python -m uvicorn app.main:app --reload

streamlit run frontend/app.py
```

---

## 📁 Project Structure

```
Burnout_proof_system/
├── README.md                          # You are here
├── requirements.txt                   # Dependencies
├── .env.example                       # Environment template
│
├── app/
│   ├── __init__.py
│   ├── main.py                        # FastAPI application
│   ├── config.py                      # Configuration
│   ├── schemas.py                     # Pydantic models
│   │
│   └── engine/                        # Core decision logic (100% AI-Free)
│       ├── __init__.py
│       ├── evaluator.py               # Score normalization, composite scoring
│       ├── classifier.py              # Zone classification, risk assessment
│       ├── triggers.py                # Contextual warning messages
│       ├── sensitivity.py             # Weight perturbation analysis
│       ├── comparator.py              # Multi-option ranking, close competition detection
│       ├── ai_reflector.py            # Optional AI wisdom with 4-layer fallback
│       └── __pycache__/
│
├── frontend/
│   ├── __init__.py
│   ├── app.py                         # Streamlit interactive dashboard
│   └── .streamlit/
│       └── config.toml                # Streamlit configuration
│
└── tests/
    ├── test_engine_logic.py           # Core evaluation tests
    ├── test_api.py                    # API endpoint tests
    ├── test_edge_cases.py             # Edge case validation
    ├── test_validation.py             # Input validation tests
    ├── test_ai_reflection.py          # AI layer tests
    └── __pycache__/
```

---

## 🚀 Future Improvements

### Short-term (1-2 weeks)
1. **User Behavior Pattern Recognition**
   - Track decision history
   - Identify user-specific patterns ("Always overweights growth")
   - Provide personalized nudges ("You tend to underestimate sustainability")
   - Machine learning: Predict which decisions will satisfy user

2. **Expanded Test Coverage**
   - Currently at ~70% coverage
   - Target: 90%+ coverage with integration tests
   - Add stress tests for large option sets (100+)

### Medium-term 
3. **AI-Assisted Decision Extraction**
   - User gives title: "Should I take this job offer?"
   - AI extracts likely criteria and scores
   - Deterministic engine evaluates, AI provides context
   - Keeps core logic AI-free, augments input

4. **Mental Health Awareness**
   - Sentiment analysis on decision context
   - Detect burnout signals in option descriptions
   - Nudge: "This sounds rushed. Sleep on it?"
   - Integration: Decision history vs. user stress levels

6. **Collaboration Mode**
   - Multiple users evaluate same options
   - Compare weight distributions
   - Consensus scoring (if groups align)
   - See where team disagrees



---

## 💻 Technical Stack

| Layer | Technology | Reason |
|-------|-----------|--------|
| **Backend API** | FastAPI | Async, automatic OpenAPI docs, type hints |
| **Core Logic** | Pure Python | Deterministic, testable, fast |
| **Frontend** | Streamlit | Rapid prototyping, real-time updates |
| **Validation** | Pydantic | Type safety, automatic validation |
| **AI (Optional)** | Google Gemini API | Multi-tier fallback, cost-effective |
| **Caching** | JSON file | Simple, no external dependency |
| **Testing** | pytest | Standard, comprehensive assertions |
| **Formatting** | Black/isort | Code consistency |
| **Type Checking** | Pylance (VS Code) | Static analysis without overhead |

---

## 📝 Key Takeaways

### What This System Does Well
✅ **Explainability**: Every output is justified and traceable
✅ **Determinism**: Reproducible, reliable, auditable
✅ **Modularity**: Each component is testable and replaceable
✅ **Resilience**: Works with or without AI layer
✅ **Nuance**: Recognizes trade-offs, not just optimization
✅ **Adaptability**: Weights, thresholds, and logic are configurable
✅ **Human-Centric**: Designed for decision quality, not automation

### What It Doesn't Do (By Design)
❌ **Automate decisions**: Always recommends, never decides
❌ **Handle uncertainty perfectly**: Sensitivity analysis shows limits
❌ **Learn from feedback**: (Planned future feature)
❌ **Replace judgment**: Supports judgment, complements it
❌ **Work perfectly for all domains**: Template-able, not universal

### The Philosophy
> *"A decision system should not be a black box that optimizes for recommendation confidence. It should be a transparent mirror that helps users see their own priorities, understand trade-offs, and make decisions they can live with."*

This system embodies that philosophy: **Explicit > Implicit, Transparent > Clever, Balanced > Optimized, Supported > Automated.**

---


**Version:** 1.0.0  
**Last Updated:** March 2, 2026  

