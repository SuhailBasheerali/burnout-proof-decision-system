# 🚀 Academic Stress Management Decision System - Streamlit Frontend

A modern, responsive web application for helping students make balanced academic decisions considering both growth and wellbeing.

## 📋 Features

- **Phase 1: Decision Entry** - Define your decision topic and number of options
- **Phase 2: Option Input** - Rate 4 key metrics for each option:
  - 📊 **Productivity**: Time/effort required (0-10)
  - ⚡ **Impact**: Academic/career benefit (0-10)
  - 💪 **Importance**: How important for your goals (0-10)
  - ✅ **Feasibility**: Can you realistically do it (0-10)

- **Phase 3: Analysis Dashboard** - Get:
  - 🥇 Ranked recommendations
  - 📊 Detailed score breakdowns
  - 📈 Visual comparisons (radar & bar charts)
  - 💡 Risk assessments & insights
  - 🎯 Decision zones & guidance

## 🛠️ Installation

### Prerequisites
- Python 3.9+
- Virtual environment (venv)

### Setup

1. **Activate virtual environment:**
   ```bash
   # Windows
   venv\Scripts\Activate.ps1
   
   # Mac/Linux
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Running the Application

### Terminal 1: Start the Backend
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
Uvicorn running on http://0.0.0.0:8000
Press CTRL+C to quit
```

### Terminal 2: Start the Streamlit Frontend
```bash
streamlit run streamlit_app.py
```

You should see:
```
  You can now view your Streamlit app in your browser.
  
  Local URL: http://localhost:8501
  Network URL: http://xxx.xxx.x.xx:8501
```

## 🎯 How to Use

### Step 1: Enter Your Decision
1. Navigate to http://localhost:8501
2. Enter your decision topic (e.g., "Course Selection for Next Semester")
3. Select the number of options you want to compare (1-5)
4. Click "Next: Enter Options"

### Step 2: Rate Your Options
For each option, provide:
- **Productivity** (0-10): How much work is needed? (0=no effort, 10=extreme)
- **Impact** (0-10): Academic/career benefit? (0=none, 10=game-changer)
- **Importance** (0-10): How important for your goals? (0=not needed, 10=critical)
- **Feasibility** (0-10): Can you realistically do it? (0=impossible, 1=very feasible)

### Step 3: Review Results
The system analyzes all options and provides:
- **Ranked recommendations** (best to worst)
- **Growth Score** (0-100): Academic advancement potential
- **Sustainability Score** (0-100): Wellbeing & feasibility
- **Tension Index**: Gap between growth and sustainability
- **Risk Level**: Burnout risk assessment
- **Decision Zone**: EXECUTE, CAUTION, or REEVALUATE

## 📊 Understanding the Results

### Composite Score
Your main decision metric (0-100). Higher is better, but balance matters more than raw numbers.

**Formula:** 
```
Base = (Growth + Sustainability) / 2
Penalty = 0.3 × (Growth - Sustainability) if imbalanced
Adjusted = Base - Penalty
```

### Tension Index
The gap between growth and sustainability scores.
- **0-15**: LOW - Well-balanced
- **16-30**: MODERATE - Fair balance
- **31-60**: HIGH - Significant imbalance
- **60+**: EXTREME - Critical gap

### Decision Zones
- 🟢 **EXECUTE**: Growth and sustainability aligned - go with confidence!
- 🟡 **CAUTION**: High growth but sustainability risks - needs strategy
- 🔵 **STEADY**: Balanced moderate scores - safe choice
- 🔴 **REEVALUATE**: High growth drive in unsustainable situation - reconsider

### Risk Levels
- ✅ **LOW**: Unlikely to cause burnout
- ⚠️ **MODERATE**: Watch for stress signals
- 🔴 **HIGH**: Significant burnout risk
- 🔴 **SEVERE**: Immediate action needed

## 🎨 UI/UX Design

### Modern Features
- ✨ Responsive gradient design
- 📱 Mobile-friendly layout
- 🎨 Color-coded metrics & zones
- 📊 Interactive charts (Plotly)
- 🎯 Intuitive 3-phase workflow
- 💾 Session state management

