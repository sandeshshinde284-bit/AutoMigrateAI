<template>
  <div class="section">
    <div class="page-title">
      <i class="ri-shield-check-line"></i>
      <h1>GDPR & TISAX Compliance</h1>
    </div>

    <!-- Overall Compliance Badge -->
    <div class="section-card compliance-header">
      <div
        class="compliance-score"
        :class="[getComplianceClass(compliance.overall_score)]"
      >
        <div class="score-number">{{ compliance.overall_score }}</div>
        <div class="score-max">/100</div>
      </div>

      <div class="compliance-info">
        <h2>{{ compliance.compliance_level }} Compliance</h2>
        <p class="compliance-status" :class="compliance.status.toLowerCase()">
          {{
            compliance.status === "COMPLIANT"
              ? "✅ COMPLIANT"
              : compliance.status === "NON_COMPLIANT"
              ? "❌ NON-COMPLIANT"
              : "⚠️ CAUTION"
          }}
        </p>
        <div class="certifications">
          <span
            v-for="cert in compliance.certifications"
            :key="cert"
            class="cert-badge"
          >
            {{ cert }}
          </span>
        </div>
      </div>

      <div class="compliance-stats">
        <div class="stat">
          <div class="stat-label">Checks</div>
          <div class="stat-value">{{ compliance.total_checks }}</div>
        </div>
        <div class="stat">
          <div class="stat-label">Violations</div>
          <div class="stat-value danger">{{ compliance.violations_found }}</div>
        </div>
        <div class="stat">
          <div class="stat-label">Warnings</div>
          <div class="stat-value warning">{{ compliance.warnings_found }}</div>
        </div>
      </div>
    </div>

    <!-- GDPR Coverage -->
    <div class="section-card">
      <div class="section-title">
        <i class="ri-checkbox-circle-line"></i>
        GDPR Articles Covered
      </div>
      <div class="articles-grid">
        <div
          v-for="article in compliance.gdpr_articles_covered"
          :key="article"
          class="article-item"
        >
          <i class="ri-check-double-line"></i>
          {{ article }}
        </div>
      </div>
    </div>

    <!-- TISAX Requirements -->
    <div class="section-card">
      <div class="section-title">
        <i class="ri-shield-line"></i>
        TISAX Requirements Implemented
      </div>
      <div class="requirements-grid">
        <div
          v-for="req in compliance.tisax_requirements"
          :key="req"
          class="requirement-item"
        >
          <i class="ri-check-double-line"></i>
          {{ req }}
        </div>
      </div>
    </div>

    <!-- Real-time Check -->
    <div class="section-card">
      <div class="section-title">
        <i class="ri-search-check-line"></i>
        Real-time Compliance Monitoring
      </div>

      <div class="check-controls">
        <button
          @click="runComplianceCheck"
          :disabled="checking"
          class="btn btn-check"
        >
          <i class="ri-play-line"></i>
          {{ checking ? "Checking..." : "RUN COMPLIANCE CHECK" }}
        </button>
      </div>

      <div v-if="checking" class="loading">
        <div class="loader"></div>
        <p>Scanning for PII, encryption, and credentials...</p>
      </div>

      <!-- Request Check Results -->
      <div v-if="lastCheck && !checking" class="check-results">
        <div class="check-section">
          <h4>Request Scan</h4>
          <div
            class="compliance-badge"
            :class="lastCheck.request_compliance.status.toLowerCase()"
          >
            Score: {{ lastCheck.request_compliance.compliance_score }}/100
          </div>

          <div
            v-if="lastCheck.request_compliance.violations.length > 0"
            class="violations-box"
          >
            <div class="violations-title">🔴 Violations Found:</div>
            <div
              v-for="(v, idx) in lastCheck.request_compliance.violations"
              :key="`req-v-${idx}`"
              class="violation-item critical"
            >
              <strong>{{ v.type }}</strong>
              <p>{{ v.message }}</p>
              <p class="fix">Fix: {{ v.fix || "N/A" }}</p>
            </div>
          </div>

          <div
            v-if="lastCheck.request_compliance.warnings.length > 0"
            class="warnings-box"
          >
            <div class="warnings-title">🟡 Warnings:</div>
            <div
              v-for="(w, idx) in lastCheck.request_compliance.warnings"
              :key="`req-w-${idx}`"
              class="warning-item"
            >
              <strong>{{ w.type }}</strong>
              <p>{{ w.message }}</p>
            </div>
          </div>

          <div
            v-if="
              lastCheck.request_compliance.violations.length === 0 &&
              lastCheck.request_compliance.warnings.length === 0
            "
            class="pass-box"
          >
            ✅ Request is compliant
          </div>
        </div>

        <!-- Response Check Results -->
        <div class="check-section">
          <h4>Response Scan</h4>
          <div
            class="compliance-badge"
            :class="lastCheck.response_compliance.status.toLowerCase()"
          >
            Score: {{ lastCheck.response_compliance.compliance_score }}/100
          </div>

          <div
            v-if="lastCheck.response_compliance.violations.length > 0"
            class="violations-box"
          >
            <div class="violations-title">🔴 Violations Found:</div>
            <div
              v-for="(v, idx) in lastCheck.response_compliance.violations"
              :key="`resp-v-${idx}`"
              class="violation-item critical"
            >
              <strong>{{ v.type }}</strong>
              <p>{{ v.message }}</p>
              <p class="fix">Fix: {{ v.fix || "N/A" }}</p>
            </div>
          </div>

          <div
            v-if="lastCheck.response_compliance.warnings.length > 0"
            class="warnings-box"
          >
            <div class="warnings-title">🟡 Warnings:</div>
            <div
              v-for="(w, idx) in lastCheck.response_compliance.warnings"
              :key="`resp-w-${idx}`"
              class="warning-item"
            >
              <strong>{{ w.type }}</strong>
              <p>{{ w.message }}</p>
            </div>
          </div>

          <div
            v-if="
              lastCheck.response_compliance.violations.length === 0 &&
              lastCheck.response_compliance.warnings.length === 0
            "
            class="pass-box"
          >
            ✅ Response is compliant
          </div>
        </div>
      </div>
    </div>

    <!-- Data Protection Features -->
    <div class="section-card features-card">
      <div class="section-title">
        <i class="ri-shield-star-line"></i>
        Automatic Data Protection
      </div>
      <div class="features-list">
        <div class="feature-item">
          <i class="ri-check-line"></i>
          <div>
            <strong>PII Detection</strong>
            <p>
              Automatically detects emails, phone numbers, SSNs, credit cards,
              and IP addresses
            </p>
          </div>
        </div>
        <div class="feature-item">
          <i class="ri-check-line"></i>
          <div>
            <strong>Encryption Monitoring</strong>
            <p>Verifies HTTPS/TLS encryption on all requests and responses</p>
          </div>
        </div>
        <div class="feature-item">
          <i class="ri-check-line"></i>
          <div>
            <strong>Credential Scanning</strong>
            <p>Detects hardcoded API keys, tokens, and private keys</p>
          </div>
        </div>
        <div class="feature-item">
          <i class="ri-check-line"></i>
          <div>
            <strong>Violation Logging</strong>
            <p>Records all compliance checks for audit trails</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Info -->
    <div class="section-card info-card">
      <p>
        <i class="ri-information-line"></i>
        All compliance data is monitored in real-time. Violations trigger
        automatic alerts and prevent data exposure.
      </p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { apiService } from "../services/api.ts";

