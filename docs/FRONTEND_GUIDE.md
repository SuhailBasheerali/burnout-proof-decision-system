# 🎓 Academic Stress Management Decision System - Frontend Guide

## Overview

A **modern, responsive Streamlit web application** that helps students make balanced academic decisions by analyzing the trade-off between growth (ambition) and sustainability (wellbeing).

---

## 🎯 System Architecture

### 3-Tier Architecture

```
┌─────────────────────────────────────────────────────────┐
│  FRONTEND (Streamlit)                                   │
│  Port: 8501                                             │
│  - Modern UI with gradients & animations               │
│  - Responsive design (desktop/tablet/mobile)           │
│  - 3-phase workflow                                     │
│  - Real-time visualizations                            │
└─────────────────────────────────────────────────────────┘
                            ↓
                    HTTP REST API
                            ↓
┌─────────────────────────────────────────────────────────┐
│  BACKEND (FastAPI)                                      │
│  Port: 8000                                             │
│  - Decision analysis engine                             │
│  - Score normalization                                 │
│  - Risk assessment & classification                     │
│  - Sensitivity analysis                                 │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  DECISION ENGINE (Python)                               │
│  - Composite scoring algorithm                          │
│  - Burnout detection                                    │
│  - Zone classification                                 │
│  - Trigger messages                                     │
└─────────────────────────────────────────────────────────┘
```

---

## 📱 UI Phases & Workflow

### Phase 1: Decision Entry
```
┌──────────────────────────────────────────┐
│ 📚 Academic Decision Analyzer             │
│ Balancing Ambition with Student Wellbeing│
├──────────────────────────────────────────┤
│                                          │
│ What are you deciding?                   │
│ [________________] (text input)          │
│                                          │
│ How many options?                        │
│ [2] [3] [4] ... [10]                    │
│                                          │
│ [🚀 NEXT: ENTER OPTIONS →]              │
│                                          │
└──────────────────────────────────────────┘
```

**User Input:**
- Decision topic (text)
- Number of options (dropdown: 1-5)

**Features:**
- Clean, inviting design
- Clear explanation of what happens next
- One-click navigation

---

### Phase 2: Option Input
```
┌────────────────────────────────────────────────────────┐
│ 📋 COMPARING 3 OPTIONS                                 │
├────────────────────────────────────────────────────────┤
│                                                         │
│ OPTION 1: [Focus on Current Classes + Internship]    │
│ OPTION 2: [Take Advanced ML Course]                  │
│ OPTION 3: [Lead Research Project]                    │
│                                                         │
│ ┌──────────────────────────────────────────────────┐  │
│ │ 🚀 GROWTH CRITERIA                               │  │
│ │ 📊 Productivity: [●═══════════] 6/10             │  │
│ │ ⚡ Impact:       [═════════●══] 8/10             │  │
│ │                                                   │  │
│ │ 😌 SUSTAINABILITY CRITERIA                       │  │
│ │ 💪 Importance:   [═════════●══] 8/10             │  │
│ │ ✅ Feasibility:  [═════════●══] 9/10             │  │
│ │                                                   │  │
│ │ ┌─────────────────────────────────────────────┐ │  │
│ │ │ Growth Score: 6.0/10 │ Sust: 7.2/10 │Gap: 1.2│ │  │
│ │ └─────────────────────────────────────────────┘ │  │
│ └──────────────────────────────────────────────────┘  │
│                                                         │
│ [← BACK]  [ANALYZE & COMPARE →]                      │
│                                                         │
└────────────────────────────────────────────────────────┘
```

**For Each Option:**
- Title (text input)
- 4 metrics (sliders, 0-10 scale)

**Metrics:**
```
Growth Criteria:
├─ 📊 Productivity (0-10): How much work is needed?
└─ ⚡ Impact (0-10): How much academic/career benefit?

Sustainability Criteria:
├─ 💪 Importance (0-10): How important for your goals?
└─ ✅ Feasibility (0-10): Can you realistically do it?
```

