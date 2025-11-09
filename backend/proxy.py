# OLD CODE WHICH IS USEFUL FOR LOCAL RUNNING

# # ============================================
# # UPDATED proxy.py - WITH ROLLBACK & HISTORY
# # ============================================

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import requests
# import time
# import random
# from datetime import datetime
# from collections import defaultdict
# import json
# from copy import deepcopy
# from code_analyzer import analyzer as code_analyzer
# import os
# from digital_twin import digital_twin as validator
# from auto_scaling import auto_scaler
# from compliance_checker import compliance_checker
# from config import config

# app = Flask(__name__)
# CORS(app)

# LEGACY_URL = "http://localhost:5000"
# CLOUD_URL = "http://localhost:5001"

# # ============================================
# # ENHANCED METRICS STORAGE - WITH HISTORY
# # ============================================

# class MetricsCollector:
#     def __init__(self):
#         self.requests = []
#         self.request_history = []  # NEW: Track all requests for rollback
#         self.migration_percentage = 0
#         self.errors = 0
#         self.total_requests = 0
#         self.rollback_states = {}  # NEW: Save states at key points
    
#     def log_request(self, endpoint, response_time, source, error=None, legacy_time=None, cloud_time=None, request_data=None, response_data=None):
#         """Log a single request with full history"""
#         self.total_requests += 1
        
#         request_entry = {
#             'id': len(self.request_history),
#             'timestamp': datetime.now().isoformat(),
#             'endpoint': endpoint,
#             'response_time': response_time,
#             'source': source,
#             'error': error,
#             'legacy_time': legacy_time,
#             'cloud_time': cloud_time,
#             'request_data': request_data,
#             'response_data': response_data,
#             'migration_percentage': self.migration_percentage
#         }
        
#         self.request_history.append(request_entry)
#         self.requests.append({
#             'timestamp': datetime.now().isoformat(),
#             'endpoint': endpoint,
#             'response_time': response_time,
#             'source': source,
#             'error': error,
#             'legacy_time': legacy_time,
#             'cloud_time': cloud_time
#         })
        
#         if error:
#             self.errors += 1
        
#         # Keep only last 100 requests
#         if len(self.requests) > 100:
#             self.requests = self.requests[-100:]
        
#         # Keep only last 50 in history for rollback
#         if len(self.request_history) > 50:
#             self.request_history = self.request_history[-50:]
    
#     def get_metrics(self):
#         """Calculate and return aggregated metrics"""
#         legacy_times = [r['response_time'] for r in self.requests if r['source'] == 'legacy']
#         cloud_times = [r['response_time'] for r in self.requests if r['source'] == 'cloud']
        
#         legacy_avg = sum(legacy_times) / len(legacy_times) if legacy_times else 2847
#         cloud_avg = sum(cloud_times) / len(cloud_times) if cloud_times else 87
        
#         legacy_cost = len(legacy_times) * 0.50
#         cloud_cost = len(cloud_times) * 0.05
#         cost_saved = legacy_cost - cloud_cost
        
#         perf_improvement = (legacy_avg / cloud_avg) if cloud_avg > 0 else 0
        
#         return {
#             'total_requests': len(self.requests),
#             'legacy_requests': len(legacy_times),
#             'cloud_requests': len(cloud_times),
#             'legacy_avg_time': round(legacy_avg, 2),
#             'cloud_avg_time': round(cloud_avg, 2),
#             'error_count': self.errors,
#             'migration_percentage': self.migration_percentage,
#             'cost_saved': round(cost_saved, 2),
#             'performance_improvement': round(perf_improvement, 1)
#         }

#     def set_migration_percentage(self, percentage):
#         """Update migration percentage and save state"""
#         self.migration_percentage = min(100, max(0, percentage))
#         # Save state for potential rollback
#         self.rollback_states[percentage] = {
#             'timestamp': datetime.now().isoformat(),
#             'migration_percentage': percentage,
#             'metrics': deepcopy(self.get_metrics())
#         }

