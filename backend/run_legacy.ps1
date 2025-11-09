# ============================================
# RUN LEGACY SYSTEM
# ============================================

Write-Host "🚀 Starting Legacy System (Port 5000)..." -ForegroundColor Cyan
Write-Host "⏱️  Response Time: 2-3 seconds (OLD SYSTEM)" -ForegroundColor Yellow
Write-Host ""

# Activate venv
.\venv\Scripts\Activate.ps1

# Go to backend
cd backend

# Start legacy system
python legacy_system.py

# To stop: Press Ctrl+C