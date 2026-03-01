# 🚀 Quick Start Guide - Academic Decision Analyzer

## ⚡ 2-Minute Setup

### 1. Verify Installation (One-time)
```bash
# From project root
pip install -r requirements.txt
```

### 2. Start Backend (Terminal 1)
```bash
python -m uvicorn app.main:app --reload
```
✅ You'll see: `Uvicorn running on http://0.0.0.0:8000`

### 3. Start Frontend (Terminal 2)
```bash
streamlit run streamlit_app.py
```
✅ Browser opens automatically at `http://localhost:8501`

---

## 🎯 First Decision (3 Minutes)

### Step 1: Enter Your Decision (30 seconds)
- **Topic:** "Should I take Data Science course?"
- **Options:** 2

### Step 2: Rate Option 1 (45 seconds)
```
Title: "Take Data Science"
📊 Productivity: 8/10  (2-3 exams, heavy projects)
⚡ Impact: 9/10        (crucial for AI career)
💪 Importance: 8/10   (major goal)
✅ Feasibility: 3/10  (major schedule conflict)
```

### Step 3: Rate Option 2 (45 seconds)
```
Title: "Focus on Current + Side Projects"
📊 Productivity: 5/10  (manageable workload)
⚡ Impact: 5/10        (decent portfolio building)
💪 Importance: 6/10   (helpful but not critical)
✅ Feasibility: 8/10  (fits your schedule)
```

### Step 4: Review Results (60 seconds)
- See ranking of options
- Check composite scores
- Read zone and risk assessment
- Make informed decision

---

## 📊 Understanding Your Results

### What You'll See
```
🥇 RECOMMENDED: Focus on Current + Side Projects (Score: 68/100)
   └─ Growth: 50  │  Sustainability: 80  │  Balance: ✅ Great

🥈 Take Data Science (Score: 35/100)
   └─ Growth: 90  │  Sustainability: 30  │  Balance: ❌ Risky
```

### What It Means
- **Higher Composite Score** = Better balance of growth & wellbeing
- **Green Zone** = Safe to pursue with confidence
- **Orange Zone** = Possible, but requires careful planning
- **Red Zone** = High burnout risk, reconsider

---

## 💡 Tips & Tricks

### For Honest Ratings
- **Productivity**: How much TIME will this take? (0=none, 10=all your time)
- **Impact**: What BENEFIT will you get? (0=none, 10=life-changing)
- **Importance**: Does this MATTER for your goals? (0=no, 10=critical)
- **Feasibility**: Can you REALISTICALLY do it? (0=no, 10=definitely)

### For Better Decisions
1. ✅ Consider multiple options (2-4 is ideal)
2. ✅ Be realistic about your time & energy
3. ✅ Compare similar options (e.g., all courses or all projects)
4. ✅ Look at the composite score, not just growth
5. ✅ Read the triggered insights for context

### Common Scenarios

**"I want to take the hardest class"**
- High productivity + high impact = high growth
- But check feasibility! If 1/10, risky for burnout
- Result: Orange zone (caution) - needs backup plan

**"I want a balanced semester"**
- Moderate productivity (4-6)
- Moderate impact (5-7)
- High importance (7-8) + high feasibility (7-8)
- Result: Green zone (execute!) - safe choice

**"I want to maximize growth"**
- High productivity (8-9)
- High impact (8-9)
- But watch importance/feasibility balance
- Result: Often orange/red - manage expectations

---

## 🔄 Comparing More Options

Want to compare 3+ options? No problem!

**Best Practice:**
- 2-4 options: Clear comparison
- 5+ options: Harder to decide, consider filtering first

**Workflow:**
```
Start with 5 options
↓
Use results to eliminate bottom 2
↓
Do deeper analysis on top 3
↓
Make final decision
```

---

## 🐛 Troubleshooting

### "Backend Offline" Error
```bash
# Check backend is running
python -m uvicorn app.main:app --reload

# If port 8000 is busy
python -m uvicorn app.main:app --port 8001 --reload
# Then update streamlit_app.py line ~31:
# BACKEND_URL = "http://localhost:8001"
```

### "Streamlit Not Found"
```bash
pip install streamlit
```

### "Port 8501 Already in Use"
```bash
streamlit run streamlit_app.py --server.port 8502
```

### Slow Performance
- Check your internet connection
- Restart both services
- Clear browser cache (Ctrl+Shift+Delete)

---

## 📱 Mobile Usage

The app works on phones/tablets! 

**Limitations:**
- Small sliders might be tricky to use
- Better experience on tablet or desktop
- Test on desktop first, then mobile

---

## 📊 Example Decisions

