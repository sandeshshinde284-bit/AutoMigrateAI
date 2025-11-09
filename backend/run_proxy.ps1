# ============================================
# RUN SMART PROXY ROUTER
# ============================================

Write-Host "🔀 Starting Smart Proxy Router (Port 8000)..." -ForegroundColor Magenta
Write-Host "📡 Controls Migration: 0% → 100%" -ForegroundColor Yellow
Write-Host ""

# Activate venv
.\venv\Scripts\Activate.ps1

# Go to backend
cd backend

# Start proxy
python proxy.py

# To stop: Press Ctrl+C