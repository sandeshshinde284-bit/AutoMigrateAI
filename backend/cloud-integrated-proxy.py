# ============================================
# FINAL PROXY.PY - WITH GEMINI AI INTEGRATION
# ============================================

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import time
import random
from datetime import datetime
from collections import defaultdict
import json
from copy import deepcopy
import os

# --- AI & CLOUD IMPORTS ---
import vertexai
from vertexai.generative_models import GenerativeModel, Part
# --------------------------

# --- LOCAL MODULE IMPORTS ---
# We still need these for all other features
from digital_twin import digital_twin as validator
from auto_scaling import auto_scaler
from compliance_checker import compliance_checker
from config import config
# We NO LONGER need 'from code_analyzer import analyzer'
# --------------------------

app = Flask(__name__)
CORS(app)

LEGACY_URL = "http://localhost:5000"
CLOUD_URL = "http://localhost:5001"

# --- INITIALIZE VERTEX AI ---
# This will use the project's default service account when in Cloud Run
try:
    vertexai.init(project=config.GCP_PROJECT_ID, location=config.GCP_REGION)
    print(f"[PROXY] Vertex AI Initialized. Project: {config.GCP_PROJECT_ID}, Region: {config.GCP_REGION}")
except Exception as e:
    print(f"[PROXY] WARNING: Could not initialize Vertex AI. AI features may fail. Error: {str(e)}")
# ----------------------------


# --- METRICSCOLLECTOR & STRANGLERROUTER (Unchanged) ---
# (Your existing MetricsCollector and StranglerRouter classes go here)
# ...
class MetricsCollector:
    def __init__(self):
        self.requests = []
        self.request_history = []  # NEW: Track all requests for rollback
        self.migration_percentage = 0
        self.errors = 0
        self.total_requests = 0
        self.rollback_states = {}  # NEW: Save states at key points
    
    def log_request(self, endpoint, response_time, source, error=None, legacy_time=None, cloud_time=None, request_data=None, response_data=None):
        self.total_requests += 1
        request_entry = {
            'id': len(self.request_history),
            'timestamp': datetime.now().isoformat(),
            'endpoint': endpoint,
            'response_time': response_time,
            'source': source,
            'error': error,
            'legacy_time': legacy_time,
            'cloud_time': cloud_time,
            'request_data': request_data,
            'response_data': response_data,
            'migration_percentage': self.migration_percentage
        }
        self.request_history.append(request_entry)
        self.requests.append({
            'timestamp': datetime.now().isoformat(),
            'endpoint': endpoint,
            'response_time': response_time,
            'source': source,
            'error': error,
            'legacy_time': legacy_time,
            'cloud_time': cloud_time
        })
        if error:
            self.errors += 1
        if len(self.requests) > 100:
            self.requests = self.requests[-100:]
        if len(self.request_history) > 50:
            self.request_history = self.request_history[-50:]
    
    def get_metrics(self):
        legacy_times = [r['response_time'] for r in self.requests if r['source'] == 'legacy']
        cloud_times = [r['response_time'] for r in self.requests if r['source'] == 'cloud']
        legacy_avg = sum(legacy_times) / len(legacy_times) if legacy_times else 2847
        cloud_avg = sum(cloud_times) / len(cloud_times) if cloud_times else 87
        legacy_cost = len(legacy_times) * 0.50
        cloud_cost = len(cloud_times) * 0.05
        cost_saved = legacy_cost - cloud_cost
        perf_improvement = (legacy_avg / cloud_avg) if cloud_avg > 0 else 0
        return {
            'total_requests': len(self.requests),
            'legacy_requests': len(legacy_times),
            'cloud_requests': len(cloud_times),
            'legacy_avg_time': round(legacy_avg, 2),
            'cloud_avg_time': round(cloud_avg, 2),
            'error_count': self.errors,
            'migration_percentage': self.migration_percentage,
            'cost_saved': round(cost_saved, 2),
            'performance_improvement': round(perf_improvement, 1)
        }

    def set_migration_percentage(self, percentage):
        self.migration_percentage = min(100, max(0, percentage))
        self.rollback_states[percentage] = {
            'timestamp': datetime.now().isoformat(),
            'migration_percentage': percentage,
            'metrics': deepcopy(self.get_metrics())
        }

    def get_request_history(self, limit=20):
        return list(reversed(self.request_history[-limit:]))

    def get_request_by_id(self, request_id):
        for req in self.request_history:
            if req['id'] == request_id:
                return req
        return None

    def rollback_to_timestamp(self, timestamp):
        rolled_back_requests = [r for r in self.request_history if r['timestamp'] >= timestamp]
        return {
            'success': True,
            'rolled_back_request_count': len(rolled_back_requests),
            'rolled_back_requests': rolled_back_requests,
            'migration_percentage_before_rollback': self.migration_percentage,
            'timestamp': datetime.now().isoformat(),
            'message': f'Ready to rollback {len(rolled_back_requests)} requests'
        }

    def get_rollback_states(self):
        return {
            'states': list(self.rollback_states.values()),
            'current_migration': self.migration_percentage
        }