#     def get_request_history(self, limit=20):
#         """Get request history for display"""
#         return list(reversed(self.request_history[-limit:]))

#     def get_request_by_id(self, request_id):
#         """Get specific request by ID"""
#         for req in self.request_history:
#             if req['id'] == request_id:
#                 return req
#         return None

#     def rollback_to_timestamp(self, timestamp):
#         """Find requests after timestamp and prepare rollback info"""
#         rolled_back_requests = [r for r in self.request_history if r['timestamp'] >= timestamp]
        
#         return {
#             'success': True,
#             'rolled_back_request_count': len(rolled_back_requests),
#             'rolled_back_requests': rolled_back_requests,
#             'migration_percentage_before_rollback': self.migration_percentage,
#             'timestamp': datetime.now().isoformat(),
#             'message': f'Ready to rollback {len(rolled_back_requests)} requests'
#         }

#     def get_rollback_states(self):
#         """Get all saved states for rollback options"""
#         return {
#             'states': list(self.rollback_states.values()),
#             'current_migration': self.migration_percentage
#         }

# # Pre-populate with sample data
# metrics = MetricsCollector()
# for i in range(20):
#     metrics.log_request("test_endpoint", random.uniform(2500, 3000), "legacy", 
#                        request_data={'test': 'legacy'}, response_data={'result': 'ok'})
#     metrics.log_request("test_endpoint", random.uniform(50, 120), "cloud",
#                        request_data={'test': 'cloud'}, response_data={'result': 'ok'})

# print("[PROXY] Pre-populated metrics with 20 sample requests")

# # ============================================
# # STRANGLER PATTERN IMPLEMENTATION
# # ============================================

# class StranglerRouter:
#     def __init__(self, legacy_url, cloud_url):
#         self.legacy_url = legacy_url
#         self.cloud_url = cloud_url
#         self.metrics = metrics
    
#     def should_use_cloud(self):
#         """Decide whether to use cloud or legacy"""
#         random_value = random.random() * 100
#         return random_value < self.metrics.migration_percentage
    
#     def route_request(self, endpoint, method, data):
#         """Route request to legacy or cloud based on migration percentage"""
#         start_time = time.time()
        
#         use_cloud = self.should_use_cloud()
#         source = "cloud" if use_cloud else "legacy"
        
#         try:
#             if use_cloud:
#                 print(f"[PROXY] Routing to CLOUD: {endpoint}")
#                 response = self._call_cloud(endpoint, method, data)
#             else:
#                 print(f"[PROXY] Routing to LEGACY: {endpoint}")
#                 response = self._call_legacy(endpoint, method, data)
            
#             response_time = (time.time() - start_time) * 1000
            
#             # LOG WITH FULL HISTORY
#             self.metrics.log_request(endpoint, response_time, source, 
#                                    request_data=data, response_data=response)
#             print(f"[PROXY] Logged {source} request: {response_time:.2f}ms")
            
#             return {
#                 'success': True,
#                 'data': response,
#                 'source': source,
#                 'response_time': round(response_time, 2),
#                 'timestamp': datetime.now().isoformat()
#             }
        
#         except Exception as e:
#             response_time = (time.time() - start_time) * 1000
#             self.metrics.log_request(endpoint, response_time, source, error=str(e))
            
#             return {
#                 'success': False,
#                 'error': str(e),
#                 'source': source,
#                 'response_time': round(response_time, 2),
#                 'timestamp': datetime.now().isoformat()
#             }
    
#     def _call_legacy(self, endpoint, method, data):
#         """Call legacy system"""
#         if endpoint == "inventory/get_part":
#             url = f"{self.legacy_url}/inventory/get_part"
#         elif endpoint == "dealer/get_details":
#             url = f"{self.legacy_url}/dealer/get_details"
#         elif endpoint == "inventory/list_all":
#             url = f"{self.legacy_url}/inventory/list_all"
#         elif endpoint == "orders/create":
#             url = f"{self.legacy_url}/orders/create"
#         else:
#             url = f"{self.legacy_url}/{endpoint}"
        
