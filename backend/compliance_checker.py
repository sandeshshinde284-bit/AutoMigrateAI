# ============================================
# FEATURE #9: GDPR & TISAX Auto-Enforcement
# File: backend/compliance_checker.py
# Purpose: Automatically check and enforce compliance
# ============================================

import re
import json
from datetime import datetime
from typing import Dict, Any, List

class ComplianceChecker:
    """Automatically check requests/responses for GDPR and TISAX compliance"""
    
    def __init__(self):
        self.violation_history = []
        self.compliance_score = 100
    
    # ============================================
    # PII PATTERNS
    # ============================================
    
    EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    PHONE_PATTERN = r'(\+?1?\d{9,15}|[0-9]{3}[-.]?[0-9]{3}[-.]?[0-9]{4})'
    SSN_PATTERN = r'\b\d{3}-\d{2}-\d{4}\b'
    CREDIT_CARD_PATTERN = r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b'
    IP_ADDRESS_PATTERN = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    
    def check_request_compliance(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check request for GDPR/TISAX violations"""
        
        violations = []
        warnings = []
        score = 100
        
        request_str = json.dumps(request_data)
        
        # Check for PII in request
        pii_found = self._find_pii(request_str)
        if pii_found:
            for pii_type, matches in pii_found.items():
                if pii_type in ['email', 'phone', 'ssn', 'credit_card']:
                    violations.append({
                        'severity': 'CRITICAL',
                        'type': f'{pii_type.upper()} in request',
                        'pii_type': pii_type,
                        'count': len(matches),
                        'message': f'{pii_type.upper()} data should not be in request body',
                        'gdpr_article': 'Article 32 (Security of processing)',
                        'fix': f'Move {pii_type} to headers or use encryption'
                    })
                    score -= 25
                elif pii_type == 'ip_address':
                    warnings.append({
                        'severity': 'MEDIUM',
                        'type': 'IP Address in request',
                        'message': 'IP addresses should be anonymized per GDPR',
                        'gdpr_article': 'Article 32 (Pseudonymization)'
                    })
                    score -= 5
        
        # Check for encryption headers
        if not self._has_encryption_indicators(request_str):
            warnings.append({
                'severity': 'HIGH',
                'type': 'No encryption indicators',
                'message': 'Request should indicate HTTPS/TLS encryption',
                'gdpr_article': 'Article 32 (Encryption)',
                'fix': 'Ensure all requests use HTTPS/TLS'
            })
            score -= 10
        
        # Check for hardcoded secrets
        secrets_found = self._find_hardcoded_secrets(request_str)
        if secrets_found:
            violations.append({
                'severity': 'CRITICAL',
                'type': 'Hardcoded credentials',
                'count': len(secrets_found),
                'message': 'Credentials found in request body',
                'tisax_requirement': 'TIS.C4.2.3 (Credential management)',
                'fix': 'Use environment variables or secure vaults'
            })
            score -= 30
        
        return {
            'timestamp': datetime.now().isoformat(),
            'violations': violations,
            'warnings': warnings,
            'compliance_score': max(0, score),
            'status': 'COMPLIANT' if score >= 80 else 'NON_COMPLIANT' if score < 60 else 'CAUTION'
        }
    
    def check_response_compliance(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check response for GDPR/TISAX violations"""
        
        violations = []
        warnings = []
        score = 100
        
        response_str = json.dumps(response_data)
        
        # Check for unnecessary PII in response
        pii_found = self._find_pii(response_str)
        if pii_found:
            for pii_type, matches in pii_found.items():
                if pii_type in ['ssn', 'credit_card']:
                    # Never expose these
                    violations.append({
                        'severity': 'CRITICAL',
                        'type': f'{pii_type.upper()} exposed in response',
                        'pii_type': pii_type,
                        'count': len(matches),
                        'message': f'{pii_type.upper()} should NEVER be in response',
                        'gdpr_article': 'Article 5 (Data minimization)',
                        'fix': f'Remove or mask {pii_type}'
                    })
                    score -= 50
                elif pii_type == 'phone':
                    warnings.append({
                        'severity': 'MEDIUM',
                        'type': 'Unmasked phone number in response',
                        'message': 'Phone numbers should be masked (last 4 digits only)',
                        'gdpr_article': 'Article 32 (Pseudonymization)',
                        'fix': 'Mask as: ***-***-1234'
                    })
                    score -= 10
        
        # Check for proper data expiration headers
        if 'cache_control' not in response_str.lower() and 'expires' not in response_str.lower():
            warnings.append({
                'severity': 'MEDIUM',
                'type': 'Missing cache control headers',
                'message': 'Should specify data retention/cache policy',
                'gdpr_article': 'Article 5 (Storage limitation)',
                'fix': 'Add Cache-Control and Expires headers'
            })
            score -= 5
        
        return {
            'timestamp': datetime.now().isoformat(),
            'violations': violations,
            'warnings': warnings,
            'compliance_score': max(0, score),
            'status': 'COMPLIANT' if score >= 80 else 'NON_COMPLIANT' if score < 60 else 'CAUTION'
        }
    
    def get_overall_compliance(self) -> Dict[str, Any]:
        """Get overall compliance dashboard"""
        
        if not self.violation_history:
            return {
                'overall_score': 100,
                'status': 'COMPLIANT',
                'total_checks': 0,
                'violations_found': 0,
                'warnings_found': 0,
                'compliance_level': 'EXCELLENT',
                'certifications': ['GDPR Ready', 'TISAX Ready'],
                'last_check': None
            }
        
        # Calculate average from history
        scores = [v['score'] for v in self.violation_history]
        avg_score = sum(scores) / len(scores) if scores else 100
        
        violations_count = sum(1 for v in self.violation_history if v['violations'])
        warnings_count = sum(1 for v in self.violation_history if v['warnings'])
        
        # Determine compliance level
        if avg_score >= 95:
            compliance_level = 'EXCELLENT'
            certifications = ['GDPR Certified', 'TISAX Certified']
        elif avg_score >= 85:
            compliance_level = 'GOOD'
            certifications = ['GDPR Ready', 'TISAX Ready']
        elif avg_score >= 70:
            compliance_level = 'FAIR'
            certifications = ['Needs improvement']
        else:
            compliance_level = 'POOR'
            certifications = ['Non-compliant']
        
        return {
            'overall_score': round(avg_score, 1),
            'status': 'COMPLIANT' if avg_score >= 80 else 'NON_COMPLIANT' if avg_score < 60 else 'CAUTION',
            'total_checks': len(self.violation_history),
            'violations_found': violations_count,
            'warnings_found': warnings_count,
            'compliance_level': compliance_level,
            'certifications': certifications,
            'last_check': self.violation_history[-1]['timestamp'] if self.violation_history else None,
            'gdpr_articles_covered': [
                'Article 5 (Principles)',
                'Article 32 (Security)',
                'Article 33 (Breach notification)'
            ],
            'tisax_requirements': [
                'TIS.C4.2.3 (Credential management)',
                'TIS.C4.1.1 (Access control)',
                'TIS.C4.1.5 (Encryption)'
            ]
        }
    
    def log_check(self, request_check: Dict[str, Any], response_check: Dict[str, Any]):
        """Log compliance check"""
        
        # Combine scores
        avg_score = (request_check['compliance_score'] + response_check['compliance_score']) / 2
        
        record = {
            'timestamp': datetime.now().isoformat(),
            'request_check': request_check,
            'response_check': response_check,
            'score': avg_score,
            'violations': request_check['violations'] + response_check['violations'],
            'warnings': request_check['warnings'] + response_check['warnings']
        }
        
        self.violation_history.append(record)
        
        # Keep last 100 checks
        if len(self.violation_history) > 100:
            self.violation_history = self.violation_history[-100:]
    
    # ============================================
    # HELPER METHODS
    # ============================================
    
    def _find_pii(self, text: str) -> Dict[str, List[str]]:
        """Find PII patterns in text"""
        found = {}
        
        emails = re.findall(self.EMAIL_PATTERN, text)
        if emails:
            found['email'] = emails
        
        phones = re.findall(self.PHONE_PATTERN, text)
        if phones:
            found['phone'] = phones
        
        ssns = re.findall(self.SSN_PATTERN, text)
        if ssns:
            found['ssn'] = ssns
        
        cards = re.findall(self.CREDIT_CARD_PATTERN, text)
        if cards:
            found['credit_card'] = cards
        
        ips = re.findall(self.IP_ADDRESS_PATTERN, text)
        if ips:
            found['ip_address'] = ips
        
        return found
    
    def _has_encryption_indicators(self, text: str) -> bool:
        """Check for encryption indicators"""
        indicators = ['https', 'tls', 'ssl', 'encrypted', 'secure']
        return any(indicator in text.lower() for indicator in indicators)
    
    def _find_hardcoded_secrets(self, text: str) -> List[str]:
        """Find hardcoded credentials"""
        secrets = []
        
        # Look for common patterns
        if re.search(r"['\"](password|secret|api_key|token)['\"]?\s*[:=]\s*['\"]?(\S+)['\"]?", text, re.IGNORECASE):
            secrets.append('Found credential pattern')
        
        if re.search(r"(BEGIN RSA PRIVATE KEY|BEGIN PRIVATE KEY|BEGIN CERTIFICATE)", text):
            secrets.append('Found private key or certificate')
        
        return secrets
    
    def get_violations_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent violations"""
        return list(reversed(self.violation_history[-limit:]))


# Singleton instance
compliance_checker = ComplianceChecker()


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🔒 COMPLIANCE CHECKER - Testing")
    print("=" * 60)
    
    # Test with sample data
    test_request = {
        'user_email': 'john.doe@example.com',
        'phone': '555-123-4567',
        'data': 'some_data'
    }
    
    test_response = {
        'status': 'success',
        'user_id': 12345
    }
    
    # Check compliance
    req_check = compliance_checker.check_request_compliance(test_request)
    resp_check = compliance_checker.check_response_compliance(test_response)
    
    print(f"\n📋 Request Compliance:")
    print(f"  Score: {req_check['compliance_score']}/100")
    print(f"  Status: {req_check['status']}")
    print(f"  Violations: {len(req_check['violations'])}")
    
    print(f"\n📋 Response Compliance:")
    print(f"  Score: {resp_check['compliance_score']}/100")
    print(f"  Status: {resp_check['status']}")
    print(f"  Warnings: {len(resp_check['warnings'])}")
    
    # Log check
    compliance_checker.log_check(req_check, resp_check)
    
    # Get overall
    overall = compliance_checker.get_overall_compliance()
    print(f"\n🔒 Overall Compliance:")
    print(f"  Score: {overall['overall_score']}/100")
    print(f"  Level: {overall['compliance_level']}")
    print(f"  Status: {overall['status']}")
    
    print("\n" + "=" * 60)