interface ComplianceStatus {
  overall_score: number;
  status: string;
  compliance_level: string;
  total_checks: number;
  violations_found: number;
  warnings_found: number;
  certifications: string[];
  gdpr_articles_covered: string[];
  tisax_requirements: string[];
}

export default defineComponent({
  name: "ComplianceCard",
  data() {
    return {
      compliance: {
        overall_score: 0,
        status: "LOADING",
        compliance_level: "LOADING",
        total_checks: 0,
        violations_found: 0,
        warnings_found: 0,
        certifications: [],
        gdpr_articles_covered: [],
        tisax_requirements: [],
      } as ComplianceStatus,
      lastCheck: null as any,
      checking: false,
      refreshInterval: null as ReturnType<typeof setInterval> | null,
    };
  },
  methods: {
    async fetchComplianceStatus() {
      try {
        // const response = await fetch(
        //   "http://localhost:8000/proxy/compliance/status"
        // );
        // const data = await response.json();
        const data = await apiService.fetchComplianceStatus();
        if (data.success) {
          this.compliance = data.compliance;
        }
      } catch (error) {
        console.error("[Compliance] Error fetching status:", error);
      }
    },
    async runComplianceCheck() {
      this.checking = true;

      try {
        // Simulate a check with sample data
        const testRequest = {
          user_email: "john@example.com",
          phone: "555-123-4567",
        };

        const testResponse = {
          status: "success",
          user_id: 12345,
        };

        // const response = await fetch(
        //   "http://localhost:8000/proxy/compliance/check",
        //   {
        //     method: "POST",
        //     headers: { "Content-Type": "application/json" },
        //     body: JSON.stringify({
        //       request: testRequest,
        //       response: testResponse,
        //     }),
        //   }
        // );

        // const data = await response.json();
        const data = await apiService.runComplianceCheck(
          testRequest,
          testResponse
        );

        if (data.success) {
          this.lastCheck = data;
          console.log("[Compliance] Check complete:", data);
          // Refresh overall status
          setTimeout(() => this.fetchComplianceStatus(), 500);
        }
      } catch (error) {
        console.error("[Compliance] Error:", error);
      } finally {
        this.checking = false;
      }
    },
    getComplianceClass(score: number): string {
      if (score >= 90) return "excellent";
      if (score >= 70) return "good";
      if (score >= 50) return "fair";
      return "poor";
    },
  },
  mounted() {
    console.log("[ComplianceCard] Mounted");
    this.fetchComplianceStatus();

    this.refreshInterval = setInterval(() => {
      this.fetchComplianceStatus();
    }, 3000);
  },
  beforeUnmount() {
    if (this.refreshInterval) clearInterval(this.refreshInterval);
  },
});
</script>

