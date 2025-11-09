<template>
  <div class="section">
    <div class="page-title">
      <i class="ri-test-tube-line"></i>
      <h1>Digital Twin Validator</h1>
    </div>

    <!-- Safety Check Info -->
    <div class="section-card info-card">
      <div class="info-header">
        <i class="ri-shield-check-line"></i>
        <h3>Zero-Risk Migration Testing</h3>
      </div>
      <p>
        Test migration scenarios in a simulated environment before going live.
        The Digital Twin runs synthetic load tests to predict real-world
        behavior.
      </p>
    </div>

    <!-- Validation Controls -->
    <div class="section-card">
      <div class="section-title">
        <i class="ri-settings-line"></i>
        Run Validation Test
      </div>

      <div class="controls-grid">
        <div class="control-group">
          <label>Migration Percentage</label>
          <div class="slider-container">
            <input
              v-model.number="testPercentage"
              type="range"
              min="0"
              max="100"
              step="5"
              class="percentage-slider"
            />
            <span class="percentage-display">{{ testPercentage }}%</span>
          </div>
        </div>

        <div class="control-group">
          <label>Traffic Volume</label>
          <select v-model.number="trafficVolume" class="control-select">
            <option value="50">Low (50 requests)</option>
            <option value="100">Medium (100 requests)</option>
            <option value="250">High (250 requests)</option>
            <option value="500">Very High (500 requests)</option>
          </select>
        </div>

        <div class="control-group">
          <label>Duration (seconds)</label>
          <input
            v-model.number="duration"
            type="number"
            min="10"
            max="120"
            class="control-input"
          />
        </div>
      </div>

      <button
        @click="runValidation"
        :disabled="validating"
        class="btn btn-validate"
      >
        <i class="ri-play-line"></i>
        {{ validating ? "Testing..." : "RUN VALIDATION" }}
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="validating" class="section-card loading-card">
      <div class="loader"></div>
      <p>Running Digital Twin simulation...</p>
      <p class="loading-detail">
        Testing {{ trafficVolume }} synthetic requests at {{ testPercentage }}%
      </p>
    </div>

    <!-- Validation Results -->
    <div v-if="validation && !validating" class="section-card">
      <div class="validation-header">
        <div
          class="score-box"
          :class="[getScoreClass(validation.analysis.validation_score)]"
        >
          <div class="score-value">
            {{ validation.analysis.validation_score }}
          </div>
          <div class="score-label">/ 100</div>
        </div>
        <div class="header-info">
          <h3>{{ validation.analysis.confidence_level }} Confidence</h3>
          <p class="recommendation">{{ validation.recommendation }}</p>
          <span
            :class="[
              'status-badge',
              validation.analysis.passed ? 'passed' : 'failed',
            ]"
          >
            {{ validation.analysis.passed ? "✅ SAFE" : "❌ UNSAFE" }}
          </span>
        </div>
      </div>
    </div>

    <!-- Simulation Results -->
    <div v-if="validation && !validating" class="section-card">
      <div class="section-title">
        <i class="ri-bar-chart-line"></i>
        Simulation Results
      </div>

      <div class="results-grid">
        <div class="result-card">
          <div class="result-label">Legacy Requests</div>
          <div class="result-value">
            {{ validation.simulation_results.legacy_requests_count }}
          </div>
          <div class="result-subtext">
            {{
              (
                (validation.simulation_results.legacy_requests_count /
                  validation.traffic_volume) *
                100
              ).toFixed(1)
            }}%
          </div>
        </div>

        <div class="result-card">
          <div class="result-label">Cloud Requests</div>
          <div class="result-value">
            {{ validation.simulation_results.cloud_requests_count }}
          </div>
          <div class="result-subtext">
            {{
              (
                (validation.simulation_results.cloud_requests_count /
                  validation.traffic_volume) *
                100
              ).toFixed(1)
            }}%
          </div>
        </div>

        <div class="result-card">
          <div class="result-label">Avg Response (Legacy)</div>
          <div class="result-value mono">
            {{ validation.simulation_results.legacy_avg_response_time }}ms
          </div>
          <div class="result-subtext">2000-3500ms baseline</div>
        </div>

        <div class="result-card">
          <div class="result-label">Avg Response (Cloud)</div>
          <div class="result-value mono">
            {{ validation.simulation_results.cloud_avg_response_time }}ms
          </div>
          <div class="result-subtext">50-150ms optimal</div>
        </div>

        <div class="result-card">
          <div class="result-label">Performance Gain</div>
          <div class="result-value accent">
            {{ validation.analysis.performance_improvement }}x
          </div>
          <div class="result-subtext">faster than legacy</div>
        </div>

        <div class="result-card">
          <div class="result-label">Error Rate</div>
          <div
            :class="[
              'result-value',
              validation.simulation_results.error_rate > 5 ? 'danger' : 'safe',
            ]"
          >
            {{ validation.simulation_results.error_rate }}%
          </div>
          <div class="result-subtext">target: <2%</div>
        </div>
      </div>
    </div>

    <!-- Metrics Table -->
    <div v-if="validation && !validating" class="section-card">
      <div class="section-title">
        <i class="ri-table-2"></i>
        Detailed Metrics
      </div>
      <div class="metrics-table-wrapper">
        <table class="metrics-table">
          <tbody>
            <tr>
              <td class="metric-name">Total Requests Simulated</td>
              <td class="metric-value">{{ validation.traffic_volume }}</td>
            </tr>
            <tr>
              <td class="metric-name">Peak Response Time</td>
              <td class="metric-value mono">
                {{ validation.simulation_results.peak_response_time }}ms
              </td>
            </tr>
            <tr>
              <td class="metric-name">Minimum Response Time</td>
              <td class="metric-value mono">
                {{ validation.simulation_results.min_response_time }}ms
              </td>
            </tr>
            <tr>
              <td class="metric-name">Legacy Success Rate</td>
              <td class="metric-value">
                {{ validation.simulation_results.legacy_success_rate }}%
              </td>
            </tr>
            <tr>
              <td class="metric-name">Cloud Success Rate</td>
              <td class="metric-value">
                {{ validation.simulation_results.cloud_success_rate }}%
              </td>
            </tr>
            <tr>
              <td class="metric-name">Total Errors</td>
              <td class="metric-value">
                {{ validation.simulation_results.total_errors }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Issues & Warnings -->
    <div
      v-if="
        validation &&
        !validating &&
        (validation.analysis.issues.length > 0 ||
          validation.analysis.warnings.length > 0)
      "
      class="section-card"
    >
      <div v-if="validation.analysis.issues.length > 0" class="issues-section">
        <div class="section-title">
          <i class="ri-alert-line"></i>
          Critical Issues
        </div>
        <div class="issues-list">
          <div
            v-for="(issue, idx) in validation.analysis.issues"
            :key="idx"
            class="issue-item critical"
          >
            {{ issue }}
          </div>
        </div>
      </div>

      <div
        v-if="validation.analysis.warnings.length > 0"
        class="warnings-section"
      >
        <div class="section-title">
          <i class="ri-alert-fill"></i>
          Warnings
        </div>
        <div class="warnings-list">
          <div
            v-for="(warning, idx) in validation.analysis.warnings"
            :key="idx"
            class="warning-item"
          >
            {{ warning }}
          </div>
        </div>
      </div>
    </div>

    <!-- Next Steps -->
    <div v-if="validation && !validating" class="section-card next-steps-card">
      <div class="section-title">
        <i class="ri-arrow-right-line"></i>
        Recommended Next Step
      </div>
      <div class="next-step-info">
        <p>
          <strong>Current:</strong> {{ testPercentage }}%
          <strong v-if="nextStep"
            >→ Recommended Next: {{ nextStep.recommended_next }}%</strong
          >
        </p>
        <p class="step-reason">{{ nextStep?.reason }}</p>
        <button
          @click="increaseToNext"
          v-if="nextStep && nextStep.recommended_next"
          class="btn btn-next"
        >
          <i class="ri-arrow-right-line"></i>
          Proceed to {{ nextStep.recommended_next }}%
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { apiService } from "../services/api.ts";

interface ValidationResult {
  validation_score: number;
  confidence_level: string;
  passed: boolean;
  performance_improvement: number;
  issues: string[];
  warnings: string[];
}

interface SimulationResults {
  legacy_requests_count: number;
  cloud_requests_count: number;
  legacy_avg_response_time: number;
  cloud_avg_response_time: number;
  legacy_success_rate: number;
  cloud_success_rate: number;
  error_rate: number;
  peak_response_time: number;
  min_response_time: number;
  total_errors: number;
  response_time: number;
}

interface Validation {
  target_percentage: number;
  traffic_volume: number;
  analysis: ValidationResult;
  simulation_results: SimulationResults;
  recommendation: string;
}

export default defineComponent({
  name: "DigitalTwinValidator",
  data() {
    return {
      testPercentage: 50,
      trafficVolume: 100,
      duration: 30,
      validating: false,
      validation: null as Validation | null,
      nextStep: null as any,
    };
  },
  methods: {
    async runValidation() {
      this.validating = true;
      this.validation = null;

      try {
        // const response = await fetch(
        //   "http://localhost:8000/proxy/validate-migration",
        //   {
        //     method: "POST",
        //     headers: { "Content-Type": "application/json" },
        //     body: JSON.stringify({
        //       percentage: this.testPercentage,
        //       duration: this.duration,
        //       traffic_volume: this.trafficVolume,
        //     }),
        //   }
        // );

        // const data = await response.json();
        const data = await apiService.validateMigration(
          this.testPercentage,
          this.duration,
          this.trafficVolume
        );

        if (data.success) {
          this.validation = data.validation;
          console.log("[DigitalTwin] Validation complete:", data.validation);

          // Fetch next step recommendation
          this.fetchNextStep();
        } else {
          console.error("[DigitalTwin] Validation failed:", data.error);
        }
      } catch (error) {
        console.error("[DigitalTwin] Error:", error);
      } finally {
        this.validating = false;
      }
    },
    async fetchNextStep() {
      try {
        // const response = await fetch(
        //   `http://localhost:8000/proxy/next-migration-step?current=${this.testPercentage}`
        // );
        // const data = await response.json();
        const data = await apiService.fetchNextStep(this.testPercentage);
        if (data.success) {
          this.nextStep = data.next_step;
        }
      } catch (error) {
        console.error("[DigitalTwin] Error fetching next step:", error);
      }
    },
    increaseToNext() {
      if (this.nextStep && this.nextStep.recommended_next) {
        this.testPercentage = this.nextStep.recommended_next;
        setTimeout(() => this.runValidation(), 500);
      }
    },
    getScoreClass(score: number): string {
      if (score >= 90) return "excellent";
      if (score >= 75) return "good";
      if (score >= 50) return "fair";
      return "poor";
    },
  },
  mounted() {
    console.log("[DigitalTwinValidator] Mounted");
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

.info-card {
  background: linear-gradient(135deg, #f0f9ff, #f0f4ff);
  border-left: 4px solid #00d4ff;
}

.info-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.info-header i {
  font-size: 24px;
  color: #00d4ff;
}

.info-header h3 {
  margin: 0;
  color: #001e50;
  font-size: 16px;
}

.info-card p {
  margin: 0;
  color: #666;
  font-size: 13px;
  line-height: 1.6;
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

.controls-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.control-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.control-group label {
  font-weight: 600;
  color: #001e50;
  font-size: 13px;
}

.slider-container {
  display: flex;
  align-items: center;
  gap: 12px;
}

.percentage-slider {
  flex: 1;
  height: 6px;
  cursor: pointer;
  accent-color: #00d4ff;
}

.percentage-display {
  font-weight: bold;
  color: #00d4ff;
  min-width: 50px;
  text-align: right;
  font-size: 14px;
}

.control-select,
.control-input {
  padding: 8px 12px;
  border: 1px solid #e8eef5;
  border-radius: 6px;
  font-size: 13px;
  color: #333;
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

.btn-validate {
  background: linear-gradient(135deg, #00d4ff, #0099cc);
  color: white;
  width: 100%;
  justify-content: center;
}

.btn-validate:hover:not(:disabled) {
  box-shadow: 0 4px 12px rgba(0, 212, 255, 0.3);
}

.btn-next {
  background: #51cf66;
  color: white;
  margin-top: 12px;
}

.btn-next:hover:not(:disabled) {
  background: #40c057;
}

.loading-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 40px;
  background: linear-gradient(135deg, #f0f4ff, #f9fafc);
  border-left: 4px solid #00d4ff;
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

.validation-header {
  display: flex;
  align-items: center;
  gap: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 20px;
}

.score-box {
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

.score-box.excellent {
  background: linear-gradient(135deg, #51cf66, #69db7c);
}

.score-box.good {
  background: linear-gradient(135deg, #00d4ff, #0099cc);
}

.score-box.fair {
  background: linear-gradient(135deg, #ff9944, #ffb366);
}

.score-box.poor {
  background: linear-gradient(135deg, #ff6b6b, #ff8a9b);
}

.score-value {
  font-size: 40px;
}

.score-label {
  font-size: 14px;
  opacity: 0.9;
}

.header-info {
  flex: 1;
}

.header-info h3 {
  margin: 0 0 8px 0;
  color: #001e50;
  font-size: 16px;
}

.recommendation {
  margin: 0 0 12px 0;
  color: #666;
  font-size: 13px;
}

.status-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: bold;
}

.status-badge.passed {
  background: rgba(81, 207, 102, 0.2);
  color: #51cf66;
}

.status-badge.failed {
  background: rgba(255, 107, 107, 0.2);
  color: #ff6b6b;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
}

.result-card {
  background: #f8f9fa;
  border: 1px solid #e8eef5;
  border-radius: 8px;
  padding: 16px;
  text-align: center;
  transition: all 0.3s ease;
}

.result-card:hover {
  border-color: #00d4ff;
  box-shadow: 0 4px 12px rgba(0, 212, 255, 0.15);
}

.result-label {
  font-size: 12px;
  color: #666;
  margin-bottom: 8px;
  font-weight: 500;
}

.result-value {
  font-size: 28px;
  font-weight: bold;
  color: #001e50;
  margin-bottom: 4px;
}

.result-value.mono {
  font-family: "Courier New", monospace;
  font-size: 24px;
}

.result-value.accent {
  color: #00d4ff;
}

.result-value.safe {
  color: #51cf66;
}

.result-value.danger {
  color: #ff6b6b;
}

.result-subtext {
  font-size: 11px;
  color: #999;
}

.metrics-table-wrapper {
  overflow-x: auto;
}

.metrics-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.metrics-table tbody tr {
  border-bottom: 1px solid #e8ecf1;
}

.metrics-table tbody tr:hover {
  background: #f8f9fa;
}

.metric-name {
  padding: 12px;
  color: #333;
  font-weight: 500;
}

.metric-value {
  padding: 12px;
  text-align: right;
  color: #001e50;
  font-weight: bold;
}

.metric-value.mono {
  font-family: "Courier New", monospace;
}

.issues-section,
.warnings-section {
  margin-bottom: 20px;
}

.issues-section .section-title {
  margin-bottom: 12px;
}

.issues-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.issue-item {
  padding: 12px;
  background: #fff5f5;
  border-left: 3px solid #ff6b6b;
  border-radius: 4px;
  color: #660000;
  font-size: 13px;
}

.warnings-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.warning-item {
  padding: 12px;
  background: #fff9e6;
  border-left: 3px solid #ff9944;
  border-radius: 4px;
  color: #664400;
  font-size: 13px;
}

.next-steps-card {
  background: linear-gradient(135deg, #f0fff4, #f0f9ff);
  border-left: 4px solid #51cf66;
}

.next-step-info {
  background: white;
  padding: 16px;
  border-radius: 8px;
}

.next-step-info p {
  margin: 8px 0;
  color: #333;
  font-size: 13px;
}

.next-step-info strong {
  color: #001e50;
}

.step-reason {
  color: #666;
  font-style: italic;
}

.mono {
  font-family: "Courier New", monospace;
}
</style>
