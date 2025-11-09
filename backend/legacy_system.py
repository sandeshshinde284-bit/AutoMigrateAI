# ============================================
# PHASE 1 - BACKEND SERVICES
# ============================================
# File 1: backend/legacy_system.py
# Description: Simulates VW's 1995 Legacy System
# Port: 5000
# Response Time: 2-3 seconds (OLD, SLOW)
# Format: XML (OLD FORMAT)
# ============================================

import os
from flask import Flask, request, Response
import time
import json
import xml.etree.ElementTree as ET
from datetime import datetime
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ============================================
# LEGACY DATABASE (In-Memory)
# ============================================

INVENTORY_DB = {
    "PART001": {
        "PART_NO": "PART001",
        "PART_NAME": "Engine Block",
        "PART_DESC": "High-performance engine component",
        "STOCK_QTY": 150,
        "PRICE": 2500.50,
        "SUPPLIER": "BOSCH",
        "STATUS": "ACTIVE"
    },
    "PART002": {
        "PART_NO": "PART002",
        "PART_NAME": "Transmission Unit",
        "PART_DESC": "Automatic transmission assembly",
        "STOCK_QTY": 89,
        "PRICE": 5000.00,
        "SUPPLIER": "ZF",
        "STATUS": "ACTIVE"
    },
    "PART003": {
        "PART_NO": "PART003",
        "PART_NAME": "Brake Pads",
        "PART_DESC": "Ceramic brake pads set",
        "STOCK_QTY": 450,
        "PRICE": 180.00,
        "SUPPLIER": "BREMBO",
        "STATUS": "ACTIVE"
    },
    "PART004": {
        "PART_NO": "PART004",
        "PART_NAME": "Battery",
        "PART_DESC": "Lead-acid automotive battery",
        "STOCK_QTY": 220,
        "PRICE": 350.00,
        "SUPPLIER": "EXIDE",
        "STATUS": "ACTIVE"
    }
}

DEALERS_DB = {
    "DEALER_DE_001": {
        "DEALER_ID": "DEALER_DE_001",
        "DEALER_NAME": "Munich Motors",
        "COUNTRY": "DE",
        "TERRITORY": "Bavaria",
        "ACTIVE": True,
        "CONTACT": "Fritz@munichm.com"
    },
    "DEALER_IN_001": {
        "DEALER_ID": "DEALER_IN_001",
        "DEALER_NAME": "Delhi Auto Hub",
        "COUNTRY": "IN",
        "TERRITORY": "Northern India",
        "ACTIVE": True,
        "CONTACT": "rajesh@deliauto.com"
    },
    "DEALER_US_001": {
        "DEALER_ID": "DEALER_US_001",
        "DEALER_NAME": "Los Angeles Motors",
        "COUNTRY": "US",
        "TERRITORY": "California",
        "ACTIVE": True,
        "CONTACT": "john@lautos.com"
    }
}

# ============================================
# HELPER FUNCTIONS
# ============================================

def simulate_slow_database_call(delay=2.0):
    """Simulate slow legacy database access"""
    actual_delay = delay + random.uniform(-0.3, 0.8)
    time.sleep(actual_delay)

def to_xml(data, root_name="response"):
    """Convert dict to XML (legacy format)"""
    root = ET.Element(root_name)
    
    def build_xml(element, data):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    child = ET.SubElement(element, key)
                    build_xml(child, value)
                else:
                    child = ET.SubElement(element, key)
                    child.text = str(value)
        elif isinstance(data, list):
            for item in data:
                child = ET.SubElement(element, "item")
                build_xml(child, item)
    
    build_xml(root, data)
    return ET.tostring(root, encoding='unicode')

def log_legacy_request(endpoint, method, response_time):
    """Log all requests"""
    print(f"[LEGACY] {datetime.now()} | {method} {endpoint} | Response: {response_time:.0f}ms")

# ============================================
# LEGACY API ENDPOINTS
# ============================================

@app.route('/inventory/get_part', methods=['POST'])
def get_part():
    """Legacy endpoint: Get part by ID (SLOW - 2-3 seconds)"""
    start = time.time()
    
    data = request.get_json()
    part_no = data.get('part_number', 'UNKNOWN')
    
    print(f"[LEGACY] Looking up part: {part_no}")
    simulate_slow_database_call(delay=2.0)
    
    if part_no in INVENTORY_DB:
        response_data = {
            "status": "SUCCESS",
            "part": INVENTORY_DB[part_no],
            "timestamp": datetime.now().isoformat()
        }
    else:
        response_data = {
            "status": "ERROR",
            "message": f"Part {part_no} not found",
            "timestamp": datetime.now().isoformat()
        }
    
    xml_response = to_xml(response_data, "PartResponse")
    response_time = (time.time() - start) * 1000
    log_legacy_request('/inventory/get_part', 'POST', response_time)
    
    return Response(xml_response, mimetype='application/xml')

