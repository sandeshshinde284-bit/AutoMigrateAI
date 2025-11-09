# ============================================
# FEATURE #7: Digital Twin Validator
# File: backend/digital_twin.py
# Purpose: Simulate migration at target percentage
# ============================================

import random
import time
from datetime import datetime
from typing import Dict, Any, List

class DigitalTwinValidator:
    """Simulate migration scenarios to test safety before going live"""
    
    def __init__(self):
        self.validation_history = []
    
    def validate_migration(self, target_percentage: int, duration_seconds: int = 30, traffic_volume: int = 100) -> Dict[str, Any]:
        """
        Simulate migration at target percentage and test for issues
        
        Args:
            target_percentage: What % of traffic to route to cloud (0-100)
            duration_seconds: How long to simulate (seconds)
            traffic_volume: Number of requests to simulate
        """
        
        print(f"\n[DigitalTwin] Starting validation at {target_percentage}% migration")
        print(f"[DigitalTwin] Duration: {duration_seconds}s, Traffic: {traffic_volume} requests")
        
        # Simulate the migration
        simulation_results = self._run_simulation(target_percentage, traffic_volume)
        
        # Analyze results
        analysis = self._analyze_results(simulation_results, target_percentage)
        
        # Store in history
        validation_record = {
            'timestamp': datetime.now().isoformat(),
            'target_percentage': target_percentage,
            'duration': duration_seconds,
            'traffic_volume': traffic_volume,
            'results': simulation_results,
            'analysis': analysis
        }
        self.validation_history.append(validation_record)
        
        print(f"[DigitalTwin] Validation complete - Score: {analysis['validation_score']}/100")
        
        return {
            'timestamp': datetime.now().isoformat(),
            'target_percentage': target_percentage,
            'duration_seconds': duration_seconds,
            'traffic_volume': traffic_volume,
            'simulation_results': simulation_results,
            'analysis': analysis,
            'recommendation': self._get_recommendation(analysis),
            'validation_complete': True
        }
    
    def _run_simulation(self, target_percentage: int, traffic_volume: int) -> Dict[str, Any]:
        """Simulate traffic routing at target percentage"""
        
        legacy_requests = []
        cloud_requests = []
        errors = []
        
        for i in range(traffic_volume):
            # Randomly route based on target percentage
            use_cloud = random.random() * 100 < target_percentage
            
            if use_cloud:
                # Simulate cloud response
                response_time = random.uniform(50, 150)  # Cloud: fast (50-150ms)
                status = 'SUCCESS' if random.random() > 0.02 else 'ERROR'  # 2% error rate
                cloud_requests.append({
                    'id': i,
                    'response_time': response_time,
                    'status': status
                })
                if status == 'ERROR':
                    errors.append({
                        'type': 'Cloud Error',
                        'request_id': i,
                        'message': 'Timeout or service unavailable'
                    })
            else:
                # Simulate legacy response
                response_time = random.uniform(2000, 3500)  # Legacy: slow (2-3.5s)
                status = 'SUCCESS' if random.random() > 0.05 else 'ERROR'  # 5% error rate
                legacy_requests.append({
                    'id': i,
                    'response_time': response_time,
                    'status': status
                })
                if status == 'ERROR':
                    errors.append({
                        'type': 'Legacy Error',
                        'request_id': i,
                        'message': 'Database timeout or lock'
                    })
        
        # Calculate metrics
        cloud_times = [r['response_time'] for r in cloud_requests]
        legacy_times = [r['response_time'] for r in legacy_requests]
        
        cloud_avg = sum(cloud_times) / len(cloud_times) if cloud_times else 0
        legacy_avg = sum(legacy_times) / len(legacy_times) if legacy_times else 0
        
        cloud_success = len([r for r in cloud_requests if r['status'] == 'SUCCESS'])
        legacy_success = len([r for r in legacy_requests if r['status'] == 'SUCCESS'])
        
        return {
            'legacy_requests_count': len(legacy_requests),
            'cloud_requests_count': len(cloud_requests),
            'legacy_avg_response_time': round(legacy_avg, 2),
            'cloud_avg_response_time': round(cloud_avg, 2),
            'legacy_success_rate': round((legacy_success / len(legacy_requests) * 100) if legacy_requests else 100, 1),
            'cloud_success_rate': round((cloud_success / len(cloud_requests) * 100) if cloud_requests else 100, 1),
            'total_errors': len(errors),
            'error_rate': round((len(errors) / traffic_volume * 100), 2),
            'peak_response_time': max(cloud_times + legacy_times) if (cloud_times + legacy_times) else 0,
            'min_response_time': min(cloud_times + legacy_times) if (cloud_times + legacy_times) else 0,
            'errors': errors[:5]  # Show first 5 errors
        }
    
    def _analyze_results(self, results: Dict[str, Any], target_percentage: int) -> Dict[str, Any]:
        """Analyze simulation results and generate recommendations"""
        
        validation_score = 100  # Start at perfect
        issues = []
        warnings = []
        
        # Check error rate
        if results['error_rate'] > 5:
            validation_score -= 20
            issues.append(f"High error rate: {results['error_rate']}% (threshold: 5%)")
        elif results['error_rate'] > 3:
            validation_score -= 10
            warnings.append(f"Elevated error rate: {results['error_rate']}%")
        
        # Check response times
        if results['peak_response_time'] > 5000:
            validation_score -= 15
            issues.append(f"Peak response time too high: {results['peak_response_time']}ms")
        elif results['peak_response_time'] > 3000:
            validation_score -= 5
            warnings.append(f"Some slow responses detected: {results['peak_response_time']}ms")
        
        # Check cloud success rate
        if results['cloud_success_rate'] < 95:
            validation_score -= 15
            issues.append(f"Cloud success rate low: {results['cloud_success_rate']}%")
        
        # Check legacy success rate
        if results['legacy_success_rate'] < 95:
            validation_score -= 10
            issues.append(f"Legacy success rate low: {results['legacy_success_rate']}%")
        
        # Check balance at target percentage
        if target_percentage > 50:
            expected_cloud = results['cloud_requests_count'] / (results['cloud_requests_count'] + results['legacy_requests_count'])
            if abs(expected_cloud - target_percentage/100) > 0.15:
                warnings.append("Traffic not evenly distributed - retry test")
        
        # Ensure minimum score
        validation_score = max(0, validation_score)
        
        return {
            'validation_score': validation_score,
            'passed': validation_score >= 75,
            'issues': issues,
            'warnings': warnings,
            'confidence_level': 'HIGH' if validation_score >= 90 else 'MEDIUM' if validation_score >= 75 else 'LOW',
            'performance_improvement': round((results['legacy_avg_response_time'] / results['cloud_avg_response_time']) if results['cloud_avg_response_time'] > 0 else 0, 1)
        }
    
    def _get_recommendation(self, analysis: Dict[str, Any]) -> str:
        """Generate recommendation based on analysis"""
        
        if analysis['validation_score'] >= 90:
            return "✅ SAFE TO PROCEED - All metrics excellent. Can increase traffic to next level."
        elif analysis['validation_score'] >= 75:
            return "⚠️ CAUTIOUS PROCEED - Some minor issues detected. Monitor closely. Can proceed with caution."
        elif analysis['validation_score'] >= 50:
            return "🛑 NOT RECOMMENDED - Multiple issues detected. Fix critical issues before proceeding."
        else:
            return "❌ DO NOT PROCEED - Serious issues detected. Rollback and investigate."
    
    def get_validation_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent validation runs"""
        return list(reversed(self.validation_history[-limit:]))
    
    def get_safe_next_percentage(self, current_percentage: int) -> Dict[str, Any]:
        """Recommend next migration percentage"""
        
        if current_percentage >= 100:
            return {
                'current': current_percentage,
                'recommendation': 'Migration complete!',
                'next_percentage': None,
                'reason': 'Already at 100%'
            }
        
        # Calculate next step based on current
        step_size = 10
        next_percentage = min(100, current_percentage + step_size)
        
        return {
            'current': current_percentage,
            'recommended_next': next_percentage,
            'step_size': step_size,
            'reason': f'Gradual migration: increase by {step_size}% steps',
            'estimated_time_to_completion': f"{(100 - current_percentage) // step_size} more steps"
        }


# Singleton instance
digital_twin = DigitalTwinValidator()


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🧪 DIGITAL TWIN VALIDATOR - Testing")
    print("=" * 60)
    
    # Test at different percentages
    for percentage in [25, 50, 75, 100]:
        result = digital_twin.validate_migration(percentage, traffic_volume=100)
        
        print(f"\n📊 Results for {percentage}% migration:")
        print(f"  Score: {result['analysis']['validation_score']}/100")
        print(f"  Recommendation: {result['recommendation']}")
        print(f"  Issues: {len(result['analysis']['issues'])}")
        print(f"  Warnings: {len(result['analysis']['warnings'])}")
    
    print("\n" + "=" * 60)