#         if method == "POST":
#             response = requests.post(url, json=data, timeout=10)
#         else:
#             response = requests.get(url, timeout=10)
        
#         response.raise_for_status()
#         return response.text
    
#     def _call_cloud(self, endpoint, method, data):
#         """Call cloud service"""
#         cloud_endpoint_map = {
#             "inventory/get_part": "api/v1/parts/get",
#             "dealer/get_details": "api/v1/dealers/get",
#             "inventory/list_all": "api/v1/inventory/list",
#             "orders/create": "api/v1/orders/create"
#         }
        
#         cloud_endpoint = cloud_endpoint_map.get(endpoint, f"api/v1/{endpoint}")
#         url = f"{self.cloud_url}/{cloud_endpoint}"
        
#         if method == "POST":
#             response = requests.post(url, json=data, timeout=10)
#         else:
#             response = requests.get(url, timeout=10)
        
#         response.raise_for_status()
#         return response.json()

# router = StranglerRouter(LEGACY_URL, CLOUD_URL)

# # ============================================
# # NEW ENDPOINTS FOR ROLLBACK & HISTORY
# # ============================================

# @app.route('/proxy/history', methods=['GET'])
# def get_history():
#     """Get request history"""
#     limit = request.args.get('limit', 20, type=int)
#     history = metrics.get_request_history(limit)
#     return jsonify({
#         'success': True,
#         'history': history,
#         'total_requests': len(metrics.request_history),
#         'timestamp': datetime.now().isoformat()
#     })

# @app.route('/proxy/request-by-id/<int:request_id>', methods=['GET'])
# def get_request_by_id(request_id):
#     """Get specific request details"""
#     req = metrics.get_request_by_id(request_id)
#     if req:
#         return jsonify({
#             'success': True,
#             'request': req
#         })
#     return jsonify({
#         'success': False,
#         'error': 'Request not found'
#     }), 404

# # @app.route('/proxy/rollback', methods=['POST'])
# # def rollback():
# #     """Rollback to specific timestamp or request ID"""
# #     data = request.get_json()
# #     timestamp = data.get('timestamp')
# #     request_id = data.get('request_id')
    
# #     if timestamp:
# #         result = metrics.rollback_to_timestamp(timestamp)
# #     elif request_id is not None:
# #         req = metrics.get_request_by_id(request_id)
# #         if req:
# #             result = metrics.rollback_to_timestamp(req['timestamp'])
# #         else:
# #             return jsonify({'success': False, 'error': 'Request not found'}), 404
# #     else:
# #         return jsonify({'success': False, 'error': 'Provide timestamp or request_id'}), 400
    
# #     return jsonify(result)

# @app.route('/proxy/rollback', methods=['POST'])
# def rollback():
#     """Rollback to specific timestamp or request ID"""
#     try:
#         data = request.get_json()
#         timestamp = data.get('timestamp')
#         request_id = data.get('request_id')
        
#         # Find the requests that would be rolled back
#         # (This is good for logging, but not the main action)
#         rollback_info = None
#         if request_id is not None:
#             req = metrics.get_request_by_id(request_id)
#             if req:
#                 rollback_info = metrics.rollback_to_timestamp(req['timestamp'])
#         elif timestamp:
#             rollback_info = metrics.rollback_to_timestamp(timestamp)

#         # --- THIS IS THE ACTUAL FIX ---
#         # Set the migration percentage to 0
#         metrics.set_migration_percentage(0)
#         print(f"[PROXY] ROLLBACK EXECUTED: Migration set to 0%")
#         # -----------------------------

#         return jsonify({
#             'success': True,
#             'message': 'Rollback successful. Migration set to 0%.',
#             'rolled_back_info': rollback_info, # Optional: send back the report
#             'new_migration_percentage': metrics.migration_percentage,
#             'timestamp': datetime.now().isoformat()
#         })
        
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)}), 400

