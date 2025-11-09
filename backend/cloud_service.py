# ============================================
# PHASE 1 - CLOUD SERVICE
# ============================================
# File 2: backend/cloud_service.py
# Description: Modern Cloud-Native API
# Port: 5001
# Response Time: <100ms (FAST, MODERN)
# Format: JSON (MODERN FORMAT)
# ============================================

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import json
import os

app = FastAPI(
    title="VW Cloud Service",
    description="Modern cloud-native replacement for legacy VW system",
    version="1.0.0"
)

# ============================================
# PYDANTIC MODELS (Data Validation)
# ============================================

class PartRequest(BaseModel):
    part_number: str

class DealerRequest(BaseModel):
    dealer_id: str

class OrderRequest(BaseModel):
    dealer_id: str
    part_number: str
    quantity: int = 1

# ============================================
# IN-MEMORY DATABASE (Same as Legacy)
# ============================================

INVENTORY_DB = {
    "PART001": {
        "id": "PART001",
        "name": "Engine Block",
        "description": "High-performance engine component",
        "stock": 150,
        "price": 2500.50,
        "supplier": "BOSCH",
        "status": "active"
    },
    "PART002": {
        "id": "PART002",
        "name": "Transmission Unit",
        "description": "Automatic transmission assembly",
        "stock": 89,
        "price": 5000.00,
        "supplier": "ZF",
        "status": "active"
    },
    "PART003": {
        "id": "PART003",
        "name": "Brake Pads",
        "description": "Ceramic brake pads set",
        "stock": 450,
        "price": 180.00,
        "supplier": "BREMBO",
        "status": "active"
    },
    "PART004": {
        "id": "PART004",
        "name": "Battery",
        "description": "Lead-acid automotive battery",
        "stock": 220,
        "price": 350.00,
        "supplier": "EXIDE",
        "status": "active"
    }
}

DEALERS_DB = {
    "DEALER_DE_001": {
        "id": "DEALER_DE_001",
        "name": "Munich Motors",
        "country": "DE",
        "territory": "Bavaria",
        "active": True,
        "contact": "Fritz@munichm.com"
    },
    "DEALER_IN_001": {
        "id": "DEALER_IN_001",
        "name": "Delhi Auto Hub",
        "country": "IN",
        "territory": "Northern India",
        "active": True,
        "contact": "rajesh@deliauto.com"
    },
    "DEALER_US_001": {
        "id": "DEALER_US_001",
        "name": "Los Angeles Motors",
        "country": "US",
        "territory": "California",
        "active": True,
        "contact": "john@lautos.com"
    }
}

# ============================================
# MODERN API ENDPOINTS (FAST, JSON)
# ============================================

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint - Fast"""
    return {
        "status": "ok",
        "system": "cloud_vw_system",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/v1/parts/get")
async def get_part(request: PartRequest):
    """
    Get part by ID - FAST VERSION (<100ms)
    Modern JSON response
    """
    part_no = request.part_number
    
    print(f"[CLOUD] Looking up part: {part_no}")
    
    if part_no in INVENTORY_DB:
        return {
            "status": "SUCCESS",
            "data": {
                "part": INVENTORY_DB[part_no]
            },
            "timestamp": datetime.now().isoformat()
        }
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Part {part_no} not found"
        )

@app.post("/api/v1/dealers/get")
async def get_dealer_details(request: DealerRequest):
    """
    Get dealer by ID - FAST VERSION (<100ms)
    Modern JSON response
    """
    dealer_id = request.dealer_id
    
    print(f"[CLOUD] Looking up dealer: {dealer_id}")
    
    if dealer_id in DEALERS_DB:
        return {
            "status": "SUCCESS",
            "data": {
                "dealer": DEALERS_DB[dealer_id]
            },
            "timestamp": datetime.now().isoformat()
        }
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Dealer {dealer_id} not found"
        )

@app.get("/api/v1/inventory/list")
async def list_all_inventory():
    """
    List all parts - FAST VERSION (<100ms)
    Modern JSON response
    """
    print("[CLOUD] Listing all inventory...")
    
    return {
        "status": "SUCCESS",
        "data": {
            "part_count": len(INVENTORY_DB),
            "parts": list(INVENTORY_DB.values())
        },
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/v1/orders/create")
async def create_order(request: OrderRequest):
    """
    Create order - FAST VERSION (<100ms)
    Includes same business logic as legacy
    """
    dealer_id = request.dealer_id
    part_no = request.part_number
    quantity = request.quantity
    
    print(f"[CLOUD] Creating order: Dealer={dealer_id}, Part={part_no}, Qty={quantity}")
    
    # Validate dealer
    if dealer_id not in DEALERS_DB:
        raise HTTPException(status_code=404, detail=f"Dealer not found")
    
    # Validate part
    if part_no not in INVENTORY_DB:
        raise HTTPException(status_code=404, detail=f"Part not found")
    
    # Check stock
    if INVENTORY_DB[part_no]["stock"] < quantity:
        raise HTTPException(status_code=400, detail=f"Insufficient stock")
    
    # Calculate discount (SAME LOGIC AS LEGACY)
    today = datetime.now()
    is_friday = today.weekday() == 4
    is_german_dealer = dealer_id.endswith("_DE_001")
    part_expensive = INVENTORY_DB[part_no]["price"] > 1000
    
    discount = 0.02 if (is_friday and is_german_dealer and part_expensive) else 0
    
    return {
        "status": "SUCCESS",
        "data": {
            "order": {
                "order_id": f"ORD-{int(datetime.now().timestamp())}",
                "dealer_id": dealer_id,
                "part_number": part_no,
                "quantity": quantity,
                "discount_applied": discount,
                "discount_percentage": discount * 100,
                "created_at": datetime.now().isoformat()
            }
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/metrics/system")
async def system_metrics():
    """Return system metrics"""
    return {
        "system": "cloud_vw_system",
        "status": "running",
        "api_version": "1.0",
        "database": "Cloud Firestore",
        "response_time_avg": "<100ms",
        "uptime": "24/7",
        "last_update": datetime.now().isoformat()
    }

# ============================================
# STARTUP/SHUTDOWN EVENTS
# ============================================

@app.on_event("startup")
async def startup_event():
    print("\n" + "=" * 60)
    print("☁️  VW CLOUD SERVICE - STARTING")
    print("=" * 60)
    print("📊 System: Cloud-Native Modern API")
    print("🔧 Framework: FastAPI")
    print("⏱️  Response Time: <100ms")
    print("📝 Format: JSON (Modern)")
    print("=" * 60)
    print("\n✅ Cloud service ready on http://localhost:5001")

@app.on_event("shutdown")
async def shutdown_event():
    print("\n❌ Cloud service shutting down...")

# ============================================
# ERROR HANDLERS
# ============================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "ERROR",
            "message": exc.detail,
            "timestamp": datetime.now().isoformat()
        }
    )

# ============================================
# ROOT ENDPOINT
# ============================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "VW Cloud Service",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "timestamp": datetime.now().isoformat()
    }

# ============================================
# For running with: uvicorn cloud_service:app --reload --port 5001
# ============================================

if __name__ == "__main__":
   import uvicorn
   port = int(os.environ.get("PORT", 5001))
   uvicorn.run(app, host="0.0.0.0", port=port)