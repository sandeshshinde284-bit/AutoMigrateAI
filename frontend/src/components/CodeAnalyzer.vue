<template>
  <div class="section">
    <div class="page-title">
      <i class="ri-file-code-line"></i>
      <h1>Legacy Code Analyzer</h1>
    </div>

    <!-- Analyze Button -->
    <div class="section-card">
      <div class="section-title">
        <i class="ri-play-circle-line"></i>
        Analyze Legacy System
      </div>
      <div class="analyze-controls">
        <button
          @click="analyzeCode"
          :disabled="analyzing"
          class="btn btn-analyze"
        >
          <i class="ri-search-line"></i>
          {{ analyzing ? "Analyzing..." : "ANALYZE LEGACY CODE" }}
        </button>
        <p class="info-text">
          Scans legacy_system.py for complexity, endpoints, and migration
          priority
        </p>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="analyzing" class="section-card loading-card">
      <div class="loader"></div>
      <p>Analyzing codebase... (simulating AI code scan)</p>
    </div>

    <!-- Analysis Results -->
    <div v-if="analysis && !analyzing" class="section-card">
      <!-- Summary Metrics -->
      <div class="analysis-summary">
        <div class="metric-box">
          <div class="metric-label">Total Endpoints</div>
          <div class="metric-value">{{ analysis.total_endpoints }}</div>
          <div class="metric-desc">Identified</div>
        </div>
        <div class="metric-box">
          <div class="metric-label">Total Lines</div>
          <div class="metric-value">{{ analysis.total_lines_of_code }}</div>
          <div class="metric-desc">of Code</div>
        </div>
        <div class="metric-box">
          <div class="metric-label">Complexity</div>
          <div class="metric-value">
            {{ analysis.overall_complexity_score }}/100
          </div>
          <div class="metric-desc">
            <span
              :class="[
                'complexity-badge',
                getComplexityClass(analysis.overall_complexity_score),
              ]"
            >
              {{ getComplexityLabel(analysis.overall_complexity_score) }}
            </span>
          </div>
        </div>
        <div class="metric-box">
          <div class="metric-label">Est. Time</div>
          <div class="metric-value">
            {{ analysis.estimated_migration_time }}
          </div>
          <div class="metric-desc">to Migrate</div>
        </div>
      </div>
    </div>

    <!-- Critical Issues -->
    <div
      v-if="analysis && !analyzing && analysis.critical_issues.length > 0"
      class="section-card"
    >
      <div class="section-title">
        <i class="ri-alert-line"></i>
        Critical Issues Found
      </div>
      <div class="issues-list">
        <div
          v-for="(issue, idx) in analysis.critical_issues"
          :key="idx"
          class="issue-item"
        >
          {{ issue }}
        </div>
      </div>
    </div>

    <!-- Slow Operations -->
    <div
      v-if="analysis && !analyzing && analysis.slow_operations.length > 0"
      class="section-card"
    >
      <div class="section-title">
        <i class="ri-speed-up-line"></i>
        Performance Bottlenecks
      </div>
      <div class="slow-ops-table">
        <table>
          <thead>
            <tr>
              <th>Operation</th>
              <th>Location</th>
              <th>Duration</th>
              <th>Impact</th>
              <th>Fix Effort</th>
              <th>Recommendation</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(op, idx) in analysis.slow_operations" :key="idx">
              <td>
                <strong>{{ op.operation }}</strong>
              </td>
              <td>{{ op.location }}</td>
              <td class="mono">{{ op.duration_ms }}ms</td>
              <td>
                <span :class="['impact-badge', op.impact.toLowerCase()]">
                  {{ op.impact }}
                </span>
              </td>
              <td>{{ op.fix_effort }}</td>
              <td class="recommendation">{{ op.recommendation }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Endpoints Analysis -->
    <div v-if="analysis && !analyzing" class="section-card">
      <div class="section-title">
        <i class="ri-route-line"></i>
        Endpoint Analysis
      </div>
      <div class="endpoints-grid">
        <div
          v-for="(endpoint, idx) in analysis.endpoints.slice(0, 6)"
          :key="idx"
          class="endpoint-card"
        >
          <div class="endpoint-header">
            <span class="endpoint-name">{{ endpoint.endpoint }}</span>
            <span
              :class="[
                'priority-badge',
                endpoint.migration_priority.toLowerCase(),
              ]"
            >
              {{ endpoint.migration_priority }}
            </span>
          </div>
          <div class="endpoint-metrics">
            <div class="metric">
              <span class="label">Complexity:</span>
              <span
                :class="['value', endpoint.complexity_category.toLowerCase()]"
              >
                {{ endpoint.complexity_category }}
              </span>
            </div>
            <div class="metric">
              <span class="label">Response:</span>
              <span class="value mono">{{ endpoint.response_time_ms }}ms</span>
            </div>
            <div class="metric">
              <span class="label">Risk:</span>
              <span :class="['value', endpoint.risk_level.toLowerCase()]">
                {{ endpoint.risk_level }}
              </span>
            </div>
            <div class="metric">
              <span class="label">Refactor:</span>
              <span class="value">{{ endpoint.estimated_refactor_days }}d</span>
            </div>
          </div>
          <div class="endpoint-deps">
            <small>Dependencies: {{ endpoint.dependencies.join(", ") }}</small>
          </div>
        </div>
      </div>
    </div>

    <!-- Migration Priority -->
    <div v-if="analysis && !analyzing" class="section-card">
      <div class="section-title">
        <i class="ri-stack-line"></i>
        Migration Roadmap (by Phase)
      </div>
      <div class="phases-container">
        <div v-for="phase in groupedPhases" :key="phase" class="phase-section">
          <h3 class="phase-title">📍 Phase {{ phase }}</h3>
          <div class="phase-items">
            <div
              v-for="(item, idx) in analysis.migration_priority.filter(
                (p) => p.phase === phase
              )"
              :key="idx"
              class="phase-item"
            >
              <div class="item-endpoint">{{ item.endpoint }}</div>
              <div class="item-details">
                <span class="detail">📊 {{ item.complexity }}</span>
                <span class="detail">⏱️ {{ item.estimated_days }}d</span>
                <span class="detail">🎯 {{ item.risk }}</span>
              </div>
              <div class="item-action">{{ item.action }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recommendations -->
    <div
      v-if="analysis && !analyzing"
      class="section-card recommendations-card"
    >
      <div class="section-title">
        <i class="ri-lightbulb-line"></i>
        AI Recommendations
      </div>
      <div class="recommendations-list">
        <div
          v-for="(rec, idx) in analysis.recommendations"
          :key="idx"
          class="rec-item"
        >
          <span class="rec-icon">💡</span>
          <span class="rec-text">{{ rec }}</span>
        </div>
      </div>
    </div>

    <!-- Error State -->
    <div v-if="error" class="section-card error-card">
      <div class="error-message">
        <i class="ri-error-warning-line"></i>
        <span>{{ error }}</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

interface Analysis {
  total_endpoints: number;
  total_lines_of_code: number;
  overall_complexity_score: number;
  estimated_migration_time: string;
  critical_issues: string[];
  slow_operations: any[];
  endpoints: any[];
  migration_priority: any[];
  recommendations: string[];
}

export default defineComponent({
  name: "CodeAnalyzer",
  data() {
    return {
      analysis: null as Analysis | null,
      analyzing: false,
      error: null as string | null,
    };
  },
  computed: {
    groupedPhases(): number[] {
      if (!this.analysis) return [];
      const phases = new Set(
        this.analysis.migration_priority.map((p) => p.phase)
      );
      return Array.from(phases).sort();
    },
  },
  methods: {
    async analyzeCode() {
      this.analyzing = true;
      this.error = null;

      try {
        const response = await fetch(
          "http://localhost:8000/proxy/analyze-code",
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ file: "legacy_system.py" }),
          }
        );

        const data = await response.json();

        if (data.success) {
          this.analysis = data.analysis;
          console.log("[CodeAnalyzer] Analysis complete:", data.analysis);
        } else {
          this.error = data.error || "Analysis failed";
        }
      } catch (error) {
        this.error = `Error: ${error}`;
        console.error("[CodeAnalyzer] Error:", error);
      } finally {
        this.analyzing = false;
      }
    },
    getComplexityClass(score: number): string {
      if (score < 50) return "low";
      if (score < 75) return "medium";
      return "high";
    },
    getComplexityLabel(score: number): string {
      if (score < 50) return "LOW";
      if (score < 75) return "MEDIUM";
      return "HIGH";
    },
  },
  mounted() {
    console.log("[CodeAnalyzer] Mounted");
    // Auto-analyze on mount
    setTimeout(() => this.analyzeCode(), 500);
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

.analyze-controls {
  display: flex;
  flex-direction: column;
  gap: 12px;
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
  width: fit-content;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-analyze {
  background: linear-gradient(135deg, #00d4ff, #0099cc);
  color: white;
}

.btn-analyze:hover:not(:disabled) {
  box-shadow: 0 4px 12px rgba(0, 212, 255, 0.3);
  transform: translateY(-2px);
}

.info-text {
  font-size: 12px;
  color: #666;
  margin: 0;
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

.analysis-summary {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 20px;
}

.metric-box {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
  border-left: 3px solid #00d4ff;
  text-align: center;
}

.metric-label {
  font-size: 12px;
  color: #666;
  margin-bottom: 8px;
}

.metric-value {
  font-size: 28px;
  font-weight: bold;
  color: #001e50;
  margin-bottom: 4px;
}

.metric-desc {
  font-size: 11px;
  color: #999;
}

.complexity-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 10px;
  font-weight: bold;
}

.complexity-badge.low {
  background: rgba(81, 207, 102, 0.2);
  color: #51cf66;
}

.complexity-badge.medium {
  background: rgba(255, 153, 68, 0.2);
  color: #ff9944;
}

.complexity-badge.high {
  background: rgba(255, 107, 107, 0.2);
  color: #ff6b6b;
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

.slow-ops-table {
  overflow-x: auto;
}

.slow-ops-table table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
}

.slow-ops-table thead {
  background: #f8f9fa;
  border-bottom: 2px solid #e8ecf1;
}

.slow-ops-table th {
  padding: 12px;
  text-align: left;
  font-weight: 600;
  color: #333;
}

.slow-ops-table td {
  padding: 10px 12px;
  border-bottom: 1px solid #e8ecf1;
  color: #666;
}

.slow-ops-table tbody tr:hover {
  background: #f8f9fa;
}

.mono {
  font-family: "Courier New", monospace;
}

.impact-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 10px;
  font-weight: bold;
  display: inline-block;
}

.impact-badge.critical {
  background: rgba(255, 107, 107, 0.2);
  color: #ff6b6b;
}

.impact-badge.high {
  background: rgba(255, 153, 68, 0.2);
  color: #ff9944;
}

.recommendation {
  font-size: 11px;
  color: #00d4ff;
  font-weight: 500;
}

.endpoints-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 16px;
}

.endpoint-card {
  background: linear-gradient(135deg, #f8fafc, #f0f4ff);
  border: 1px solid #e8eef5;
  border-radius: 8px;
  padding: 16px;
  transition: all 0.3s ease;
}

.endpoint-card:hover {
  border-color: #00d4ff;
  box-shadow: 0 4px 12px rgba(0, 212, 255, 0.15);
}

.endpoint-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  border-bottom: 1px solid #e8ecf1;
  padding-bottom: 10px;
}

.endpoint-name {
  font-weight: 600;
  color: #001e50;
  font-size: 13px;
}

.priority-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 10px;
  font-weight: bold;
}