### Example 1: Student Choosing Courses
```
DECISION: "What courses to take next semester?"

OPTION 1: "Algorithms I + Machine Learning"
├─ Productivity: 8/10
├─ Impact: 9/10
├─ Importance: 8/10
└─ Feasibility: 2/10 (lectures overlap!)
Result: RED ZONE - Feasibility killer

OPTION 2: "Algorithms I + Databases"
├─ Productivity: 7/10
├─ Impact: 7/10
├─ Importance: 8/10
└─ Feasibility: 7/10
Result: GREEN ZONE - Choose this!
```

### Example 2: Student Choosing Commitments
```
DECISION: "Should I join research group?"

OPTION 1: "Join research (10 hrs/week)"
├─ Productivity: 9/10
├─ Impact: 9/10 (publication opportunity)
├─ Importance: 9/10 (grad school prep)
└─ Feasibility: 1/10 (no time with current load)
Result: RED ZONE - Postpone until next year

OPTION 2: "Tutoring job (6 hrs/week)"
├─ Productivity: 5/10
├─ Impact: 7/10 (money + resume)
├─ Importance: 6/10 (helps pay tuition)
└─ Feasibility: 8/10 (flexible hours)
Result: YELLOW ZONE - Doable with planning
```

### Example 3: Student Choosing Summer Plans
```
DECISION: "How to spend summer?"

OPTION 1: "Intensive bootcamp (full-time)"
├─ Productivity: 10/10
├─ Impact: 9/10 (job-ready skis)
├─ Importance: 8/10 (career goal)
└─ Feasibility: 5/10 (exhausting, no break)
Result: YELLOW ZONE - Good but risky for burnout

OPTION 2: "Part-time internship + projects"
├─ Productivity: 6/10
├─ Impact: 8/10 (industry experience)
├─ Importance: 8/10 (networking)
└─ Feasibility: 9/10 (sustainable pace)
Result: GREEN ZONE - Balanced approach!

OPTION 3: "Just rest & refresh"
├─ Productivity: 1/10
├─ Impact: 2/10 (no career gain)
├─ Importance: 3/10 (not a goal)
└─ Feasibility: 10/10 (easy!)
Result: MIXED - Good for wellbeing, zero growth
```

---

## 🎓 Learning the System

### First Time?
1. ✅ Go through quick example above
2. ✅ Make one simple decision with 2 options
3. ✅ Read all the explanation tabs
4. ✅ Try with 3 options next

### Getting Comfortable?
1. ✅ Use for real academic decisions
2. ✅ Compare results with your gut feeling
3. ✅ Track which recommendations you follow
4. ✅ See outcomes (did the good option work out?)

### Advanced Users?
1. ✅ Compare 4-5 complex options
2. ✅ Use sensitivity ranges to understand stability
3. ✅ Look at triggered messages for hidden insights
4. ✅ Export/save decisions for later review

---

## 🎯 Philosophy Behind the System

**Core Belief:**
> "Ambition without balance ≠ success. Success = Growth + Wellbeing"

**Why This Matters:**
- 🚀 Pure growth can lead to burnout
- 😌 Pure sustainability can lead to stagnation
- ⚖️ Balance leads to sustainable success

**What the System Does:**
1. ✅ Quantifies your options numerically
2. ✅ Identifies burnout patterns early
3. ✅ Recommends choices that work long-term
4. ✅ Explains the reasoning clearly
5. ✅ Empowers YOU to make the final decision

---

## 📞 Getting Help

### Common Questions

**Q: Why is my top growth option not recommended?**
A: Probably low feasibility or sustainability. The system prioritizes balance over raw growth scores.

**Q: Can I change my mind after deciding?**
A: Absolutely! You can run multiple analyses. Academic decisions aren't permanent.

**Q: Should I always follow the recommendation?**
A: No! Use it as a thinking tool. The recommendation is based on your ratings - trust your judgment too.

**Q: What if the scores are very close?**
A: Look at the sensitivity/stability analysis. Very close options might be equivalent choices.

---

## ✅ Checklist Before Deciding

```
☐ All options have titles
☐ All metrics rated (no blanks)
☐ Ratings feel honest to you
☐ You reviewed the detailed breakdown
☐ You checked the triggered insights
☐ You understand the zones
☐ You're ready to decide!
```

---

## 🎉 You're Ready!

```bash
# Start both services
python -m uvicorn app.main:app --reload &
streamlit run streamlit_app.py
```

Open http://localhost:8501 and **make your first balanced decision!** 

Good luck! 🌟

---

## 📚 Learn More

- 📖 [Frontend Guide](FRONTEND_GUIDE.md) - Detailed UI documentation
- 📖 [Streamlit README](STREAMLIT_README.md) - Setup & deployment
- 📖 [API Docs](docs/01_API_DOCUMENTATION.md) - Backend specification
- 📖 [System Architecture](docs/03_SYSTEM_ARCHITECTURE.md) - How it works