@app.route('/dealer/get_details', methods=['POST'])
def get_dealer_details():
    """Legacy endpoint: Get dealer info (SLOW - 1.5-2 seconds)"""
    start = time.time()
    
    data = request.get_json()
    dealer_id = data.get('dealer_id', 'UNKNOWN')
    
    print(f"[LEGACY] Looking up dealer: {dealer_id}")
    simulate_slow_database_call(delay=1.5)
    
    if dealer_id in DEALERS_DB:
        response_data = {
            "status": "SUCCESS",
            "dealer": DEALERS_DB[dealer_id],
            "timestamp": datetime.now().isoformat()
        }
    else:
        response_data = {
            "status": "ERROR",
            "message": f"Dealer {dealer_id} not found",
            "timestamp": datetime.now().isoformat()
        }
    
    xml_response = to_xml(response_data, "DealerResponse")
    response_time = (time.time() - start) * 1000
    log_legacy_request('/dealer/get_details', 'POST', response_time)
    
    return Response(xml_response, mimetype='application/xml')

@app.route('/inventory/list_all', methods=['GET'])
def list_all_inventory():
    """Legacy endpoint: List all parts (SLOW - 2.5-3 seconds)"""
    start = time.time()
    
    print("[LEGACY] Performing full inventory scan...")
    simulate_slow_database_call(delay=2.5)
    
    response_data = {
        "status": "SUCCESS",
        "part_count": len(INVENTORY_DB),
        "parts": list(INVENTORY_DB.values()),
        "timestamp": datetime.now().isoformat()
    }
    
    xml_response = to_xml(response_data, "InventoryResponse")
    response_time = (time.time() - start) * 1000
    log_legacy_request('/inventory/list_all', 'GET', response_time)
    
    return Response(xml_response, mimetype='application/xml')

@app.route('/orders/create', methods=['POST'])
def create_order():
    """Legacy endpoint: Create order (SLOW - 3-4 seconds)"""
    start = time.time()
    
    data = request.get_json()
    dealer_id = data.get('dealer_id')
    part_no = data.get('part_number')
    quantity = data.get('quantity', 1)
    
    print(f"[LEGACY] Creating order: Dealer={dealer_id}, Part={part_no}, Qty={quantity}")
    
    # Simulate complex legacy business logic with multiple delays
    time.sleep(0.5)  # Step 1: Validate dealer
    time.sleep(0.8)  # Step 2: Check inventory
    time.sleep(0.3)  # Step 3: Calculate discount
    time.sleep(0.7)  # Step 4: Generate order number
    time.sleep(0.7)  # Step 5: Write to database
    
    # Hidden business logic: Friday + German dealer + expensive part = 2% discount
    today = datetime.now()
    is_friday = today.weekday() == 4
    is_german_dealer = dealer_id.endswith("_DE_001") if dealer_id else False
    part_expensive = INVENTORY_DB.get(part_no, {}).get('PRICE', 0) > 1000
    
    discount = 0.02 if (is_friday and is_german_dealer and part_expensive) else 0
    
    response_data = {
        "status": "SUCCESS",
        "order": {
            "order_id": f"ORD-{int(time.time())}",
            "dealer_id": dealer_id,
            "part_number": part_no,
            "quantity": quantity,
            "discount_applied": discount,
            "discount_percentage": discount * 100,
            "created_at": datetime.now().isoformat()
        },
        "timestamp": datetime.now().isoformat()
    }
    
    xml_response = to_xml(response_data, "OrderResponse")
    response_time = (time.time() - start) * 1000
    log_legacy_request('/orders/create', 'POST', response_time)
    
    return Response(xml_response, mimetype='application/xml')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint (fast)"""
    return json.dumps({
        "status": "ok",
        "system": "legacy_vw_system",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/metrics/system', methods=['GET'])
def system_metrics():
    """Return system metrics"""
    return json.dumps({
        "system": "legacy_vw_inventory",
        "status": "running",
        "api_version": "1.0",
        "database": "Oracle 8i",
        "response_time_avg": "2500ms",
        "uptime": "423 days",
        "last_backup": "2024-01-15T02:30:00Z"
    })

@app.errorhandler(500)
def internal_error(error):
    xml_error = to_xml({
        "status": "ERROR",
        "message": "Internal Server Error",
        "timestamp": datetime.now().isoformat()
    }, "ErrorResponse")
    return Response(xml_error, mimetype='application/xml', status=500)

if __name__ == '__main__':
    print("=" * 60)
    print("🏭 VW LEGACY SYSTEM - RUNNING")
    print("=" * 60)
    print("📊 System: VW Dealer/Inventory Management (1995)")
    print("🔧 Database: Oracle 8i (Simulated)")
    print("⏱️  Response Time: 1.5-4 seconds")
    print("📝 Format: XML (Legacy)")
    print("=" * 60)
    print("\n🚀 Starting server on http://localhost:5050...")
    print("\n📍 Endpoints:")
    print("   POST /inventory/get_part")
    print("   POST /dealer/get_details")
    print("   GET  /inventory/list_all")
    print("   POST /orders/create")
    print("   GET  /health")
    print("   GET  /metrics/system")
    print("\n" + "=" * 60)
    
    port = int(os.environ.get("PORT", 5050))
    app.run(host='0.0.0.0', port=port, debug=False)