# @app.route('/proxy/rollback-states', methods=['GET'])
# def get_rollback_states():
#     """Get available rollback states"""
#     states = metrics.get_rollback_states()
#     return jsonify(states)

# # ============================================
# # EXISTING ENDPOINTS (UNCHANGED)
# # ============================================

# @app.route('/proxy/request', methods=['POST'])
# def proxy_request():
#     """Main proxy endpoint"""
#     try:
#         data = request.get_json()
#         endpoint = data.get('endpoint')
#         method = data.get('method', 'POST')
#         request_data = data.get('data', {})
        
#         result = router.route_request(endpoint, method, request_data)
#         return jsonify(result)
    
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e),
#             'timestamp': datetime.now().isoformat()
#         }), 400

# @app.route('/proxy/metrics', methods=['GET'])
# def get_metrics():
#     """Get current metrics"""
#     return jsonify(metrics.get_metrics())

# @app.route('/proxy/set_migration', methods=['POST'])
# def set_migration():
#     """Set migration percentage"""
#     try:
#         data = request.get_json()
#         percentage = data.get('percentage', 0)
        
#         metrics.set_migration_percentage(percentage)
        
#         print(f"[PROXY] Migration percentage set to: {percentage}%")
        
#         return jsonify({
#             'success': True,
#             'migration_percentage': metrics.migration_percentage,
#             'timestamp': datetime.now().isoformat()
#         })
    
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 400

# @app.route('/proxy/health', methods=['GET'])
# def health():
#     """Health check"""
#     return jsonify({
#         'status': 'ok',
#         'system': 'proxy_router',
#         'migration_percentage': metrics.migration_percentage,
#         'timestamp': datetime.now().isoformat()
#     })

# @app.route('/proxy/reset', methods=['POST'])
# def reset_metrics():
#     """Reset metrics and migration percentage"""
#     metrics.requests = []
#     metrics.request_history = []
#     metrics.errors = 0
#     metrics.total_requests = 0
#     metrics.migration_percentage = 0
#     metrics.rollback_states = {}
    
#     return jsonify({
#         'success': True,
#         'message': 'Metrics reset',
#         'timestamp': datetime.now().isoformat()
#     })

# # ============================================
# # ADD THIS NEW ENDPOINT (after /proxy/reset endpoint)
# # ============================================

# @app.route('/proxy/analyze-code', methods=['POST'])
# def analyze_code():
#     """Analyze legacy code for migration priority"""
#     try:
#         data = request.get_json()
#         codebase_file = data.get('file', 'legacy_system.py')
        
#         # Try multiple paths
#         possible_paths = [
#             f'backend/{codebase_file}',
#             codebase_file,
#             f'./backend/{codebase_file}',
#             f'../backend/{codebase_file}',
#             os.path.join(os.getcwd(), 'backend', codebase_file),
#         ]
        
#         file_path = None
#         for path in possible_paths:
#             if os.path.exists(path):
#                 file_path = path
#                 print(f"[PROXY] Found file at: {file_path}")
#                 break
        
#         if not file_path:
#             print(f"[PROXY] File not found in paths: {possible_paths}")
#             print(f"[PROXY] Current directory: {os.getcwd()}")
#             print(f"[PROXY] Files in backend/: {os.listdir('backend') if os.path.exists('backend') else 'backend/ does not exist'}")
            
#             return jsonify({
#                 'success': False,
#                 'error': f'{codebase_file} not found',
#                 'tried_paths': possible_paths,
#                 'current_directory': os.getcwd(),
#                 'message': 'Make sure legacy_system.py exists in backend/ directory'
#             }), 404
        
#         # Read the codebase with proper encoding handling
#         codebase = None
#         for encoding in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']:
#             try:
#                 with open(file_path, 'r', encoding=encoding) as f:
#                     codebase = f.read()
#                 print(f"[PROXY] File read with encoding: {encoding}")
#                 break
#             except (UnicodeDecodeError, LookupError):
#                 continue
        
