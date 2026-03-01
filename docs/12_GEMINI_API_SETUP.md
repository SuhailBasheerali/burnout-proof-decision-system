# Gemini API Setup Guide for Absolem AI Reflective Layer

This guide provides step-by-step instructions to enable the Gemini API for the ABSOLEM AI reflective wisdom layer in the Burnout Proof System.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step-by-Step Setup](#step-by-step-setup)
3. [Where to Store API Key](#where-to-store-api-key)
4. [Verify Installation](#verify-installation)
5. [Troubleshooting](#troubleshooting)
6. [Understanding the Integration](#understanding-the-integration)

---

## Prerequisites

- Active Google account (free tier available)
- Internet connection
- Project already has: `google-generativeai==0.8.6` package installed

### Check if Gemini Package is Installed

Run in terminal:
```powershell
pip list | findstr google-generativeai
```

Expected output: `google-generativeai       0.8.6`

If not installed, run:
```powershell
pip install google-generativeai==0.8.6
```

---

## Step-by-Step Setup

### STEP 1: Get Gemini API Key from Google

1. **Go to Google AI Studio**
   - Open browser: https://aistudio.google.com/
   - Sign in with your Google account (create one if needed)

2. **Create/Access API Key**
   - Click **"Get API key"** button (top-left or in main panel)
   - Click **"Create new secret key"**
   - A dialog will appear with your new API key
   - **COPY the entire key** (it looks like: `AIzaSyD...xB8`)

3. **Save temporary copy**
   - Paste in temporary notepad/text editor
   - **DO NOT share or commit this key to git**

### STEP 2: Store API Key in `.env` File

The system expects the API key in a `.env` file at the **project root**.

#### Create `.env` File

1. **Navigate to project root:**
   ```
   c:\Users\HP\OneDrive\Desktop\coding\Burnout_proof_system\
   ```

2. **Create `.env` file** (if doesn't exist)
   - Right-click in folder → New → Text Document
   - Name it: `.env` (with just the dot, no extension)

3. **Add API Key to `.env`**
   ```
   GOOGLE_GEMINI_API_KEY=YOUR_API_KEY_HERE
   ```
   
   **Example:**
   ```
   GOOGLE_GEMINI_API_KEY=AIzaSyD_xB8a5nK9vL2mO4pQ6rT8uV1wX2yZ3
   ```

4. **Save file** (Ctrl+S)

#### Verify `.env` File Location

Your file structure should look like:
```
Burnout_proof_system/
├── .env                          ✅ API KEY HERE
├── .gitignore                    (already configured)
├── app/
├── frontend/
├── tests/
├── docs/
├── requirements.txt
└── README.md
```

---

## Where to Store API Key

### ✅ DO Store Here:

**`.env` file** (root directory)
```
GOOGLE_GEMINI_API_KEY=YOUR_KEY
```

### ❌ DO NOT Store Here:

- ❌ `app/config.py` - Could be accidentally committed
- ❌ `requirements.txt` - Tracked in git
- ❌ Source code files - Security risk
- ❌ `.streamlit/config.toml` - Checked in git
- ❌ Comments or documentation files

### Why `.env` is Safe?

- `.env` is already in `.gitignore` (see [.gitignore](.gitignore))
- Won't be committed to git repository
- Each developer has their own local copy
- Environment-specific settings stay private

#### Verify in `.gitignore`:

Open `.gitignore` and confirm:
```
.env
```

If NOT present, add it:
```
.env
```

---

## Verify Installation

### Test 1: Check Environment Variable

Run in terminal (PowerShell):
```powershell
$env:GOOGLE_GEMINI_API_KEY
```

Expected: Your API key displayed (or blank if not set)

### Test 2: Run Backend and Check Logs

```powershell
# Activate venv
& .\venv\Scripts\Activate.ps1

# Run backend
python -m uvicorn app.main:app --reload
```

**Check console for:**
```
✨ Gemini API initialized successfully
```

If you see:
```
📖 Using Absolem's Default Wisdom (no API configured)
```

→ API key not found, check Step 2

### Test 3: Call `/stats` Endpoint

Once backend is running:

1. Open browser: `http://localhost:8000/docs`
2. Find `/stats` endpoint
3. Click "Try it out" → Execute
4. Check response for stats (should show `total_calls: 0` initially)

---

## Understanding the Integration

### How the System Uses Gemini API

#### Location: `app/engine/ai_reflector.py`

**Key Points:**

1. **Initialization** (Lines 45-57)
   ```python
   self.api_key = api_key or os.getenv("GOOGLE_GEMINI_API_KEY")
   genai.configure(api_key=self.api_key)
   self.model = genai.GenerativeModel("gemini-1.5-flash")
   ```

2. **What It Does:**
   - Gets API key from `GOOGLE_GEMINI_API_KEY` environment variable
   - Initializes Gemini 1.5 Flash model
   - Generates cryptic yet helpful advice (Absolem character)

3. **Fallback Mechanism** (Lines 199-212)
   - If API fails: uses default wisdom (no crash)
   - If no API key: uses fallback wisdom
   - Error logged but app continues

4. **Caching** (Lines 65-94)
   - Responses cached in `.ai_cache/` directory
   - **Already in `.gitignore`** (auto-generated, not committed)
   - Reduces API calls for same options
   - Cache expires after 24 hours

5. **Safety Features:**
   - Max 200 tokens per response (cost-efficient)
   - Temperature 0.7 (balanced creativity)
   - Harmful content filtering enabled

### API Endpoint in Backend

**File:** `app/main.py` (Lines 167-197)

**Endpoint:** `POST /decision/reflect`

**Called by:** Frontend when user clicks "Get Absolem's Wisdom"

**Input:**
```json
{
  "options": [{"title": "Option A"}, {"title": "Option B"}],
  "comparison_result": {"recommended_option": "Option A"}
}
```

**Output:**
```json
{
  "advice": "Absolem's cryptic wisdom advice...",
  "action_plan": ["Action 1", "Action 2", "Action 3"],
  "comparison_insight": "Why sustainable path matters...",
  "source": "Absolem (via Gemini)" or "Absolem's Default Wisdom"
}
```

### Frontend Integration

**File:** `frontend/app.py` (Lines 208-235)

**Function:** `call_reflection()`

**When Called:** User clicks "✨ Get Absolem's Wisdom" button in Phase 3

**Flow:**
1. Frontend collects selected options and results
2. Sends POST to backend `/decision/reflect`
3. Displays response with special "Absolem" styling
4. Handles errors gracefully with fallback message

---

## Troubleshooting

### Issue 1: "Using Absolem's Default Wisdom (no API configured)"

**Cause:** API key not found in environment

**Solution:**
1. Check `.env` file exists in project root
2. Verify format: `GOOGLE_GEMINI_API_KEY=YOUR_KEY` (no spaces)
3. Restart backend (must reload env variables)
4. Check API key isn't expired (went inactive on Google AI Studio)

### Issue 2: "Gemini API initialization failed"

**Cause:** Invalid API key format or Google AI Studio issue

**Solution:**
1. Go to https://aistudio.google.com/
2. Check if API key still valid (sometimes keys become inactive)
3. Create a NEW API key
4. Update `.env` file
5. Restart backend

### Issue 3: "Rate limit exceeded" or "Quota exceeded"

**Cause:** Exceeded free tier limits (1500 requests/day)

**Solution:**
1. Check `/stats` endpoint to see usage
2. Clear `.ai_cache/` folder (optional, to reset cache)
3. Wait 24 hours for quota reset
4. Or upgrade to paid Google Cloud plan

### Issue 4: API key visible in logs

**Cause:** Accidentally logging API key

**Solution:**
1. Search codebase for `GOOGLE_GEMINI_API_KEY` prints
2. Logs shouldn't show actual key (only initialization status)
3. Check git history if committed accidentally → rotate key immediately

### Issue 5: frontend showing different window layout for Absolem section

**Cause:** Streamlit cache or CSS issue

**Solution:**
- Clear browser cache: Ctrl+Shift+Delete
- Restart Streamlit: `streamlit run app.py`
- Check console (F12) for CSS errors

---

## Optional: Environment Management

### Using Python-Dotenv (Recommended)

If you want automatic loading:

1. **Install:**
   ```powershell
   pip install python-dotenv
   ```

2. **Add to `app/config.py`** (at top):
   ```python
   from dotenv import load_dotenv
   import os
   
   load_dotenv()  # Load .env file automatically
   ```

3. **But already set up!**
   The system uses `os.getenv()` which Python respects

### Alternative: Set Environment Variable Directly (Windows)

Instead of `.env` file:

```powershell
$env:GOOGLE_GEMINI_API_KEY = "YOUR_API_KEY"
```

⚠️ **Note:** This expires when terminal closes. `.env` is better.

---

## Security Checklist

- ✅ `.env` is in `.gitignore`
- ✅ API key not in any source files
- ✅ API key not in documentation
- ✅ Cache directory (`.ai_cache/`) is in `.gitignore`
- ✅ Fallback system works if API key missing
- ✅ Error messages don't expose API key
- ✅ Each developer keeps own `.env` file

---

## Useful Links

- **Google AI Studio:** https://aistudio.google.com/
- **Gemini API Docs:** https://ai.google.dev/gemini-api/docs/
- **Free Tier Limits:** 1500 requests/day, 50K tokens/minute
- **Pricing:** https://ai.google.dev/pricing

---

## Next Steps

1. Create `.env` file with API key
2. Restart backend
3. Open frontend and test
4. Click "Get Absolem's Wisdom" to verify

Once working, you should see:
- ✨ "Absolem (via Gemini)" in source
- 🧠 Cryptic advice tailored to your decision
- 📋 Action plan for burnout prevention
- 💡 Comparative insight

---

## Support

If issues persist:

1. Check backend logs for error messages
2. Verify API key format (no extra spaces)
3. Test at https://aistudio.google.com/ that key works
4. Check Google Cloud quota limits
5. Review Gemini API documentation for model availability