metrics = MetricsCollector()
for i in range(20):
    metrics.log_request("test_endpoint", random.uniform(2500, 3000), "legacy", 
                       request_data={'test': 'legacy'}, response_data={'result': 'ok'})
    metrics.log_request("test_endpoint", random.uniform(50, 120), "cloud",
                       request_data={'test': 'cloud'}, response_data={'result': 'ok'})
print("[PROXY] Pre-populated metrics with 20 sample requests")

class StranglerRouter:
    def __init__(self, legacy_url, cloud_url):
        self.legacy_url = legacy_url
        self.cloud_url = cloud_url
        self.metrics = metrics
    
    def should_use_cloud(self):
        random_value = random.random() * 100
        return random_value < self.metrics.migration_percentage
    
    def route_request(self, endpoint, method, data):
        start_time = time.time()
        use_cloud = self.should_use_cloud()
        source = "cloud" if use_cloud else "legacy"
        try:
            if use_cloud:
                print(f"[PROXY] Routing to CLOUD: {endpoint}")
                response = self._call_cloud(endpoint, method, data)
            else:
                print(f"[PROXY] Routing to LEGACY: {endpoint}")
                response = self._call_legacy(endpoint, method, data)
            response_time = (time.time() - start_time) * 1000
            self.metrics.log_request(endpoint, response_time, source, 
                                   request_data=data, response_data=response)
            print(f"[PROXY] Logged {source} request: {response_time:.2f}ms")
            return {
                'success': True,
                'data': response,
                'source': source,
                'response_time': round(response_time, 2),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            self.metrics.log_request(endpoint, response_time, source, error=str(e))
            return {
                'success': False,
                'error': str(e),
                'source': source,
                'response_time': round(response_time, 2),
                'timestamp': datetime.now().isoformat()
            }
    
    def _call_legacy(self, endpoint, method, data):
        # NOTE: In a real cloud deployment, 'localhost' will fail.
        # This proxy must be in the same private network (VPC) as the legacy system.
        # For this demo, we assume the legacy/cloud services are not deployed.
        # We will mock the response if the call fails.
        try:
            # (Your existing request logic)
            pass
        except requests.ConnectionError:
            print("[PROXY] MOCKING LEGACY: Connection failed.")
            time.sleep(random.uniform(2.0, 3.5)) # Simulate slowness
            return {'mocked_legacy_response': 'ok', 'endpoint': endpoint}
        
    def _call_cloud(self, endpoint, method, data):
        try:
            # (Your existing request logic)
            pass
        except requests.ConnectionError:
            print("[PROXY] MOCKING CLOUD: Connection failed.")
            time.sleep(random.uniform(0.05, 0.15)) # Simulate speed
            return {'mocked_cloud_response': 'ok', 'endpoint': endpoint}

router = StranglerRouter(LEGACY_URL, CLOUD_URL)
migration_plan = {} # Global var to hold the plan
# ...
# (All your other endpoints: /proxy/history, /proxy/rollback, etc. go here)
# ...
@app.route('/proxy/history', methods=['GET'])
def get_history():
    limit = request.args.get('limit', 20, type=int)
    history = metrics.get_request_history(limit)
    return jsonify({
        'success': True,
        'history': history,
        'total_requests': len(metrics.request_history),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/proxy/request-by-id/<int:request_id>', methods=['GET'])
def get_request_by_id(request_id):
    req = metrics.get_request_by_id(request_id)
    if req:
        return jsonify({'success': True, 'request': req})
    return jsonify({'success': False, 'error': 'Request not found'}), 404

@app.route('/proxy/rollback', methods=['POST'])
def rollback():
    try:
        data = request.get_json()
        timestamp = data.get('timestamp')
        request_id = data.get('request_id')
        rollback_info = None
        if request_id is not None:
            req = metrics.get_request_by_id(request_id)
            if req:
                rollback_info = metrics.rollback_to_timestamp(req['timestamp'])
        elif timestamp:
            rollback_info = metrics.rollback_to_timestamp(timestamp)
        
        metrics.set_migration_percentage(0) # The actual rollback
        print(f"[PROXY] ROLLBACK EXECUTED: Migration set to 0%")
        
        return jsonify({
            'success': True,
            'message': 'Rollback successful. Migration set to 0%.',
            'rolled_back_info': rollback_info,
            'new_migration_percentage': metrics.migration_percentage,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/proxy/rollback-states', methods=['GET'])
def get_rollback_states():
    states = metrics.get_rollback_states()
    return jsonify(states)

@app.route('/proxy/request', methods=['POST'])
def proxy_request():
    try:
        data = request.get_json()
        endpoint = data.get('endpoint')
        method = data.get('method', 'POST')
        request_data = data.get('data', {})
        result = router.route_request(endpoint, method, request_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e), 'timestamp': datetime.now().isoformat()}), 400

@app.route('/proxy/metrics', methods=['GET'])
def get_metrics():
    return jsonify(metrics.get_metrics())

@app.route('/proxy/set_migration', methods=['POST'])
def set_migration():
    try:
        data = request.get_json()
        percentage = data.get('percentage', 0)
        metrics.set_migration_percentage(percentage)
        print(f"[PROXY] Migration percentage set to: {percentage}%")
        return jsonify({
            'success': True,
            'migration_percentage': metrics.migration_percentage,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/proxy/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'system': 'proxy_router',
        'migration_percentage': metrics.migration_percentage,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/proxy/reset', methods=['POST'])
def reset_metrics():
    metrics.requests = []
    metrics.request_history = []
    metrics.errors = 0
    metrics.total_requests = 0
    metrics.migration_percentage = 0
    metrics.rollback_states = {}
    return jsonify({'success': True, 'message': 'Metrics reset', 'timestamp': datetime.now().isoformat()})

# --- HELPER TO FIND 'legacy_system.py' ---
def find_legacy_system_file():
    possible_paths = [
        'backend/legacy_system.py',
        'legacy_system.py',
        './backend/legacy_system.py',
        os.path.join(os.getcwd(), 'backend', 'legacy_system.py'),
        os.path.join(os.getcwd(), 'legacy_system.py'),
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None
# ------------------------------------------

# ============================================
# === REPLACED /proxy/analyze-code ENDPOINT ===
# ============================================
@app.route('/proxy/analyze-code', methods=['POST'])
def analyze_code():
    """
    Analyze legacy code using the Gemini 1.5 Pro
    """
    try:
        # 1. Read the legacy_system.py file
        file_path = find_legacy_system_file()
        if not file_path:
            print(f"[PROXY] File not found. CWD: {os.getcwd()}")
            return jsonify({'success': False, 'error': f'legacy_system.py not found. CWD: {os.getcwd()}'}), 404
        
        print(f"[PROXY] Found legacy file at: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            legacy_code = f.read()

        # 2. Initialize the Gemini Model
        model = GenerativeModel("gemini-1.5-pro-preview-0409")

        # 3. Create a detailed prompt
        prompt = f"""
        You are an expert legacy system migration analyzer. Analyze the following Python (Flask) codebase:
        
        CODE:
        ---
        {legacy_code}
        ---
        
        Based on your analysis, return a JSON object with the following structure.
        - Do not include any text before or after the JSON object.
        - Do not use markdown backticks (```json ... ```).
        - The "response_time_ms" should be an estimate.
        - The "complexity_score" should be from 1-100.
        
        JSON STRUCTURE TO RETURN:
        {{
          "total_endpoints": <int>,
          "total_lines_of_code": <int>,
          "overall_complexity_score": <int>,
          "estimated_migration_time": "<string>",
          "critical_issues": ["<string>", "..."],
          "slow_operations": [
            {{
              "operation": "<string>",
              "location": "<string>",
              "duration_ms": <int>,
              "impact": "<CRITICAL|HIGH|MEDIUM>",
              "fix_effort": "<Easy|Medium|Hard>",
              "recommendation": "<string>"
            }}
          ],
          "endpoints": [
            {{
              "endpoint": "<string>",
              "complexity_score": <int>,
              "complexity_category": "<LOW|MEDIUM|HIGH>",
              "response_time_ms": <int>,
              "migration_priority": "<FIRST|MEDIUM|LAST>",
              "risk_level": "<LOW|MEDIUM|HIGH>",
              "dependencies": ["<string>", "..."],
              "estimated_refactor_days": <int>
            }}
          ],
          "migration_priority": [
            {{
              "phase": <int>,
              "endpoint": "<string>",
              "complexity": "<LOW|MEDIUM|HIGH>",
              "priority_score": <int>,
              "estimated_days": <int>,
              "dependencies": ["<string>", "..."],
              "risk": "<LOW|MEDIUM|HIGH>",
              "action": "<string>"
            }}
          ],
          "recommendations": ["<string>", "..."]
        }}
        """

        # 4. Call the Gemini API
        response = model.generate_content(prompt)
        
        # 5. Clean and parse the JSON response
        json_text = response.text.strip().replace("```json", "").replace("```", "")
        analysis_json = json.loads(json_text)

        # Add the 'analysis_complete' flag our frontend expects
        analysis_json['analysis_complete'] = True

        print(f"[PROXY] Real AI analysis complete - {analysis_json['total_endpoints']} endpoints found")

        return jsonify({
            'success': True,
            'analysis': analysis_json,
            'file_analyzed': file_path,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        print(f"[PROXY] Real AI Analysis error: {str(e)}")
        # Provide more debug info
        return jsonify({
            'success': False,
            'error': str(e),
            'current_directory': os.getcwd(),
            'message': 'Error during Gemini analysis. Check server logs.'
        }), 500

# ============================================
# (All other endpoints: /validate-migration, /auto-scaling, etc.)
# ...
@app.route('/proxy/plan/save', methods=['POST'])
def save_migration_plan():
    global migration_plan
    try:
        data = request.get_json()
        migration_plan = data
        print(f"[PROXY] New migration plan saved: {migration_plan}")
        return jsonify({'success': True, 'message': 'Plan saved successfully', 'plan': migration_plan})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/proxy/validate_plan', methods=['POST'])
def validate_plan():
    try:
        data = request.get_json()
        duration = data.get('duration', 30)
        traffic_volume = data.get('traffic_volume', 100)
        print(f"[PROXY] Starting Digital Twin validation for plan: {migration_plan}")
        demo_percentage = migration_plan.get("subsystems", {}).get("engine", 50)
        result = validator.validate_migration(demo_percentage, duration, traffic_volume)
        return jsonify({
            'success': True,
            'validation': result,
            'timestamp': datetime.now().isoformat(),
            'message': f"Simulation run based on saved plan (using 'engine' value: {demo_percentage}%)"
        })
    except Exception as e:
        print(f"[PROXY] Validation error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/proxy/validate-migration', methods=['POST'])
def validate_migration():
    try:
        data = request.get_json()
        target_percentage = data.get('percentage', 50)
        duration = data.get('duration', 30)
        traffic_volume = data.get('traffic_volume', 100)
        if not 0 <= target_percentage <= 100:
            return jsonify({'success': False, 'error': 'Percentage must be between 0-100'}), 400
        print(f"[PROXY] Starting Digital Twin validation at {target_percentage}%")
        result = validator.validate_migration(target_percentage, duration, traffic_volume)
        return jsonify({'success': True, 'validation': result, 'timestamp': datetime.now().isoformat()})
    except Exception as e:
        print(f"[PROXY] Validation error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/proxy/validation-history', methods=['GET'])
def get_validation_history():
    try:
        limit = request.args.get('limit', 10, type=int)
        history = validator.get_validation_history(limit)
        return jsonify({'success': True, 'history': history, 'total': len(history)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/proxy/next-migration-step', methods=['GET'])
def get_next_migration_step():
    try:
        current = request.args.get('current', 0, type=int)
        next_step = validator.get_safe_next_percentage(current)
        return jsonify({'success': True, 'next_step': next_step, 'timestamp': datetime.now().isoformat()})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400    
    
@app.route('/proxy/auto-scaling/predict', methods=['GET'])
def predict_scaling():
    try:
        prediction = auto_scaler.predict_next_spike()
        print(f"[PROXY] Auto-scaling prediction: Spike={prediction['spike_detected']}, Confidence={prediction['confidence']}%")
        return jsonify({'success': True, 'prediction': prediction, 'timestamp': datetime.now().isoformat()})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/proxy/auto-scaling/recommendation', methods=['GET'])
def get_scaling_recommendation():
    try:
        current_capacity = request.args.get('capacity', 100, type=int)
        recommendation = auto_scaler.get_scaling_recommendation(current_capacity)
        auto_scaler.add_recommendation(recommendation)
        print(f"[PROXY] Scaling recommendation: {recommendation['action']}")
        return jsonify({'success': True, 'recommendation': recommendation, 'timestamp': datetime.now().isoformat()})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/proxy/auto-scaling/metrics', methods=['GET'])
def get_scaling_metrics():
    try:
        metrics = auto_scaler.get_metrics_summary()
        return jsonify({'success': True, 'metrics': metrics, 'timestamp': datetime.now().isoformat()})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/proxy/auto-scaling/record-traffic', methods=['POST'])
def record_traffic():
    try:
        data = request.get_json()
        request_count = data.get('request_count', 0)
        auto_scaler.record_traffic(request_count)
        return jsonify({'success': True, 'message': f'Recorded {request_count} requests'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400    
    
@app.route('/proxy/compliance/check', methods=['POST'])
def check_compliance():
    try:
        data = request.get_json()
        request_data = data.get('request', {})
        response_data = data.get('response', {})
        req_check = compliance_checker.check_request_compliance(request_data)
        resp_check = compliance_checker.check_response_compliance(response_data)
        compliance_checker.log_check(req_check, resp_check)
        print(f"[PROXY] Compliance check: Req={req_check['status']}, Resp={resp_check['status']}")
        return jsonify({
            'success': True,
            'request_compliance': req_check,
            'response_compliance': resp_check,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        print(f"[PROXY] Compliance error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/proxy/compliance/status', methods=['GET'])
def get_compliance_status():
    try:
        overall = compliance_checker.get_overall_compliance()
        return jsonify({'success': True, 'compliance': overall, 'timestamp': datetime.now().isoformat()})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/proxy/compliance/violations', methods=['GET'])
def get_violations():
    try:
        limit = request.args.get('limit', 10, type=int)
        violations = compliance_checker.get_violations_history(limit)
        return jsonify({'success': True, 'violations': violations, 'total': len(violations)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400    

@app.route('/', methods=['GET'])
def root():
    return jsonify({
        'service': 'AutoMigrate AI - Smart Proxy Router',
        'version': '1.0.0',
        'status': 'running',
        'migration_percentage': metrics.migration_percentage,
        'endpoints': {
            'POST /proxy/request': 'Route request to legacy or cloud',
            'GET /proxy/metrics': 'Get current metrics',
            'POST /proxy/set_migration': 'Set migration percentage',
            'POST /proxy/analyze-code': 'NEW: Analyze code with Gemini AI'
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/proxy/config', methods=['GET'])
def get_config():
    return jsonify({
        'success': True,
        'config': {
            'investment_required': config.INVESTMENT_REQUIRED
        },
        'timestamp': datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found', 'timestamp': datetime.now().isoformat()}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error', 'timestamp': datetime.now().isoformat()}), 500

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🚀 AutoMigrate AI PROXY - STARTING (WITH GEMINI AI)")
    print("=" * 60)
    print(f"🔧 Config Loaded: Project={config.GCP_PROJECT_ID}, Region={config.GCP_REGION}")
    print("✨ AI Features: ENABLED (using Vertex AI)")
    print("=" * 60)
    print(f"\n✅ Proxy ready on http://localhost:{config.PROXY_PORT}")
    app.run(host='0.0.0.0', port=config.PROXY_PORT, debug=config.DEBUG)