**Real-time Feedback:**
- Live score calculation
- Balance gap indicator
- Color-coded feedback

---

### Phase 3: Analysis Results Dashboard

#### 3.1 Recommendation Card
```
┌────────────────────────────────────────────────────────┐
│ 🥇 RECOMMENDED: Focus on Current + Internship         │
│                                                         │
│ Composite Score: 78.5/100                              │
│ Decision Status: 🟢 CLEAR WINNER                       │
│ Risk Level: LOW                                         │
│                                    Zone: EXECUTE 🟢     │
└────────────────────────────────────────────────────────┘
```

#### 3.2 Ranking Table
```
│ Rank │ Option                  │ Growth │ Sust. │ Risk│Score│
├──────┼─────────────────────────┼────────┼───────┼─────┼─────┤
│ 🥇  │ Focus on Current...     │ 72/100 │85/100 │LOW  │78.5 │
│ 🥈  │ Advanced ML Course      │ 85/100 │42/100 │MOD  │68.2 │
│ 🥉  │ Lead Research Project   │ 88/100 │35/100 │HIGH │61.8 │
```

#### 3.3 Visual Metrics (for each option)
```
┌─────────────────────────────────────────────────────────┐
│ GAUGE CHARTS (3 columns)                                │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ Growth Score (72)  │ Sustainability (85)  │ Tension (13)│
│ ════════════════   │ ═══════════════════  │ ═══════    │
│ [0        50  100] │ [0        50  100] │[0   50 100]│
│                                                          │
└─────────────────────────────────────────────────────────┘
```

#### 3.4 Detailed Cards (tabbed interface)
```
Per Option Tabs:
├─ Zone ANALYSIS
│  ├─ Classification (EXECUTE)
│  ├─ Zone Reason (Well-balanced...)
│  ├─ Tension Severity (MILD)
│  └─ Risk Level (LOW)
│
├─ STABILITY ANALYSIS
│  ├─ Sensitivity Range (±5%)
│  ├─ Stability Level (Very Stable)
│  └─ Composite Score (78.5/100)
│
└─ TRIGGERED INSIGHTS
   ├─ 💡 Insight 1
   ├─ 💡 Insight 2
   └─ 💡 Insight 3
```

#### 3.5 Visual Comparisons
```
Left: Radar Chart          │ Right: Bar Chart
                           │
  Growth                   │ 100 ┌─────────────────┐
   ╱╲                      │     │   Growth (blue) │
  ╱  ╲ Sustainability      │  75 │   Sust (green)  │
 Sust  ╲      ╱Balance     │  50 │   Comp (purple) │
  ╲  ╱    ╳      ╱Safety   │  25 │                 │
   ╲╱    ╱  ╲  ╱           │   0 └─────────────────┘
        ╱    ╲╱            │   Opt1  Opt2   Opt3
```

---

## 🎨 Design Features

### Color Scheme
```
Primary: Purple (#667eea) - Academic/Growth
Secondary: Teal (#10b981) - Sustainability/Wellbeing
Warning: Amber (#f59e0b) - Caution/Tension
Danger: Red (#ef4444) - High Risk
```

### Icons & Visual Language
```
🚀 Growth/Career
😌 Wellbeing/Sustainability
⚡ Impact/Intensity
💪 Importance
✅ Feasibility/Success
🎯 Goal-oriented
⚠️ Risk/Warning
🔴 High Alert
🟡 Caution
🟢 Good to Go
```

### Responsive Layout
```
Desktop (1200px+):
┌─────────────────────────────────────┐
│    ✨ Full-width layout             │
│    ✨ 3-column grids for metrics    │
│    ✨ Side-by-side comparisons      │
└─────────────────────────────────────┘

Tablet (768px-1199px):
┌──────────────────┐
│  2-column layout │
│  Optimized grids │
│  Full readability│
└──────────────────┘

Mobile (< 768px):
┌──────┐
│Stack │
│layout│
│100%w │
└──────┘
```

---

## 📊 Scoring Algorithm (Displayed)

