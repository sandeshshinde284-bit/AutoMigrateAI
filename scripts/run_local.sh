#!/bin/bash

echo "?? Starting AutoMigrate AI locally..."
echo ""

# Create terminal windows and run services
echo "Starting Legacy System (port 5000)..."
cd backend
python legacy_system.py &
LEGACY_PID=$!

echo "Starting Cloud Service (port 5001)..."
python cloud_service.py &
CLOUD_PID=$!

echo "Starting Proxy (port 8000)..."
python proxy.py &
PROXY_PID=$!

echo "Starting Frontend (port 5173)..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "? All services started!"
echo ""
echo "Legacy System: http://localhost:5000"
echo "Cloud Service: http://localhost:5001"
echo "Proxy: http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for all processes
wait
