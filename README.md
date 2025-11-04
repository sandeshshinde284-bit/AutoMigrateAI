# AutoMigrate AI - Smart Enterprise Modernization

## Overview
Intelligent legacy-to-cloud transformation platform for Volkswagen Group

## Quick Start

### Local Development
```bash
# Activate virtual environment
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows

# Run all services
bash scripts/run_local.sh
```

### Google Cloud Deployment
```bash
bash scripts/setup_gcp.sh
bash scripts/deploy_cloud_run.sh
```

## Project Structure
automigrateai-demo/
├── backend/           # Python services
├── frontend/          # Vue.js dashboard
├── docker/            # Docker configurations
├── gcp/               # Google Cloud configs
├── scripts/           # Deployment scripts
└── docs/              # Documentation

## Services
- **Legacy System** (Port 5000) - Simulates old VW system
- **Cloud Service** (Port 5001) - Modern FastAPI service
- **Proxy** (Port 8000) - Smart router
- **Frontend** (Port 5173) - Vue.js dashboard