### Growth Score Calculation
```
Growth = (Productivity × Impact) / 10 × 10
       = (6 × 8) / 100 = 0.48
       Normalized to 0-100 scale = 72/100
```

### Sustainability Score Calculation
```
Sustainability = (Importance × Feasibility) / 10 × 10
               = (8 × 9) / 100 = 0.72
               Normalized to 0-100 scale = 85/100
```

### Composite Viability Score
```
Base Score = (Growth + Sustainability) / 2
           = (72 + 85) / 2 = 78.5

Imbalance Penalty:
  If Growth > Sustainability:
    Penalty = 0.3 × (72 - 42) = 9
  
Final = 78.5 - imbalance_penalty
      = ~78.5 (in this case, well-balanced)
```

### Tension Index
```
Tension = |Growth - Sustainability|
        = |72 - 85| = 13

Severity:
  0-15:  LOW (✅ Well-balanced)
  16-30: MODERATE (⚠️ Fair balance)
  31-60: HIGH (🔴 Significant gap)
  60+:   EXTREME (🔴🔴 Critical)
```

---

## 🔄 State Management

### Session State Variables
```python
st.session_state = {
    "current_phase": 1,              # Which phase (1-3)
    "decision_topic": "...",         # User's decision
    "num_options": 3,                # Number of options
    "options_data": {                # Per-option metrics
        0: {
            "title": "...",
            "productivity": 6.0,
            "impact": 8,
            "importance": 8.0,
            "feasibility": 9
        },
        ...
    },
    "analysis_results": {            # Backend results
        "evaluations": [...],
        "recommended_option": "...",
        "decision_status": "..."
    }
}
```

### Phase Transitions
```
Phase 1 (Entry)
     ↓ [NEXT button]
Phase 2 (Input)
     ├─ [BACK button] → Phase 1
     └─ [ANALYZE button] → Phase 3
Phase 3 (Results)
     ├─ [BACK button] → Phase 2
     └─ [NEW DECISION button] → Phase 1 (reset)
```

---

## 🔌 API Integration

### Request Payload
```json
{
  "options": [
    {
      "title": "Focus on Current + Internship",
      "growth_criteria": [
        {
          "weight": 6.0,    # Productivity
          "impact": 8       # Impact
        }
      ],
      "sustainability_criteria": [
        {
          "weight": 8.0,    # Importance
          "impact": 9       # Feasibility
        }
      ]
    }
    ...
  ]
}
```

### Response Payload
```json
{
  "evaluations": [
    {
      "title": "Focus on Current + Internship",
      "growth_score": 72.0,
      "sustainability_score": 85.0,
      "tension_index": 13.0,
      "tension_severity": "LOW",
      "zone": "EXECUTE_FULLY",
      "zone_reason": "High growth and sustainable",
      "composite_score": 78.5,
      "risk_level": "LOW",
      "triggered_messages": [
        "Option is well-balanced",
        "Strong feasibility"
      ],
      "sensitivity_range": 5.0,
      "stability_level": "Very Stable"
    }
    ...
  ],
  "recommended_option": "Focus on Current + Internship",
  "decision_status": "CLEAR_WINNER",
  "recommendation_reason": "..."
}
```

---

## 🚀 Features Implemented

### User Experience
- ✅ Multi-step wizard interface
- ✅ Real-time input validation
- ✅ Live score calculation feedback
- ✅ Responsive design
- ✅ Intuitive slider controls
- ✅ Tab-based organization
- ✅ Status indicators (emojis)

### Visualizations
- ✅ Gauge charts (Plotly)
- ✅ Radar comparison chart
- ✅ Bar chart comparisons
- ✅ Ranking tables
- ✅ Color-coded zones
- ✅ Status badges

### Data Management
- ✅ Session state persistence
- ✅ Form validation
- ✅ Error handling
- ✅ Backend connectivity check
- ✅ User-friendly error messages