### Responsive Breakpoints
- Works on desktop, tablet, and mobile
- Adaptive column layouts
- Touch-friendly controls

## 🔌 API Integration

The frontend communicates with the backend via:

**Endpoint:** `POST http://localhost:8000/decision/compare`

**Request Body:**
```json
{
  "options": [
    {
      "title": "Option Name",
      "growth_criteria": [
        {
          "weight": 6.0,
          "impact": 8
        }
      ],
      "sustainability_criteria": [
        {
          "weight": 8.0,
          "impact": 9
        }
      ]
    }
  ]
}
```

**Response:** Ranked evaluations with detailed metrics

## 📈 Example Decision Flow

**Scenario:** Student choosing between 3 options

1. **Entry Phase:**
   - Decision: "Course Selection for Next Semester"
   - Options: 3

2. **Input Phase:**
   - Option 1: "Focus on Current Classes + Internship"
     - Productivity: 6/10, Impact: 8/10
     - Importance: 8/10, Feasibility: 9/10
   
   - Option 2: "Advanced ML Course"
     - Productivity: 8/10, Impact: 9/10
     - Importance: 8/10, Feasibility: 2/10
   
   - Option 3: "Research Project"
     - Productivity: 9/10, Impact: 9/10
     - Importance: 9/10, Feasibility: 1/10

3. **Results:**
   - 🥇 **Rank 1:** Focus on Current + Internship (Composite: 78.5)
   - 🥈 **Rank 2:** Advanced ML Course (Composite: 68.2)
   - 🥉 **Rank 3:** Research Project (Composite: 61.8)

## 🐛 Troubleshooting

### Backend Connection Error
- Ensure backend is running: `python -m uvicorn app.main:app --reload`
- Check port 8000 is available
- Verify firewall settings

### Streamlit Not Found
```bash
pip install streamlit
```

### Missing Dependencies
```bash
pip install -r requirements.txt
```

### Port Already in Use
Change port in startup command:
```bash
streamlit run streamlit_app.py --server.port 8502
```

## 📝 Configuration

### Backend URL
Edit in `streamlit_app.py`:
```python
BACKEND_URL = "http://localhost:8000"
```

### Streamlit Config
Create `~/.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#f8f9fa"
secondaryBackgroundColor = "#ffffff"
textColor = "#262730"
```

## 📚 Project Structure

```
Burnout_proof_system/
├── streamlit_app.py          # Frontend application
├── app/
│   ├── main.py               # Backend API
│   ├── schemas.py            # Data models
│   └── engine/               # Decision logic
├── tests/                    # Test suite
├── docs/                     # Documentation
└── requirements.txt          # Dependencies
```

## 🚀 Deployment

### Local Development
```bash
# Terminal 1
python -m uvicorn app.main:app --reload

# Terminal 2
streamlit run streamlit_app.py
```

### Production (Example with Heroku)
```bash
# Create Procfile
echo "web: streamlit run streamlit_app.py" > Procfile
echo "backend: python -m uvicorn app.main:app --host 0.0.0.0" >> Procfile

heroku create
git push heroku main
```

## 📖 Documentation

- [API Documentation](docs/01_API_DOCUMENTATION.md)
- [User Guide](docs/02_USER_GUIDE.md)
- [System Architecture](docs/03_SYSTEM_ARCHITECTURE.md)

## 🎓 Educational Purpose

This system helps students make decisions that balance:
- 🚀 **Ambition** - Academic growth and career advancement
- 😌 **Wellbeing** - Mental health, sleep, relationships, sustainability

The goal: **Achieve your goals WITHOUT burning out.**

## 📧 Support

For issues or questions:
1. Check the troubleshooting section
2. Review backend logs
3. Enable debug mode in Streamlit:
   ```bash
   streamlit run streamlit_app.py --logger.level=debug
   ```

## ✅ Testing

Run backend tests:
```bash
python -m pytest tests/ -v
```

## 🎉 Ready to Make Better Decisions!

Your path to balanced academic success starts here. Good luck! 🌟
