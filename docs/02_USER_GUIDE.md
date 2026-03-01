# User Guide: Burnout-Proof Decision System

## Table of Contents
1. [Getting Started](#getting-started)
2. [Core Concepts](#core-concepts)
3. [How to Use](#how-to-use)
4. [Understanding Results](#understanding-results)
5. [Decision Scenarios](#decision-scenarios)
6. [Tips & Best Practices](#tips--best-practices)

---

## Getting Started

### What is This System?
The Burnout-Proof Decision System helps you make strategic decisions that balance **growth** (progress toward goals) with **sustainability** (maintainability and team health). It identifies burnout risks and recommends whether to "go full steam," time-box the effort, or recover first.

### Who Should Use It?
- 🏢 Business leaders evaluating new initiatives
- 👥 Team managers deciding on project scope
- 🎯 Product managers prioritizing features
- 📊 Entrepreneurs planning growth strategies
- 💼 Individuals managing career decisions

### The Problem It Solves
Many organizations chase growth at the cost of sustainability, leading to:
- Team burnout
- Quality degradation
- High turnover
- Reduced long-term viability

This system **prevents that** by making burnout risks explicit in every decision.

---

## Core Concepts

### Growth vs. Sustainability

#### Growth (forward progress)
What drives the organization forward?
- Revenue increase
- Market expansion
- Feature development
- Team capability growth
- Strategic positioning

**Score Range**: 0-100
- 0-30: Minimal progress
- 30-70: Moderate progress
- 70-100: Strong momentum

#### Sustainability (ability to maintain)
What enables long-term execution?
- Team health & capacity
- Process maturity
- Technical debt management
- Resource availability
- Work-life balance

**Score Range**: 0-100
- 0-30: Unsustainable (burnout risk)
- 30-70: Moderately sustainable
- 70-100: Highly sustainable (healthy pace)

### The Tension Index
Shows the imbalance between growth and sustainability.

```
Tension = |Growth Score - Sustainability Score|
```

| Tension | Type | Meaning |
|---------|------|---------|
| 0-15 | LOW | Well-balanced decision |
| 15-30 | MODERATE | Some trade-offs present |
| 30-60 | HIGH | Significant imbalance |
| 60-100 | CRITICAL | Severe imbalance, burnout trap |

### Zones: Where You Are

| Zone | G Score | S Score | Situation | Action |
|------|---------|---------|-----------|--------|
| **EXECUTE_FULLY** | ≥70 | ≥70 | Health & growth | 🚀 Full speed |
| **TIME_BOX** | ≥70 | <50 | Growth push | ⏱️ Limited sprint |
| **LIGHT_RECOVERY** | <50 | ≥70 | Rebuilding | 🔄 Stabilize |
| **STEADY_EXECUTION** | Both moderate | Balance | Sustainable | ⏸️ Maintain pace |
| **AVOID** | <40 | <40 | Weak option | ❌ Reject/redesign |

### Risk Levels: What Could Go Wrong

| Risk Level | Condition | Action |
|-----------|-----------|--------|
| **STRUCTURALLY_STABLE** | Balanced scores | ✅ Proceed with confidence |
| **SEVERE_BURNOUT_RISK** | High G, low S | ⚠️ Time-box and recover |
| **SUSTAINABILITY_DEFICIT** | S score very low | 🔧 Invest in capacity |
| **GROWTH_STAGNATION_RISK** | G score very low | 📈 Increase ambition |
| **LOW_STRUCTURAL_VALUE** | Both scores low | ❌ Redesign required |

### Stability: How Robust Is It?

Measures how sensitive the decision is to changes in criteria weights.

| Level | Sensitivity Variance | Robustness | Action |
|-------|----------------------|-----------|--------|
| **STABLE** | <8 | Very robust | Trust the decision |
| **MODERATELY_STABLE** | 8-20 | Fairly robust | Proceed, monitor key metrics |
| **FRAGILE** | >20 | Low robustness | Verify assumptions; reduce risk |

---

## How to Use

### Step 1: Identify Your Criteria

Choose **growth criteria** that represent forward progress:
```
Examples:
- "Revenue growth: 40%"
- "Launch 3 new products"
- "Add 50 customers"
- "Expand to new market"
```

Choose **sustainability criteria** that represent stability:
```
Examples:
- "Maintain team happiness score >7/10"
- "Keep unplanned overtime <5 hours/week"
- "Reduce technical debt by 20%"
- "Increase process efficiency"
```

### Step 2: Assign Weights (Importance)

How important is each criterion? (0-10 scale)

```
Weight Scale:
0-2:   Not important (nice-to-have)
3-5:   Moderately important (should consider)
6-8:   Very important (key metric)
9-10:  Critical (must achieve)
```

**Example**:
```
Growth Criteria:
- "Revenue growth 40%" → weight: 8 (very important)
- "Market expansion" → weight: 6 (important)

Sustainability Criteria:
- "Team health" → weight: 9 (critical)
- "Technical debt reduction" → weight: 5 (moderately important)
```

### Step 3: Estimate Impact (0-10)

If we execute this option, how much will we achieve each criterion?

```
Impact Scale:
0-2:   Minimal outcome
3-5:   Moderate outcome
6-8:   Strong outcome
9-10:  Exceptional outcome
```

**Example**:
```
Revenue Growth (weight: 8):
- Option A can achieve: impact 9 (expected 40% growth)
- Option B can achieve: impact 6 (expected 25% growth)
```

### Step 4: Submit to System

Send your options to the API:
```
Option Title: "Aggressive Q2 Expansion"
Growth Criteria:
  - weight: 8, impact: 9 (revenue growth)
  - weight: 7, impact: 8 (market expansion)
Sustainability Criteria:
  - weight: 9, impact: 3 (team health)
  - weight: 6, impact: 4 (technical debt)
```

### Step 5: Interpret Results

See the decision status and follow the recommended action.

---

## Understanding Results

### Single Option (Viability Assessment)

You submitted 1 option → System answers: **"Is this a good idea?"**

**Decision Status**: `SINGLE_OPTION_CLASSIFIED`

**Output**:
```
✅ EXECUTE_FULLY
Growth: 75/100 | Sustainability: 75/100 | Score: 75/100
Risk: STRUCTURALLY_STABLE | Stability: STABLE
→ Proceed with confidence
```

### Multiple Options (Comparison)

You submitted 2-10 options → System answers: **"Which option should we choose?"**

**Decision Status**: One of:
- `CLEAR_WINNER` — One option is significantly better
- `CLOSE_COMPETITION` — Multiple options are competitive
- `ALL_OPTIONS_POOR_FIT` — None of the options are good; redesign needed

**Output** (example):
```
🏆 CLEAR_WINNER: "Balanced Growth Strategy"

Ranking:
1. Balanced Growth Strategy        Score: 68/100
2. Aggressive Expansion           Score: 54/100  ⚠️ Burnout trap
3. Conservative Growth            Score: 38/100

Winner wins because it balances growth and sustainability,
while others have burnout risks or insufficient momentum.
```

### Reading the Scores

**Composite Score = Pure viability**
- If growth=80, sustainability=60 → raw average=70
- If imbalanced, system penalizes asymmetrically:
  - Growth-dominant penalty: 0.3 × imbalance
  - Sustainability-dominant penalty: 0.1 × imbalance
- This makes burnout (high G, low S) 3x worse than stagnation

---

## Decision Scenarios

### Scenario 1: Career Promotion

**Question**: "Should I accept this promotion given my current workload?"

**Setup**:
```
Growth Criteria:
- "Title elevation & prestige" → weight: 7, estimated impact: 9
- "Salary increase (20%)" → weight: 8, estimated impact: 9
- "Learning opportunities" → weight: 6, estimated impact: 8

Sustainability Criteria:
- "Time commitment (<50 hours/week)" → weight: 9, estimated impact: 2
- "Work-life balance" → weight: 8, estimated impact: 3
- "Team support for transition" → weight: 7, estimated impact: 4
```

**Expected Result**: TIME_BOX zone, SEVERE_BURNOUT_RISK
- Composite Score: ~45-50/100
- Recommendation: "Accept, but time-box: Set 6-month intensive push, then delegate to rebuild sustainability"

---

### Scenario 2: Startup Scale

**Question**: "Should we do a Series B raise and aggressive hiring?"

**Setup**:
```
Growth Criteria:
- "Revenue increase to $10M ARR" → weight: 9, impact: 9
- "Team growth 30→100 people" → weight: 8, impact: 9
- "Market leadership positioning" → weight: 7, impact: 8

Sustainability Criteria:
- "Maintain culture & values" → weight: 8, impact: 3
- "Operational excellence" → weight: 7, impact: 2
- "Technical architecture scalability" → weight: 9, impact: 4
```

**Expected Result**: TIME_BOX zone, possible SEVERE_BURNOUT_RISK
- Recommendation: "Yes, but with explicit recovery phases and culture investments"

---

### Scenario 3: Recovery Phase

**Question**: "Should we stop growth initiatives and focus on consolidation?"

**Setup**:
```
Growth Criteria:
- "New feature launches" → weight: 3, impact: 2
- "Market share growth" → weight: 2, impact: 1

Sustainability Criteria:
- "Team mental health recovery" → weight: 10, impact: 9
- "Technical debt elimination" → weight: 9, impact: 8
- "Process standardization" → weight: 8, impact: 7
```

**Expected Result**: LIGHT_RECOVERY zone, STRUCTURALLY_STABLE
- Recommendation: "Yes, this is healthy. Consolidate, rebuild, prepare for next push"

---

## Tips & Best Practices

### ✅ DO

1. **Be realistic with impacts**
   - Don't rate everything as 9-10
   - Consider what's actually achievable
   - Account for execution risk

2. **Include sustainability criteria**
   - Too many initiatives ignore this
   - Team health, technical debt, process maturity
   - Long-term thinking

3. **Weight by true importance**
   - Don't just put 8-9 on everything
   - Distinguish what's critical vs. nice-to-have
   - Align with organizational values

4. **Use for pattern awareness**
   - Most options high-growth, low-sustainability?
   - That's a cultural problem to address
   - System helps identify systemic issues

5. **Complement with judgment**
   - System provides structure, not the final answer
   - Company culture, external market, team morale matter
   - Use system output to inform, not dictate

### ❌ DON'T

1. **Over-specify criteria**
   - 2-4 criteria per dimension is ideal
   - More makes scoring difficult
   - Keep it simple and focused

2. **Use identical weights**
   - If all are 7, you're not differentiating
   - Force yourself to rank what matters most

3. **Rate everything in the "high" range**
   - "Impact: 9" everywhere is unrealistic
   - Creates false confidence
   - Be honest about constraints

4. **Ignore sustainability signals**
   - Red flags: sustainability score <40
   - Green flags: both scores >60
   - Yellow flags: tension index >40

5. **Treat one-option evaluation as final approval**
   - EXECUTE_FULLY still needs execution risk review
   - System assesses viability, not implementation details

### 🎯 Decision Framework

```
After system evaluation:

COMPOSITE SCORE > 70 + STABLE
  → Execute with confidence
  → Minimal risk monitoring needed

COMPOSITE SCORE 50-70 + MODERATELY_STABLE
  → Proceed with caution
  → Establish monitoring and rollback plan

COMPOSITE SCORE < 50 OR FRAGILE
  → High risk, recommend redesign
  → If proceeding: clear contingency plan required
```

### 📊 Interpreting Tension

**Balanced (tension <15)**:
```
Growth=75, Sustainability=80 → Tension=5 ✅
Execution style: Normal pace, sustainable long-term
```

**Growth-focused (tension > sustainability)**:
```
Growth=85, Sustainability=50 → Tension=35 ⚠️
Execution style: Sprint-recovery cycles
```

**Recovery-focused (sustainability > growth)**:
```
Growth=40, Sustainability=80 → Tension=40 ⚠️
Execution style: Build capacity for future momentum
```

---

## Common Questions

### Q: What's a "good" composite score?

**A**: Context-dependent:
- 70+ for normal execution = healthy
- 50-70 for sprint phases = acceptable
- <40 = redesign recommended
- Anything + STABLE = more confident than anything + FRAGILE

### Q: Should I always choose the highest score?

**A**: Usually, but consider:
- **CLEAR_WINNER with highest score** → Choose it
- **CLOSE_COMPETITION** → Weigh non-numerical factors (culture fit, strategic positioning, team preference)
- **Multiple options with high burnout risk** → None are good; redesign is better

### Q: Can I have a TIME_BOX forever?

**A**: No. TIME_BOX assumes:
- Explicit time boundary (90 days typical)
- Recovery period after (30-60 days)
- Repeat cycle only 2-3 times before burnout
- Use for strategic pushes, not permanent state

### Q: My team votes overweight sustainability. Is that wrong?

**A**: Not wrong, it's strategic:
- Young companies: growth-weighted (build momentum)
- Mature companies: sustainability-weighted (maintain quality)
- Scaling companies: balanced (both matter)
- Post-burnout companies: sustainability-weighted (rebuild)

### Q: Can criteria be subjective?

**A**: Yes:
- "Team happiness" is subjective, but measurable (survey 1-10)
- "Culture preservation" is subjective, but important
- Weight and impact don't need to be financial metrics
- Just be consistent in your scoring

---

## Getting Help

- **API Issues**: Check [API Documentation](01_API_DOCUMENTATION.md)
- **Algorithm Details**: See [Algorithm Reference](08_ALGORITHM_REFERENCE.md)
- **Setup Instructions**: See [Setup & Deployment Guide](05_SETUP_DEPLOYMENT.md)