#         if codebase is None:
#             return jsonify({
#                 'success': False,
#                 'error': 'Could not decode file with any encoding',
#                 'file_path': file_path,
#                 'message': 'Try saving the file as UTF-8'
#             }), 400
        
#         # Analyze it
#         analysis = code_analyzer.analyze_legacy_code(codebase)
        
#         print(f"[PROXY] Code analysis complete - {analysis['total_endpoints']} endpoints found")
        
#         return jsonify({
#             'success': True,
#             'analysis': analysis,
#             'file_analyzed': file_path,
#             'timestamp': datetime.now().isoformat()
#         })
    
#     except Exception as e:
#         print(f"[PROXY] Analysis error: {str(e)}")
#         return jsonify({
#             'success': False,
#             'error': str(e),
#             'current_directory': os.getcwd()
#         }), 400


# @app.route('/proxy/analyze-code-snippet', methods=['POST'])
# def analyze_code_snippet():
#     """Analyze custom code snippet"""
#     try:
#         data = request.get_json()
#         code_snippet = data.get('code', '')
        
#         if not code_snippet:
#             return jsonify({
#                 'success': False,
#                 'error': 'No code provided'
#             }), 400
        
#         analysis = code_analyzer.analyze_legacy_code(code_snippet)
        
#         return jsonify({
#             'success': True,
#             'analysis': analysis,
#             'timestamp': datetime.now().isoformat()
#         })
    
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 400

# @app.route('/proxy/validate-migration', methods=['POST'])
# def validate_migration():
#     """Validate migration at target percentage using Digital Twin"""
#     try:
#         data = request.get_json()
#         target_percentage = data.get('percentage', 50)
#         duration = data.get('duration', 30)
#         traffic_volume = data.get('traffic_volume', 100)
        
#         # Validate inputs
#         if not 0 <= target_percentage <= 100:
#             return jsonify({
#                 'success': False,
#                 'error': 'Percentage must be between 0-100'
#             }), 400
        
#         print(f"[PROXY] Starting Digital Twin validation at {target_percentage}%")
        
#         # Run validation
#         result = validator.validate_migration(target_percentage, duration, traffic_volume)
        
#         return jsonify({
#             'success': True,
#             'validation': result,
#             'timestamp': datetime.now().isoformat()
#         })
    
#     except Exception as e:
#         print(f"[PROXY] Validation error: {str(e)}")
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 400

# @app.route('/proxy/validation-history', methods=['GET'])
# def get_validation_history():
#     """Get recent validation runs"""
#     try:
#         limit = request.args.get('limit', 10, type=int)
#         history = validator.get_validation_history(limit)
        
#         return jsonify({
#             'success': True,
#             'history': history,
#             'total': len(history)
#         })
    
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 400

# @app.route('/proxy/next-migration-step', methods=['GET'])
# def get_next_migration_step():
#     """Get recommendation for next migration percentage"""
#     try:
#         current = request.args.get('current', 0, type=int)
        
#         next_step = validator.get_safe_next_percentage(current)
        
#         return jsonify({
#             'success': True,
#             'next_step': next_step,
#             'timestamp': datetime.now().isoformat()
#         })
    
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 400    
    
# @app.route('/proxy/auto-scaling/predict', methods=['GET'])
# def predict_scaling():
#     """Get auto-scaling prediction"""
#     try:
#         prediction = auto_scaler.predict_next_spike()
        
#         print(f"[PROXY] Auto-scaling prediction: Spike={prediction['spike_detected']}, Confidence={prediction['confidence']}%")
        
#         return jsonify({
#             'success': True,
#             'prediction': prediction,
#             'timestamp': datetime.now().isoformat()
#         })
    
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 400

