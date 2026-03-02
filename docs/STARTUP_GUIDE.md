# 🚀 Run Both Services - Quick Start

This script helps you start both the backend and frontend with simple commands.

## Option 1: Use This Script (Easiest)

### Windows PowerShell
```powershell
# Make the script executable
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Run both services
.\start_services.ps1
```

### Mac/Linux Bash
```bash
chmod +x start_services.sh
./start_services.sh
```

## Option 2: Manual Start (Two Terminals)

### Terminal 1: Backend
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2: Frontend
```bash
streamlit run frontend/app.py
```

## Services will run on:
- **Backend API:** http://localhost:8000
- **Frontend App:** http://localhost:8501

## Troubleshooting

**Backend not starting?**
```bash
pip install -r requirements.txt
```

**Frontend not found?**
```bash
pip install streamlit plotly pandas requests
```

**Ports already in use?**
```bash
# Change backend port
python -m uvicorn app.main:app --port 8001

# Change frontend port
streamlit run frontend/app.py --server.port 8502
```

---

See [QUICKSTART.md](QUICKSTART.md) for more details.
