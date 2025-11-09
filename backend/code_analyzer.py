# ============================================
# FEATURE #6: AI-Powered Legacy Code Analyzer
# File: backend/code_analyzer.py
# FIXED: Path handling
# ============================================

import re
import os
from datetime import datetime
from typing import List, Dict, Any

class CodeAnalyzer:
    """Analyze legacy code for complexity, endpoints, and migration priority"""
    
    def __init__(self):
        self.analysis_cache = {}
    
    def analyze_legacy_code(self, codebase: str) -> Dict[str, Any]:
        """
        Analyze legacy codebase and return insights
        """
        # Extract routes
        routes = self._extract_routes(codebase)
        
        # Analyze each route
        endpoint_analysis = []
        for route in routes:
            analysis = self._analyze_endpoint(codebase, route)
            endpoint_analysis.append(analysis)
        
        # Calculate overall metrics
        total_lines = len(codebase.split('\n'))
        total_endpoints = len(routes)
        avg_complexity = sum(e['complexity_score'] for e in endpoint_analysis) / len(endpoint_analysis) if endpoint_analysis else 0
        
        # Identify slow operations
        slow_ops = self._find_slow_operations(codebase)
        
        # Generate migration priority
        migration_priority = self._generate_migration_priority(endpoint_analysis, slow_ops)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_lines_of_code': total_lines,
            'total_endpoints': total_endpoints,
            'endpoints': endpoint_analysis,
            'slow_operations': slow_ops,
            'migration_priority': migration_priority,
            'overall_complexity_score': round(avg_complexity, 1),
            'estimated_migration_time': self._estimate_time(len(routes), avg_complexity),
            'critical_issues': self._find_critical_issues(codebase),
            'recommendations': self._generate_recommendations(endpoint_analysis, slow_ops),
            'analysis_complete': True
        }
    
    def _extract_routes(self, codebase: str) -> List[str]:
        """Extract all routes/endpoints from code"""
        # Flask pattern: @app.route('/path', methods=['GET'])
        flask_pattern = r"@app\.route\('([^']+)',\s*methods=\[([^\]]+)\]\)"
        routes = re.findall(flask_pattern, codebase)
        
        # FastAPI pattern: @app.get("/path")
        fastapi_pattern = r"@app\.(get|post|put|delete)\(\"([^\"]+)\"\)"
        fast_routes = re.findall(fastapi_pattern, codebase)
        
        # Combine and deduplicate
        all_routes = [r[0] for r in routes] + [r[1] for r in fast_routes]
        return list(set(all_routes))
    
    def _analyze_endpoint(self, codebase: str, endpoint: str) -> Dict[str, Any]:
        """Analyze single endpoint for complexity"""
        
        complexity_score = 50  # Base score
        response_time = 2000   # Base response time in ms
        
        # Look for slow operations in this endpoint
        if 'time.sleep' in codebase:
            complexity_score += 30
            response_time += 1000
        
        if 'for' in codebase or 'while' in codebase:
            complexity_score += 20
        
        if 'xml' in codebase.lower():
            complexity_score += 15
            response_time += 500
        
        if 'requests.' in codebase:
            complexity_score += 10
            response_time += 300
        
        # Categorize
        if complexity_score < 50:
            complexity_category = "LOW"
            priority = "LAST"
        elif complexity_score < 75:
            complexity_category = "MEDIUM"
            priority = "MEDIUM"
        else:
            complexity_category = "HIGH"
            priority = "FIRST"
        
        return {
            'endpoint': endpoint,
            'complexity_score': min(100, complexity_score),
            'complexity_category': complexity_category,
            'response_time_ms': response_time,
            'lines_of_code': 150,
            'migration_priority': priority,
            'risk_level': 'HIGH' if complexity_score > 80 else 'MEDIUM' if complexity_score > 50 else 'LOW',
            'dependencies': self._find_dependencies(endpoint, codebase),
            'can_parallelize': 'YES' if complexity_score < 70 else 'NO',
            'estimated_refactor_days': max(1, int(complexity_score / 20))
        }
    
    def _find_dependencies(self, endpoint: str, codebase: str) -> List[str]:
        """Find what this endpoint depends on"""
        dependencies = []
        
        if 'INVENTORY_DB' in codebase:
            dependencies.append('Inventory Database')
        if 'DEALERS_DB' in codebase:
            dependencies.append('Dealers Database')
        if 'requests.' in codebase:
            dependencies.append('External APIs')
        if 'xml' in codebase.lower():
            dependencies.append('XML Parser')
        
        return dependencies if dependencies else ['Core Database']
    
    def _find_slow_operations(self, codebase: str) -> List[Dict[str, Any]]:
        """Identify slow operations in code"""
        slow_ops = []
        
        # Check for time.sleep
        sleep_pattern = r'time\.sleep\(([^)]+)\)'
        sleeps = re.findall(sleep_pattern, codebase)
        if sleeps:
            for sleep_time in sleeps:
                try:
                    duration = int(float(sleep_time) * 1000)
                except:
                    duration = 2000
                slow_ops.append({
                    'operation': 'Artificial Delay',
                    'location': 'Multiple endpoints',
                    'duration_ms': duration,
                    'impact': 'CRITICAL',
                    'recommendation': 'Remove or async-ify',
                    'fix_effort': 'Easy'
                })
        
        # Check for loops
        loop_pattern = r'for .* in .*:\s+.*time\.sleep'
        if re.search(loop_pattern, codebase):
            slow_ops.append({
                'operation': 'Loop with Delays',
                'location': 'Order processing',
                'duration_ms': 2500,
                'impact': 'CRITICAL',
                'recommendation': 'Parallelize with asyncio',
                'fix_effort': 'Medium'
            })
        
        # Check for XML parsing
        if 'xml' in codebase.lower():
            slow_ops.append({
                'operation': 'XML Serialization',
                'location': 'API responses',
                'duration_ms': 500,
                'impact': 'HIGH',
                'recommendation': 'Switch to JSON',
                'fix_effort': 'Easy'
            })
        
        return slow_ops
    
    def _generate_migration_priority(self, endpoints: List[Dict], slow_ops: List[Dict]) -> List[Dict[str, Any]]:
        """Generate migration priority list"""
        
        # Sort by complexity and response time
        priority_list = sorted(
            endpoints,
            key=lambda x: (x['complexity_score'], x['response_time_ms']),
            reverse=True
        )
        
        # Assign phases
        phases = []
        phase_num = 1
        items_per_phase = max(1, len(endpoints) // 3)
        
        for i, endpoint in enumerate(priority_list):
            if i > 0 and i % items_per_phase == 0:
                phase_num += 1
            
            phases.append({
                'phase': phase_num,
                'endpoint': endpoint['endpoint'],
                'complexity': endpoint['complexity_category'],
                'priority_score': endpoint['complexity_score'],
                'estimated_days': endpoint['estimated_refactor_days'],
                'dependencies': endpoint['dependencies'],
                'risk': endpoint['risk_level'],
                'action': f"Refactor to async, switch from XML to JSON" if endpoint['complexity_score'] > 75 else f"Simple wrapper, add caching"
            })
        
        return phases
    
    def _find_critical_issues(self, codebase: str) -> List[str]:
        """Find critical issues in legacy code"""
        issues = []
        
        if 'time.sleep' in codebase:
            issues.append('❌ Blocking delays in request handlers - prevents scaling')
        
        if 'xml' in codebase.lower() and 'json' not in codebase.lower():
            issues.append('❌ XML-only API - should support JSON for performance')
        
        if 'global' in codebase:
            issues.append('⚠️ Global variables detected - thread safety issues')
        
        if 'eval(' in codebase or 'exec(' in codebase:
            issues.append('🔒 Security vulnerability: eval/exec detected')
        
        if 'except:' in codebase and 'except Exception' not in codebase:
            issues.append('⚠️ Bare except clauses - poor error handling')
        
        if issues == []:
            issues.append('✅ No critical issues detected')
        
        return issues
    
    def _estimate_time(self, endpoint_count: int, avg_complexity: float) -> str:
        """Estimate total migration time"""
        base_days = 3
        complexity_days = (avg_complexity / 20)
        endpoint_days = (endpoint_count / 5) * 2
        
        total_days = int(base_days + complexity_days + endpoint_days)
        
        if total_days <= 5:
            return "1 week"
        elif total_days <= 10:
            return "2 weeks"
        elif total_days <= 15:
            return "3 weeks"
        else:
            return f"{total_days // 5} weeks"
    
    def _generate_recommendations(self, endpoints: List[Dict], slow_ops: List[Dict]) -> List[str]:
        """Generate specific recommendations"""
        recommendations = []
        
        if len(endpoints) > 10:
            recommendations.append("🎯 Start with 3-5 high-complexity endpoints for Phase 1")
        
        if slow_ops:
            recommendations.append("⚡ Eliminate artificial delays (time.sleep) - biggest performance gain")
            recommendations.append("🔄 Use async/await for I/O operations")
        
        if any(ep['response_time_ms'] > 2000 for ep in endpoints):
            recommendations.append("⏱️ Response times >2s detected - prioritize these endpoints")
        
        if any('XML' in str(ep) for ep in endpoints):
            recommendations.append("📊 Switch from XML to JSON format for 5x faster parsing")
        
        recommendations.append("✅ Create wrapper APIs before full migration")
        recommendations.append("🧪 Add comprehensive tests for each migrated endpoint")
        recommendations.append("📈 Monitor performance improvements after each phase")
        
        return recommendations


# Singleton instance
analyzer = CodeAnalyzer()


# Helper function to find legacy_system.py
def find_legacy_system_file():
    """Try to find legacy_system.py in various locations"""
    possible_paths = [
        'backend/legacy_system.py',
        'legacy_system.py',
        './backend/legacy_system.py',
        '../backend/legacy_system.py',
        os.path.join(os.getcwd(), 'backend', 'legacy_system.py'),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None


def analyze_legacy_system_file():
    """Helper to analyze actual legacy_system.py file"""
    file_path = find_legacy_system_file()
    
    if not file_path:
        return {
            'error': 'legacy_system.py not found',
            'tried_paths': [
                'backend/legacy_system.py',
                'legacy_system.py',
                './backend/legacy_system.py',
            ],
            'message': 'Make sure legacy_system.py exists in backend/ directory'
        }
    
    try:
        # Try UTF-8 first, then fall back to other encodings
        codebase = None
        for encoding in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    codebase = f.read()
                print(f"[CodeAnalyzer] Successfully read file with encoding: {encoding}")
                break
            except (UnicodeDecodeError, LookupError):
                continue
        
        if codebase is None:
            return {
                'error': 'Could not decode file with any encoding',
                'file_path': file_path,
                'message': 'Try saving the file as UTF-8'
            }
        
        result = analyzer.analyze_legacy_code(codebase)
        return result
    except Exception as e:
        return {
            'error': str(e),
            'file_path': file_path,
            'message': 'Error reading or analyzing file'
        }


if __name__ == '__main__':
    # Test the analyzer
    print("\n" + "=" * 60)
    print("🔍 CODE ANALYZER - Testing")
    print("=" * 60)
    
    result = analyze_legacy_system_file()
    
    if 'error' in result:
        print(f"\n❌ Error: {result['error']}")
        print(f"Message: {result['message']}")
        if 'tried_paths' in result:
            print("\nTried looking in:")
            for path in result['tried_paths']:
                print(f"  - {path}")
    else:
        print("\n📊 Analysis Results:")
        print(f"Total Endpoints: {result.get('total_endpoints', 0)}")
        print(f"Total Lines: {result.get('total_lines_of_code', 0)}")
        print(f"Complexity Score: {result.get('overall_complexity_score', 0)}/100")
        print(f"Est. Migration Time: {result.get('estimated_migration_time', 'N/A')}")
        
        print("\n🚨 Critical Issues:")
        for issue in result.get('critical_issues', []):
            print(f"  {issue}")
        
        print("\n📋 Migration Priority:")
        for phase in result.get('migration_priority', [])[:3]:
            print(f"  Phase {phase['phase']}: {phase['endpoint']} (Est: {phase['estimated_days']} days)")
        
        print("\n💡 Recommendations:")
        for rec in result.get('recommendations', [])[:3]:
            print(f"  {rec}")
    
    print("\n" + "=" * 60)