### Design
- ✅ Modern gradient backgrounds
- ✅ Smooth transitions
- ✅ Consistent color scheme
- ✅ Professional typography
- ✅ Accessible contrast ratios
- ✅ Spacing & alignment

---

## 📋 Running & Testing

### Start Both Services
```bash
# Terminal 1: Backend
python -m uvicorn app.main:app --reload

# Terminal 2: Frontend
streamlit run streamlit_app.py
```

### Testing Workflow
```
1. Open http://localhost:8501
2. Enter topic: "Course Decision"
3. Select 2 options
4. Rate Option 1: P=5, I=7, Imp=6, F=8
5. Rate Option 2: P=8, I=9, Imp=8, F=3
6. Click "Analyze"
7. See recommendations
8. Explore tabs & visualizations
```

---

## 🎯 User Journey Example

```
┌─────────────────────────────────────────────────────┐
│ USER JOURNEY: Choosing Between 2 Courses            │
└─────────────────────────────────────────────────────┘

START
  ↓
[Phase 1] Enter decision topic
  "Should I take Advanced Python or Web Dev?"
  Number of options: 2
  ↓
[Phase 2] Rate Option 1 - "Advanced Python"
  Productivity: 8/10 (very demanding)
  Impact: 9/10 (great for career)
  Importance: 8/10 (crucial skill)
  Feasibility: 2/10 (major conflict with work)
  
  Calculated Scores:
  - Growth: 72/100
  - Sustainability: 20/100
  - Tension: 52 (EXTREME)
  - Composite: ~25/100
  ↓
[Phase 2] Rate Option 2 - "Web Dev"
  Productivity: 6/10 (manageable)
  Impact: 7/10 (good for portfolio)
  Importance: 7/10 (relevant skill)
  Feasibility: 8/10 (fits schedule)
  
  Calculated Scores:
  - Growth: 52/100
  - Sustainability: 70/100
  - Tension: 18 (MODERATE)
  - Composite: ~66/100
  ↓
[Phase 2] Click "Analyze & Compare"
  ↓
[Phase 3] See Results
  🥇 RECOMMENDED: Web Dev (66/100)
  🥈 Option 2: Advanced Python (25/100)
  
  Reason: Web Dev is SUSTAINABLE
  Advanced Python risks BURNOUT
  ↓
[Phase 3] User explores detailed breakdown
  - Sees Python has extreme tension gap
  - Sees Web Dev is well-balanced
  - Reads triggered insights
  - Checks sensitivity/stability
  ↓
[Phase 3] User makes informed decision
  ✅ Choose Web Dev this semester
  📌 Consider Python after graduation when schedule is flexible
  ↓
END
```

---

## 🎓 Educational Value

This system teaches students:

1. **Trade-off Thinking**
   - Not all choices are growth opportunities
   - Sustainability matters as much as ambition

2. **Metrics Awareness**
   - How to quantify abstract concepts
   - Why both effort AND benefit matter

3. **Risk Assessment**
   - Recognizing burnout patterns early
   - Making data-driven academic decisions

4. **Balance Philosophy**
   - Success = Growth + Wellbeing
   - Short-term gain ≠ long-term success

---

## 🔐 Frontend Security

- ✅ Input validation on all forms
- ✅ Slider constraints (0-10 ranges)
- ✅ Backend connection timeout (10s)
- ✅ Error boundary handling
- ✅ Session state reset
- ✅ No sensitive data in logs

---

## 📱 Responsive Testing

```bash
# Desktop view
streamlit run streamlit_app.py --client.showErrorDetails=true

# Mobile view (DevTools)
Press F12 → Toggle Device Toolbar → iPhone/Android

# Tablet view
Set viewport to 768px width
```

---

## 🎉 Summary

This Streamlit frontend provides:
- 📚 **Intuitive 3-phase workflow**
- 🎨 **Modern, responsive design**
- 📊 **Rich visualizations**
- 🔄 **Seamless API integration**
- ✅ **Student-friendly language**
- 💡 **Data-driven decision support**

Perfect for helping students **balance ambition with wellbeing**! 🌟