# @app.route('/proxy/auto-scaling/recommendation', methods=['GET'])
# def get_scaling_recommendation():
#     """Get scaling recommendation"""
#     try:
#         current_capacity = request.args.get('capacity', 100, type=int)
        
#         recommendation = auto_scaler.get_scaling_recommendation(current_capacity)
#         auto_scaler.add_recommendation(recommendation)
        
#         print(f"[PROXY] Scaling recommendation: {recommendation['action']}")
        
#         return jsonify({
#             'success': True,
#             'recommendation': recommendation,
#             'timestamp': datetime.now().isoformat()
#         })
    
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 400

# @app.route('/proxy/auto-scaling/metrics', methods=['GET'])
# def get_scaling_metrics():
#     """Get current scaling metrics"""
#     try:
#         metrics = auto_scaler.get_metrics_summary()
        
#         return jsonify({
#             'success': True,
#             'metrics': metrics,
#             'timestamp': datetime.now().isoformat()
#         })
    
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 400

# @app.route('/proxy/auto-scaling/record-traffic', methods=['POST'])
# def record_traffic():
#     """Record traffic for auto-scaling analysis"""
#     try:
#         data = request.get_json()
#         request_count = data.get('request_count', 0)
        
#         auto_scaler.record_traffic(request_count)
        
#         return jsonify({
#             'success': True,
#             'message': f'Recorded {request_count} requests'
#         })
    
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 400    
    
# @app.route('/proxy/compliance/check', methods=['POST'])
# def check_compliance():
#     """Check request/response for compliance violations"""
#     try:
#         data = request.get_json()
#         request_data = data.get('request', {})
#         response_data = data.get('response', {})
        
#         # Check both
#         req_check = compliance_checker.check_request_compliance(request_data)
#         resp_check = compliance_checker.check_response_compliance(response_data)
        
#         # Log
#         compliance_checker.log_check(req_check, resp_check)
        
#         print(f"[PROXY] Compliance check: Req={req_check['status']}, Resp={resp_check['status']}")
        
#         return jsonify({
#             'success': True,
#             'request_compliance': req_check,
#             'response_compliance': resp_check,
#             'timestamp': datetime.now().isoformat()
#         })
    
#     except Exception as e:
#         print(f"[PROXY] Compliance error: {str(e)}")
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 400

# @app.route('/proxy/compliance/status', methods=['GET'])
# def get_compliance_status():
#     """Get overall compliance status"""
#     try:
#         overall = compliance_checker.get_overall_compliance()
        
#         return jsonify({
#             'success': True,
#             'compliance': overall,
#             'timestamp': datetime.now().isoformat()
#         })
    
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 400

# @app.route('/proxy/compliance/violations', methods=['GET'])
# def get_violations():
#     """Get recent violations"""
#     try:
#         limit = request.args.get('limit', 10, type=int)
#         violations = compliance_checker.get_violations_history(limit)
        
#         return jsonify({
#             'success': True,
#             'violations': violations,
#             'total': len(violations)
#         })
    
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         }), 400    

# @app.route('/', methods=['GET'])
# def root():
#     """Root endpoint"""
#     return jsonify({
#         'service': 'AutoMigrate AI - Smart Proxy Router',
#         'version': '1.0.0',
#         'status': 'running',
#         'migration_percentage': metrics.migration_percentage,
#         'total_requests': metrics.total_requests,
#         'endpoints': {
#             'POST /proxy/request': 'Route request to legacy or cloud',
#             'GET /proxy/metrics': 'Get current metrics',
#             'GET /proxy/history': 'Get request history (NEW)',
#             'GET /proxy/request-by-id/<id>': 'Get specific request (NEW)',
#             'POST /proxy/rollback': 'Rollback to timestamp (NEW)',
#             'GET /proxy/rollback-states': 'Get rollback states (NEW)',
#             'POST /proxy/set_migration': 'Set migration percentage',
#             'GET /proxy/health': 'Health check',
#             'POST /proxy/reset': 'Reset metrics',
#             'POST /proxy/analyze-code': 'Analyze legacy code file',
#             'POST /proxy/analyze-code-snippet': 'Analyze code snippet'
#         },
#         'timestamp': datetime.now().isoformat()
#     })