.priority-badge.first {
  background: rgba(255, 107, 107, 0.2);
  color: #ff6b6b;
}

.priority-badge.medium {
  background: rgba(255, 153, 68, 0.2);
  color: #ff9944;
}

.priority-badge.last {
  background: rgba(81, 207, 102, 0.2);
  color: #51cf66;
}

.endpoint-metrics {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 12px;
}

.metric {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
}

.metric .label {
  color: #666;
  font-weight: 500;
}

.metric .value {
  color: #001e50;
  font-weight: 600;
}

.metric .value.low {
  color: #51cf66;
}

.metric .value.medium {
  color: #ff9944;
}

.metric .value.high {
  color: #ff6b6b;
}

.endpoint-deps {
  padding-top: 8px;
  border-top: 1px solid #e8ecf1;
  color: #999;
}

.phases-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
}

.phase-section {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 16px;
  border-left: 4px solid #00d4ff;
}

.phase-title {
  margin: 0 0 12px 0;
  color: #001e50;
  font-size: 14px;
  font-weight: bold;
}

.phase-items {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.phase-item {
  background: white;
  padding: 12px;
  border-radius: 6px;
  border-left: 3px solid #00d4ff;
}

.item-endpoint {
  font-weight: 600;
  color: #001e50;
  margin-bottom: 6px;
  font-size: 12px;
}

.item-details {
  display: flex;
  gap: 12px;
  margin-bottom: 8px;
  font-size: 11px;
  color: #666;
}

.detail {
  display: inline-block;
}

.item-action {
  font-size: 11px;
  color: #00d4ff;
  font-style: italic;
}

.recommendations-card {
  background: linear-gradient(135deg, #f0fff4, #f0f9ff);
  border-left: 4px solid #51cf66;
}

.recommendations-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.rec-item {
  display: flex;
  gap: 12px;
  font-size: 13px;
  color: #333;
  padding: 10px;
  background: white;
  border-radius: 6px;
  border-left: 3px solid #51cf66;
}

.rec-icon {
  flex-shrink: 0;
}

.rec-text {
  flex: 1;
}

.error-card {
  background: #fff5f5;
  border-left: 4px solid #ff6b6b;
}

.error-message {
  display: flex;
  gap: 12px;
  align-items: center;
  color: #660000;
  font-weight: 500;
}

.error-message i {
  font-size: 20px;
}
</style>
