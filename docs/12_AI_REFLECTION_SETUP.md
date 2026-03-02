# AI Reflection Layer - Setup & Configuration Guide

## 🦋 Overview

The **Absolem AI Reflection Layer** provides philosophical, character-themed guidance on decision-making with a focus on burnout prevention. It analyzes your options and provides wise counsel on which path sustains your wellbeing best.

### Features

✅ **Cryptic Yet Helpful Advice** - Absolem-themed wisdom  
✅ **Burnout Prevention Focus** - Sustainability analysis  
✅ **Action Plans** - Concrete steps to implement your decision  
✅ **Comparative Insights** - Why one option beats others  
✅ **Forever Free** - Uses Google Gemini's free tier (1,500 requests/day)  
✅ **Fallback Safety** - Works offline with default wisdom  
✅ **Response Caching** - Reduces API calls for same decisions  

---

## 🚀 Quick Setup

### 1. Get Your Gemini API Key (Free)

1. Go to [Google AI Studio](https://ai.google.dev)
2. Click **"Get API Key"** 
3. Click **"Create API key"** (in new project)
4. Copy your API key (looks like: `AIzaSy...`)

**No credit card needed!**

### 2. Add Your API Key

Create a `.env` file in your project root:

```bash
GOOGLE_GEMINI_API_KEY=your_api_key_here
```

Or set it as an environment variable:

**Windows (PowerShell):**
```powershell
$env:GOOGLE_GEMINI_API_KEY = "your_api_key_here"
```

**Linux/Mac:**
```bash
export GOOGLE_GEMINI_API_KEY="your_api_key_here"
```

### 3. Restart the Backend

The backend will automatically load your API key on startup:

```bash
python -m uvicorn app.main:app --reload
```

Look for this in the logs:
```
✨ Gemini API initialized successfully
```

---

## 💡 How It Works

### In the Frontend

1. Open the Academic Decision Analyzer
2. Complete Phase 1 & 2 (enter your decision and options)
3. View Phase 3 results
4. Scroll to **"Absolem's Reflective Wisdom"** section
5. Click **"✨ Get Absolem's Wisdom"**
6. Receive philosophical guidance on sustainable choice

### Behind the Scenes

```
Frontend Button Click
    ↓
POST /decision/reflect
    ↓
ai_reflector.py
    ├─ Check Cache → Return cached (fastest)
    ├─ Call Gemini API → Stream response
    ├─ Save to cache → Reuse for identical decisions
    └─ Fallback → Default wisdom if API fails
    ↓
Display in Phase 3 UI
```

---

## 🛡️ Mitigation Strategies Included

### 1. **Fallback Wisdom**
If the API fails or isn't configured, Absolem's default wisdom is served:

```
"Patience, young learner. The burden you carry is not the decision 
itself, but your resistance to choosing. Some options demand the 
soul's surrender—avoid those."
```

### 2. **Response Caching**
- Identical decisions get cached for 24 hours
- Cached folder: `.ai_cache/` in project root
- Dramatically reduces API usage
- Fallback if API is temporarily down

### 3. **Error Handling**
- Connection errors return friendly fallback
- API rate limits gracefully handled
- Timeout protection (15 seconds max)

### 4. **Usage Monitoring**
Check your API usage:

```bash
curl http://localhost:8000/stats
```

Response includes:
```json
{
  "ai_reflection_stats": {
    "total_calls": 5,
    "failed_calls": 0,
    "cached_calls": 3,
    "cache_enabled": true,
    "fallback_available": true
  }
}
```

---

## 📊 Free Tier Limits

| Metric | Limit | Your Typical Usage |
|--------|-------|-------------------|
| Requests/Day | 1,500 | ~5-20 |
| Requests/Minute | 60 | ~1-2 |
| Token Limit | ~1M/day | ~50K |
| Cost | Free | $0 |

**You'll stay well within limits for personal/student use** ✅

---

## 🔧 Advanced Configuration

### Custom Prompts

Edit `app/engine/ai_reflector.py` line ~157:

```python
def _create_prompt(self, options: list, best_option: str, analysis_data: dict) -> str:
    """Create Absolem-themed prompt."""
    options_str = ", ".join([opt["name"] for opt in options])
    return f"""Your custom prompt here..."""
```

### Change Cache Expiry

Edit line ~36:
```python
CACHE_EXPIRY_HOURS = 24  # Change this value
```

### Disable AI Feature Entirely

Don't set the environment variable. The system gracefully falls back to default wisdom.

---

## 🧪 Testing

### Test the API Directly

```bash
# Get your API status
curl http://localhost:8000/stats

# Or in PowerShell
Invoke-WebRequest -Uri http://localhost:8000/stats
```

### Test Without Frontend

Create a test file:

```python
from app.engine.ai_reflector import get_absolem_wisdom

options = [
    {
        "name": "Option A",
        "scores": {"growth": 85, "sustainability": 70}
    }
]

result = get_absolem_wisdom(options, {
    "recommendation": "Option A",
    "analysis": {"growth_score": 85, "sustainability_score": 70}
})

print(result["advice"])
```

---

## ❓ FAQ

### Q: Is it really free forever?
**A:** Yes, as long as Google maintains the free tier API (very likely). 1,500 requests/day = ∞ for student use.

### Q: What if I exceed the free tier?
**A:** The system falls back to default Absolem wisdom. No charges ever occur.

### Q: Can I use a different AI?
**A:** Yes! You can modify `ai_reflector.py` to use OpenAI, Claude, or any LLM. The wrapper pattern makes it easy.

### Q: Does it work without an API key?
**A:** Yes! It falls back gracefully to default wisdom. Perfect for offline use or privacy.

### Q: Can I cache responses?
**A:** Yes, automatic 24-hour caching is built in. Same decision = instant response.

### Q: How do I monitor usage?
**A:** Hit `/stats` endpoint or check `.ai_cache/` folder size.

---

## 🚨 Troubleshooting

### "Gemini API initialization failed"
- Check your API key is valid
- Verify it's set in environment variable
- Check `.env` file format

### "Cannot connect to backend"
- Ensure backend is running: `python -m uvicorn app.main:app --reload`
- Check port 8000 is available

### "API reflection unavailable"
- This is intentional - system has fallen back to default wisdom
- Check internet connection
- Check API usage at `/stats`

### Cache not working
- `.ai_cache/` folder must be writable
- Check disk space
- Clear cache: delete `.ai_cache/` folder

---

## 📚 Architecture

```
Frontend (Streamlit)
    ↓
    POST /decision/reflect endpoint
    ↓
ai_reflector.py (main logic)
    ├─ Cache Manager
    ├─ Prompt Engineering
    ├─ Error Handling
    └─ Gemini API Client
    ↓
Google Gemini API (Free Tier)
    ↓
Backend Response
    ↓
Frontend Display with Styled Card
```

---

## ✅ Next Steps

1. **Get API Key** - Visit [ai.google.dev](https://ai.google.dev)
2. **Set Environment Variable** - Add `GOOGLE_GEMINI_API_KEY`
3. **Restart Backend** - `python -m uvicorn app.main:app --reload`
4. **Test in Frontend** - Click "✨ Get Absolem's Wisdom" button
5. **Monitor Usage** - Check `/stats` endpoint regularly

---

**Questions?** The system gracefully handles all errors and falls back to philosophy. Enjoy Absolem's wisdom! 🦋
