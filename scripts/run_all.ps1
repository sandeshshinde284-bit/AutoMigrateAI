# Copy this into scripts/run_all.ps1

Write-Host "🚀 AutoMigrate AI - Starting All Services" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Get project root
$projectRoot = (Get-Item (Split-Path -Path $PSScriptRoot)).Parent.FullName

# Activate venv
Set-Location $projectRoot
.\venv\Scripts\Activate.ps1

Write-Host "Starting 3 services in separate PowerShell windows..." -ForegroundColor Yellow
Write-Host ""

# Service 1: Legacy System (5000)
Write-Host "1️⃣  Starting Legacy System (Port 5000)" -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit -Command {
    Set-Location '$projectRoot'
    `.\venv\Scripts\Activate.ps1
    cd backend
    Write-Host '🏭 LEGACY SYSTEM - PORT 5000' -ForegroundColor Cyan
    Write-Host 'Response Time: 2-3 seconds' -ForegroundColor Yellow
    python legacy_system.py
}"

Start-Sleep -Seconds 2

# Service 2: Cloud Service (5001)
Write-Host "2️⃣  Starting Cloud Service (Port 5001)" -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit -Command {
    Set-Location '$projectRoot'
    `.\venv\Scripts\Activate.ps1
    cd backend
    Write-Host '☁️  CLOUD SERVICE - PORT 5001' -ForegroundColor Green
    Write-Host 'Response Time: <100ms' -ForegroundColor Yellow
    python -m uvicorn cloud_service:app --reload --port 5001
}"

Start-Sleep -Seconds 2

# Service 3: Smart Proxy (8000)
Write-Host "3️⃣  Starting Smart Proxy (Port 8000)" -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit -Command {
    Set-Location '$projectRoot'
    `.\venv\Scripts\Activate.ps1
    cd backend
    Write-Host '🔀 SMART PROXY - PORT 8000' -ForegroundColor Magenta
    Write-Host 'Controls migration: 0% → 100%' -ForegroundColor Yellow
    python proxy.py
}"

Write-Host ""
Write-Host "✅ All services started!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 URLs:" -ForegroundColor Cyan
Write-Host "   Legacy System: http://localhost:5000" -ForegroundColor Gray
Write-Host "   Cloud Service: http://localhost:5001" -ForegroundColor Gray
Write-Host "   Smart Proxy:   http://localhost:8000" -ForegroundColor Gray
Write-Host ""
Write-Host "🧪 Test API:" -ForegroundColor Cyan
Write-Host "   curl -X POST http://localhost:8000/proxy/metrics" -ForegroundColor Gray
Write-Host ""
Write-Host "Close any terminal to stop that service." -ForegroundColor Yellow