# @app.route('/proxy/config', methods=['GET'])
# def get_config():
#     """Get application configuration values"""
#     return jsonify({
#         'success': True,
#         'config': {
#             'investment_required': config.INVESTMENT_REQUIRED
#         },
#         'timestamp': datetime.now().isoformat()
#     })

# @app.errorhandler(404)
# def not_found(error):
#     return jsonify({
#         'error': 'Endpoint not found',
#         'timestamp': datetime.now().isoformat()
#     }), 404

# @app.errorhandler(500)
# def internal_error(error):
#     return jsonify({
#         'error': 'Internal server error',
#         'timestamp': datetime.now().isoformat()
#     }), 500

# if __name__ == '__main__':
#     print("\n" + "=" * 60)
#     print("🔧 SMART PROXY ROUTER - STARTING (WITH ROLLBACK)")
#     print("=" * 60)
#     print("📡 Service: Migration Orchestrator + Request History")
#     print("🎯 Pattern: Strangler Fig Pattern")
#     print("✨ New: Rollback & History Tracking")
#     print("=" * 60)
#     print("\n✅ Proxy ready on http://localhost:8000")
#     print("\n🔑 NEW Endpoints:")
#     print("   GET  /proxy/history              (Get request history)")
#     print("   GET  /proxy/request-by-id/<id>   (Get specific request)")
#     print("   POST /proxy/rollback             (Rollback to timestamp)")
#     print("   GET  /proxy/rollback-states      (Get rollback options)")
#     print("\n" + "=" * 60)
    
#     port = int(os.environ.get("PORT", config.PROXY_PORT))
#     app.run(host='0.0.0.0', port=port, debug=config.DEBUG)


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

# LEGACY_URL = "http://localhost:5000"
# CLOUD_URL = "http://localhost:5001"

LEGACY_URL = "https://automigrate-legacy-157263375859.us-central1.run.app"
CLOUD_URL = "https://automigrate-cloud-157263375859.us-central1.run.app"

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
        # The try/except is now removed. We want to see real errors.
        if endpoint == "inventory/get_part":
            url = f"{self.legacy_url}/inventory/get_part"
        # ... (all your other 'elif's) ...
        else:
            url = f"{self.legacy_url}/{endpoint}"

        if method == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            response = requests.get(url, timeout=10)

        response.raise_for_status()
        return response.text # Legacy returns text/XML
        
    def _call_cloud(self, endpoint, method, data):
        """Call cloud service"""
        cloud_endpoint_map = {
            "inventory/get_part": "api/v1/parts/get",
            "dealer/get_details": "api/v1/dealers/get",
            "inventory/list_all": "api/v1/inventory/list",
            "orders/create": "api/v1/orders/create"
        }
        
        cloud_endpoint = cloud_endpoint_map.get(endpoint, f"api/v1/{endpoint}")
        url = f"{self.cloud_url}/{cloud_endpoint}"
        
        if method == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            response = requests.get(url, timeout=10)
        
        response.raise_for_status()
        return response.json() # Cloud service returns JSON

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

        models_to_try = [
            "gemini-2.0-flash",
            "gemini-2.5-flash", 
            "gemini-1.5-flash",
            "gemini-2.5-pro",
            "gemini-1.5-pro",
        ]
        model = None
        for model_name in models_to_try:
            try:
                model = GenerativeModel(model_name)
                model.generate_content("test", generation_config={"max_output_tokens": 2})
                print(f"   ✅ Using {model_name}")
                break
            except Exception as e:
                print(f"   ⚠️  {model_name} unavailable")
                continue    

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
    port = int(os.environ.get("PORT", config.PROXY_PORT))
    app.run(host='0.0.0.0', port=port, debug=config.DEBUG)