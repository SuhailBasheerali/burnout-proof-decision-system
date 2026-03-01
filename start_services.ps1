# Start Backend and Frontend Services
# This script runs both services in parallel for easy testing

Write-Host "🚀 Starting Academic Decision Analyzer..." -ForegroundColor Cyan
Write-Host "🔧 System Check..." -ForegroundColor Yellow

# Check if venv is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "⚠️  Virtual environment not detected. Activating..." -ForegroundColor Yellow
    & "./venv/Scripts/Activate.ps1"
}

# Check if required packages are installed
Write-Host "📦 Checking dependencies..." -ForegroundColor Yellow
$pythonPath = if ($env:VIRTUAL_ENV) { "$env:VIRTUAL_ENV\Scripts\python.exe" } else { "python" }
& $pythonPath -m pip install -q streamlit plotly pandas requests fastapi uvicorn pydantic pytest httpx 2>$null

Write-Host ""
Write-Host "✅ Ready to start services!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 OPTION 1: Start Both Services" -ForegroundColor Cyan
Write-Host "   Command: ./start_both.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "📋 OPTION 2: Start Individual Services" -ForegroundColor Cyan
Write-Host ""
Write-Host "   Backend (Terminal 1):" -ForegroundColor Yellow
Write-Host "   python -m uvicorn app.main:app --reload" -ForegroundColor Gray
Write-Host ""
Write-Host "   Frontend (Terminal 2):" -ForegroundColor Yellow
Write-Host "   streamlit run frontend/app.py" -ForegroundColor Gray
Write-Host ""
Write-Host "🌐 Access the Application:" -ForegroundColor Cyan
Write-Host "   Frontend: http://localhost:8501" -ForegroundColor Green
Write-Host "   Backend:  http://localhost:8000" -ForegroundColor Green
Write-Host ""
Write-Host "💡 Tips:" -ForegroundColor Cyan
Write-Host "   - Keep both terminals open" -ForegroundColor Gray
Write-Host "   - Use Ctrl+C to stop services" -ForegroundColor Gray
Write-Host "   - Check STARTUP_GUIDE.md for more options" -ForegroundColor Gray
Write-Host ""
