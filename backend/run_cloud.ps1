# ============================================
# RUN CLOUD SERVICE
# ============================================

Write-Host "☁️  Starting Cloud Service (Port 5001)..." -ForegroundColor Green
Write-Host "⚡ Response Time: <100ms (FAST, MODERN)" -ForegroundColor Yellow
Write-Host ""

# Activate venv
.\venv\Scripts\Activate.ps1

# Go to backend
cd backend

# Start cloud service
python -m uvicorn cloud_service:app --reload --port 5001

# To stop: Press Ctrl+C