# Setup & Deployment Guide: Burnout-Proof Decision System

## Table of Contents
1. [Quick Start](#quick-start)
2. [Prerequisites](#prerequisites)
3. [Local Development Setup](#local-development-setup)
4. [Running Tests](#running-tests)
5. [Development Workflow](#development-workflow)
6. [Production Deployment](#production-deployment)
7. [Docker Deployment](#docker-deployment)
8. [Troubleshooting](#troubleshooting)

---

## Quick Start

### 30-Second Setup (Experienced Developers)

```bash
# Clone and navigate
git clone <repo-url>
cd Burnout_proof_system

# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run development server
python -m uvicorn app.main:app --reload --port 8000

# API available at http://localhost:8000
# API docs at http://localhost:8000/docs
```

### 5-Minute Setup (First Time)

Follow [Local Development Setup](#local-development-setup) section below.

---

## Prerequisites

### Required

- **Python**: 3.10 or higher (recommend 3.13)
- **pip**: Latest version
- **Git**: For version control
- **Terminal/PowerShell**: For commands

### Recommended

- **Poetry** or **pip-tools**: For dependency management
- **IDE**: VS Code, PyCharm, or similar
- **Git GUI**: (Optional) For non-CLI git operations

### System Requirements

- **RAM**: 2GB minimum
- **Disk**: 500MB free
- **Network**: For pip package downloads
- **OS**: Windows, macOS, or Linux

---

## Local Development Setup

### Step 1: Clone Repository

```bash
# HTTPS (recommended if no SSH key)
git clone https://github.com/yourusername/Burnout_proof_system.git
cd Burnout_proof_system

# Or SSH (if SSH key configured)
git clone git@github.com:yourusername/Burnout_proof_system.git
cd Burnout_proof_system
```

### Step 2: Create Virtual Environment

**Why virtual environment?**
Isolates project dependencies from system Python. Prevents version conflicts.

**Windows (PowerShell)**:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
```

**Verify activation**:
```bash
# Should show (venv) prefix in terminal
python --version  # Should show 3.10+
```

### Step 3: Install Dependencies

```bash
# Upgrade pip (recommended)
pip install --upgrade pip

# Install from requirements.txt
pip install -r requirements.txt
```

**What gets installed**:
```
- fastapi==latest          # Web framework
- uvicorn==latest          # ASGI server
- pydantic==latest         # Data validation
- pytest==latest           # Testing framework
- pytest-cov==latest       # Coverage tracking
```

**Verify installation**:
```bash
pip list  # Should show all packages
python -c "import fastapi; print(fastapi.__version__)"
```

### Step 4: Start Development Server

```bash
# Navigate to project root
cd Burnout_proof_system

# Start server with auto-reload
python -m uvicorn app.main:app --reload --port 8000

# Output should show:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# INFO:     Application startup complete
```

**Verify server is running**:
```bash
# In another terminal
curl http://localhost:8000/health  # Should return 200 OK
```

### Step 5: Access API Documentation

Open browser to:
```
http://localhost:8000/docs        # Interactive Swagger UI
http://localhost:8000/redoc       # ReDoc documentation
```

---

## Running Tests

### Run All Tests

```bash
pytest

# Output example:
# test_validation.py ...                                [12%]
# test_engine_logic.py .......                          [42%]
# test_api.py ............                              [100%]
# 25 passed in 1.23s ✓
```

### Run Specific Test File

```bash
pytest tests/test_api.py          # API endpoint tests
pytest tests/test_engine_logic.py # Core engine tests
pytest tests/test_validation.py   # Schema validation tests
```

### Run Specific Test Function

```bash
pytest tests/test_api.py::test_balanced_growth_option
pytest tests/test_engine_logic.py::test_composite_score_calculation
```

### Run with Coverage Report

```bash
pytest --cov=app --cov-report=html

# Opens coverage report in htmlcov/index.html
# Shows which lines are tested
```

### Run with Verbose Output

```bash
pytest -v                # Verbose: shows each test
pytest -v -s             # Even more verbose, print statements shown
pytest --tb=short        # Shorter error messages
```

### Run in Watch Mode (Optional)

```bash
pip install pytest-watch
ptw                      # Auto-reruns tests on file changes
```

---

## Development Workflow

### Common Development Tasks

#### Adding a New Feature

1. **Create feature branch**:
   ```bash
   git checkout -b feature/new-feature-name
   ```

2. **Make changes**:
   ```bash
   # Edit files in app/
   # Example: app/engine/classifier.py
   ```

3. **Write tests** (TDD recommended):
   ```bash
   # Add tests in tests/
   # Run tests: pytest
   ```

4. **Run local server**:
   ```bash
   # In terminal 1
   python -m uvicorn app.main:app --reload --port 8000
   
   # In terminal 2
   curl -X POST http://localhost:8000/decision/compare \
     -H "Content-Type: application/json" \
     -d '{"options": [...]}'
   ```

5. **Commit changes**:
   ```bash
   git add app/
   git commit -m "Add new feature: description"
   ```

#### Debugging

**Print debugging**:
```python
# In app/engine/evaluator.py
def composite_score(growth, sustainability):
    print(f"DEBUG: growth={growth}, sustainability={sustainability}")
    # ... rest of code
```

**Using Python debugger**:
```python
# In your code
import pdb
pdb.set_trace()  # Execution stops here

# In terminal during test
(Pdb) p growth  # Print variable
(Pdb) c          # Continue
```

**Using IDE debugger**:
```
VS Code: Install Python extension, set breakpoint, run with debugger
PyCharm: Built-in debugger, graphical breakpoint interface
```

#### Modifying Test Scenarios

Test scenarios are in `tests/test_api.py`:

```python
def test_your_scenario():
    payload = {
        'options': [
            {
                'title': 'Your Option',
                'growth_criteria': [
                    {'weight': 7, 'impact': 8}
                ],
                'sustainability_criteria': [
                    {'weight': 7, 'impact': 8}
                ]
            }
        ]
    }
    
    response = client.post('/decision/compare', json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data['decision_status'] == 'SINGLE_OPTION_CLASSIFIED'
    # ... more assertions
```

#### Adjusting System Parameters

**Composite score penalty ratio**:
```python
# In app/engine/evaluator.py
asymmetric_penalty = (0.3 * growth_dominant) + (0.1 * sustainability_dominant)
#                     ↑                         ↑
#                     Change these ratios to adjust burnout weighting
```

**Sensitivity perturbation**:
```python
# In app/engine/sensitivity.py
multiplier = 1.2  # ±20% perturbation
#            ↑
#            Change to 1.1 for ±10%, 1.3 for ±30%, etc.
```

**Stability thresholds**:
```python
# In app/engine/sensitivity.py
STABLE_THRESHOLD = 8  # < 8 = STABLE
MODERATELY_STABLE_THRESHOLD = 20  # 8-20 = MODERATELY_STABLE
# > 20 = FRAGILE
```

---

## Production Deployment

### Pre-Deployment Checklist

```bash
# ✓ All tests passing
pytest

# ✓ No security vulnerabilities
pip check

# ✓ Code is formatted
# (Optional: black app/ tests/)

# ✓ All changes committed
git status  # Should be clean

# ✓ No secrets in code
grep -r "password\|API_KEY\|secret" app/
```

### Deployment Option 1: Heroku (Easiest)

**Setup** (first time):
```bash
# Install Heroku CLI
# Login
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set ENVIRONMENT=production
```

**Deploy**:
```bash
git push heroku main  # Automatically deploys from git
heroku open           # Opens your deployed app
heroku logs -t        # Stream logs
```

### Deployment Option 2: AWS EC2

**Setup** (first time):
```bash
# Launch EC2 instance (Ubuntu 22.04)
# Security group: inbound on ports 80, 443, 22

# SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Install dependencies
sudo apt update && sudo apt install python3-pip python3-venv

# Clone repo
git clone <repo-url>
cd Burnout_proof_system

# Create environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
pip install gunicorn
```

**Run with Gunicorn** (production server):
```bash
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

**Setup systemd service** (auto-restart):
```bash
sudo nano /etc/systemd/system/burnout-api.service
```

Copy:
```ini
[Unit]
Description=Burnout-Proof Decision API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/Burnout_proof_system
Environment="PATH=/home/ubuntu/Burnout_proof_system/venv/bin"
ExecStart=/home/ubuntu/Burnout_proof_system/venv/bin/gunicorn app.main:app --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable burnout-api
sudo systemctl start burnout-api
sudo systemctl status burnout-api
```

### Deployment Option 3: DigitalOcean

**Similar to AWS**, but simpler interface:
1. Create Droplet (Ubuntu 22.04, 2GB RAM minimum)
2. Follow AWS EC2 steps above
3. Use built-in DNS pointing

---

## Docker Deployment

### Build Docker Image

**Create `Dockerfile`** (already in root):
```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ app/

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Build image**:
```bash
docker build -t burnout-api:latest .
```

**Run container locally**:
```bash
docker run -p 8000:8000 burnout-api:latest
# API available at http://localhost:8000
```

### Push to Docker Registry

**Docker Hub**:
```bash
# Login
docker login

# Tag image
docker tag burnout-api:latest yourusername/burnout-api:latest

# Push
docker push yourusername/burnout-api:latest
```

**Use in production**:
```bash
docker run -d -p 80:8000 yourusername/burnout-api:latest
```

### Docker Compose (Multiple Services)

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
```

**Run**:
```bash
docker-compose up -d    # Start in background
docker-compose logs -f  # Stream logs
docker-compose down     # Stop
```

---

## Environment Variables

### Development
```bash
# .env (create in project root, don't commit)
ENVIRONMENT=development
LOG_LEVEL=DEBUG
```

### Production
```bash
ENVIRONMENT=production
LOG_LEVEL=INFO
WORKERS=4
```

### Using Environment Variables

```python
# In app/main.py
import os

environment = os.getenv('ENVIRONMENT', 'development')
workers = int(os.getenv('WORKERS', 1))
```

---

## Monitoring & Logging

### View Server Logs

**Development**:
```bash
# Just look at terminal where uvicorn is running
# Shows all requests automatically
```

**Production (Gunicorn)**:
```bash
# Tail logs
tail -f /var/log/gunicorn.log

# Or using systemd
journalctl -u burnout-api -f
```

**Production (Docker)**:
```bash
docker logs -f <container-id>
```

### Health Check

```bash
# Check if API is responding
curl http://localhost:8000/health

# Response: 
# {"status": "healthy"}
```

### Performance Monitoring

```bash
# Install monitoring tool
pip install prometheus-client

# Or use application performance monitoring:
# - New Relic
# - Datadog
# - CloudWatch (AWS)
```

---

## Scaling

### Horizontal Scaling (Multiple Instances)

**Option 1: Load Balancer + Multiple Instances**
```
         ┌─ API Instance 1 (port 8001)
         ├─ API Instance 2 (port 8002)
Nginx ->─┼─ API Instance 3 (port 8003)
         ├─ API Instance 4 (port 8004)
         └─ API Instance 5 (port 8005)
```

**Nginx Config Example**:
```nginx
upstream api {
    server localhost:8001;
    server localhost:8002;
    server localhost:8003;
}

server {
    listen 80;
    location / {
        proxy_pass http://api;
    }
}
```

**Option 2: Kubernetes**
```bash
# Deploy to Kubernetes cluster
kubectl apply -f deployment.yaml
kubectl scale deployment burnout-api --replicas=5
```

### Vertical Scaling (Bigger Servers)

Usually not needed for this application, but if needed:
- Increase server RAM
- Upgrade CPU
- Use SSD storage

---

## Troubleshooting

### Virtual Environment Issues

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
# Verify you're in the venv
which python  # Should show venv path

# Reinstall dependencies
pip install -r requirements.txt

# Verify
python -c "import fastapi; print('OK')"
```

### Port Already in Use

**Problem**: `Address already in use`

**Solution**:
```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux

# Kill process
kill -9 <PID>

# Or use different port
python -m uvicorn app.main:app --reload --port 8001
```

### Tests Failing

**Problem**: `FAILED test_api.py::test_balanced_growth_option`

**Solution**:
```bash
# Run with verbose output
pytest -v -s tests/test_api.py

# Check for recent code changes
git status

# Rollback if needed
git checkout app/engine/evaluator.py

# Run tests again
pytest
```

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'app'`

**Solution**:
```bash
# Verify you're in project root
pwd  # Should show .../Burnout_proof_system

# Verify structure
ls app/  # Should show __init__.py, main.py, etc.

# Reinstall in development mode
pip install -e .
```

### Database/Persistence Questions

**This application doesn't use a database** (yet). All processing is stateless.

If you need to add persistence:
```python
# Option 1: SQLite (simple)
pip install sqlalchemy

# Option 2: PostgreSQL (production)
pip install psycopg2-binary sqlalchemy
```

---

## Maintenance

### Regular Tasks

**Weekly**:
```bash
# Run tests
pytest

# Check for updates
pip list --outdated
```

**Monthly**:
```bash
# Update dependencies (carefully)
pip install -U -r requirements.txt
pytest  # Verify nothing broke

# Check security
pip check
```

**Quarterly**:
```bash
# Major version updates (if needed)
# Example: FastAPI 0.x → 1.x
pip install --upgrade fastapi
# Thoroughly test before deploying

# Review and update documentation
# Check GitHub issues/PRs
```

### Backup Strategy

```bash
# Backup configuration
cp .env .env.backup

# Backup deployment scripts
git push  # Ensure code is committed

# Backup database (if added later)
# pg_dump database_name > backup.sql
```

---

## Support & Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Uvicorn Docs**: https://www.uvicorn.org/
- **Pytest Docs**: https://docs.pytest.org/
- **GitHub Issues**: Report bugs in repository

---

## Upgrade Path

### From Development to Production

1. ✅ All tests passing locally
2. ✅ No hardcoded secrets in code
3. ✅ Environment variables set up
4. ✅ Logging configured
5. ✅ Health check endpoint working
6. ✅ Error handling robust
7. ✅ Documentation updated
8. ✅ Deploy to staging first
9. ✅ Run smoke tests in staging
10. ✅ Deploy to production
11. ✅ Monitor in production