<style scoped>
.section {
  space: 24px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 30px;
}

.page-title h1 {
  font-size: 28px;
  font-weight: bold;
  color: #001e50;
}

.page-title i {
  font-size: 28px;
  color: #00d4ff;
}

.section-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  border: 1px solid #e8eef5;
}

.compliance-header {
  display: flex;
  align-items: center;
  gap: 40px;
  background: linear-gradient(135deg, #f0fff4, #f0f9ff);
  border-left: 4px solid #51cf66;
}

.compliance-score {
  width: 120px;
  height: 120px;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
}

.compliance-score.excellent {
  background: linear-gradient(135deg, #51cf66, #69db7c);
}

.compliance-score.good {
  background: linear-gradient(135deg, #00d4ff, #0099cc);
}

.compliance-score.fair {
  background: linear-gradient(135deg, #ff9944, #ffb366);
}

.compliance-score.poor {
  background: linear-gradient(135deg, #ff6b6b, #ff8a9b);
}

.score-number {
  font-size: 40px;
}

.score-max {
  font-size: 14px;
  opacity: 0.9;
}

.compliance-info {
  flex: 1;
}

.compliance-info h2 {
  margin: 0 0 8px 0;
  color: #001e50;
  font-size: 20px;
}

.compliance-status {
  margin: 0 0 12px 0;
  font-size: 14px;
  font-weight: bold;
}

.compliance-status.compliant {
  color: #51cf66;
}

.compliance-status.non_compliant {
  color: #ff6b6b;
}

.compliance-status.caution {
  color: #ff9944;
}

.certifications {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.cert-badge {
  display: inline-block;
  background: rgba(81, 207, 102, 0.2);
  color: #51cf66;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: bold;
}

.compliance-stats {
  display: flex;
  gap: 20px;
}

.stat {
  text-align: center;
}

.stat-label {
  font-size: 12px;
  color: #999;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #001e50;
}

.stat-value.danger {
  color: #ff6b6b;
}

.stat-value.warning {
  color: #ff9944;
}

.section-title {
  font-size: 16px;
  font-weight: bold;
  color: #001e50;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.section-title i {
  color: #00d4ff;
  font-size: 18px;
}

.articles-grid,
.requirements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 12px;
}

.article-item,
.requirement-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 6px;
  border-left: 3px solid #51cf66;
}

.article-item i,
.requirement-item i {
  color: #51cf66;
  font-weight: bold;
  font-size: 18px;
}

.check-controls {
  margin-bottom: 20px;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-check {
  background: linear-gradient(135deg, #00d4ff, #0099cc);
  color: white;
  width: 100%;
  justify-content: center;
}

.btn-check:hover:not(:disabled) {
  box-shadow: 0 4px 12px rgba(0, 212, 255, 0.3);
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 30px;
  background: #f8f9fa;
  border-radius: 8px;
}

.loader {
  width: 40px;
  height: 40px;
  border: 3px solid #e8eef5;
  border-top-color: #00d4ff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.check-results {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.check-section {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
}

.check-section h4 {
  margin: 0 0 12px 0;
  color: #001e50;
  font-size: 14px;
}

.compliance-badge {
  display: inline-block;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: bold;
  margin-bottom: 12px;
}

.compliance-badge.compliant {
  background: rgba(81, 207, 102, 0.2);
  color: #51cf66;
}

.compliance-badge.non_compliant {
  background: rgba(255, 107, 107, 0.2);
  color: #ff6b6b;
}

.compliance-badge.caution {
  background: rgba(255, 153, 68, 0.2);
  color: #ff9944;
}

.violations-box,
.warnings-box {
  margin-bottom: 12px;
  padding: 12px;
  background: white;
  border-radius: 6px;
  border-left: 3px solid;
}

.violations-box {
  border-left-color: #ff6b6b;
}

.warnings-box {
  border-left-color: #ff9944;
}

.violations-title,
.warnings-title {
  font-weight: bold;
  margin-bottom: 8px;
  font-size: 12px;
}

.violation-item,
.warning-item {
  padding: 8px;
  margin: 6px 0;
  background: #fff5f5;
  border-radius: 4px;
  font-size: 12px;
  color: #333;
}

.violation-item.critical {
  border-left: 2px solid #ff6b6b;
}

.warning-item {
  background: #fff9f0;
  border-left: 2px solid #ff9944;
}

.violation-item strong,
.warning-item strong {
  display: block;
  color: #001e50;
  margin-bottom: 4px;
}

.violation-item p,
.warning-item p {
  margin: 4px 0;
  line-height: 1.4;
}

.fix {
  color: #666;
  font-style: italic;
}

.pass-box {
  padding: 12px;
  background: #f0fff4;
  border-left: 3px solid #51cf66;
  border-radius: 4px;
  color: #51cf66;
  font-weight: bold;
}

.features-card {
  background: linear-gradient(135deg, #f0f9ff, #f9fafc);
  border-left: 4px solid #00d4ff;
}

.features-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.feature-item {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.feature-item i {
  color: #51cf66;
  font-weight: bold;
  font-size: 18px;
  margin-top: 2px;
}

.feature-item strong {
  display: block;
  color: #001e50;
  margin-bottom: 4px;
  font-size: 13px;
}

.feature-item p {
  margin: 0;
  color: #666;
  font-size: 12px;
  line-height: 1.5;
}

.info-card {
  background: linear-gradient(135deg, #f0f9ff, #f9fafc);
  border-left: 4px solid #00d4ff;
}

.info-card p {
  margin: 0;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 12px;
  color: #666;
}

.info-card i {
  color: #00d4ff;
}
</style>
