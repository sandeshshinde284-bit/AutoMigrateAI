<template>
  <div class="section">
    <div class="page-title">
      <i class="ri-line-chart-line"></i>
      <h1>Performance Optimization</h1>
    </div>

    <div class="metrics-section">
      <div class="metric-card legacy">
        <div class="metric-label">Legacy Response Time</div>
        <div class="metric-value">{{ metrics.legacy_avg_time }}ms</div>
        <div class="metric-subtitle">Legacy System</div>
      </div>
      <div class="metric-card improvement">
        <div class="metric-label">Performance Improvement</div>
        <div class="metric-value">{{ performanceGain }}x</div>
        <div class="metric-subtitle">Vs. Baseline</div>
      </div>
      <div class="metric-card cloud">
        <div class="metric-label">Cloud Response Time</div>
        <div class="metric-value">{{ metrics.cloud_avg_time }}ms</div>
        <div class="metric-subtitle">Cloud System</div>
      </div>
    </div>

    <div class="chart-section">
      <div class="chart-tabs">
        <div class="chart-tab active">Response Time</div>
        <div class="chart-tab">Processing Throughput</div>
        <div class="chart-tab">Error Rates</div>
      </div>

      <div class="chart-container">
        <svg
          width="100%"
          height="100%"
          viewBox="0 0 1000 320"
          preserveAspectRatio="none"
          style="position: absolute; left: 0; top: 0"
        >
          <text x="10" y="20" font-size="12" fill="#999">3000ms</text>
          <text x="10" y="80" font-size="12" fill="#999">2250ms</text>
          <text x="10" y="140" font-size="12" fill="#999">1500ms</text>
          <text x="10" y="200" font-size="12" fill="#999">750ms</text>
          <text x="10" y="260" font-size="12" fill="#999">0ms</text>

          <line
            x1="50"
            y1="20"
            x2="980"
            y2="20"
            stroke="#f0f0f0"
            stroke-width="1"
          />
          <line
            x1="50"
            y1="80"
            x2="980"
            y2="80"
            stroke="#f0f0f0"
            stroke-width="1"
          />
          <line
            x1="50"
            y1="140"
            x2="980"
            y2="140"
            stroke="#f0f0f0"
            stroke-width="1"
          />
          <line
            x1="50"
            y1="200"
            x2="980"
            y2="200"
            stroke="#f0f0f0"
            stroke-width="1"
          />
          <line
            x1="50"
            y1="260"
            x2="980"
            y2="260"
            stroke="#ddd"
            stroke-width="1"
          />

          <polyline
            points="60,80 150,85 240,90 330,120 420,200 510,250 600,280 690,290 780,295 870,298 960,300"
            fill="none"
            stroke="#ff4444"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />

          <polyline
            points="60,240 150,235 240,220 330,180 420,140 510,100 600,70 690,50 780,40 870,35 960,30"
            fill="none"
            stroke="#22cc88"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />

          <line
            x1="60"
            y1="150"
            x2="960"
            y2="150"
            stroke="#ff9944"
            stroke-width="1.5"
            stroke-dasharray="4,4"
          />

          <text x="50" y="280" font-size="12" fill="#999">0%</text>
          <text x="500" y="280" font-size="12" fill="#999" text-anchor="middle">
            50%
          </text>
          <text x="960" y="280" font-size="12" fill="#999" text-anchor="end">
            100%
          </text>
        </svg>
      </div>

      <div class="chart-legend">
        <div class="legend-item">
          <div class="legend-color legacy"></div>
          <span>Legacy System</span>
        </div>
        <div class="legend-item">
          <div class="legend-color cloud"></div>
          <span>Cloud System</span>
        </div>
        <div class="legend-item">
          <div class="legend-color threshold"></div>
          <span>Driver Perception Threshold</span>
        </div>
      </div>
    </div>

    <div class="technical-section">
      <div class="section-title">Technical Performance Details</div>
      <table class="tech-table">
        <thead>
          <tr>
            <th>Component</th>
            <th>Legacy Response</th>
            <th>Cloud Response</th>
            <th>Improvement</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="component-name">Engine Control Module</td>
            <td class="time-value">2847ms</td>
            <td class="time-value">87ms</td>
            <td class="improvement-value">+3168%</td>
            <td>
              <span class="status-badge status-optimized">Optimized</span>
            </td>
          </tr>
          <tr>
            <td class="component-name">Infotainment System</td>
            <td class="time-value">1523ms</td>
            <td class="time-value">156ms</td>
            <td class="improvement-value">+876%</td>
            <td>
              <span class="status-badge status-optimized">Optimized</span>
            </td>
          </tr>
          <tr>
            <td class="component-name">Diagnostics</td>
            <td class="time-value">892ms</td>
            <td class="time-value">45ms</td>
            <td class="improvement-value">+1882%</td>
            <td>
              <span class="status-badge status-optimized">Optimized</span>
            </td>
          </tr>
          <tr>
            <td class="component-name">Network Interface</td>
            <td class="time-value">1245ms</td>
            <td class="time-value">234ms</td>
            <td class="improvement-value">+432%</td>
            <td><span class="status-badge status-pending">Pending</span></td>
          </tr>
          <tr>
            <td class="component-name">Data Processing Pipeline</td>
            <td class="time-value">3156ms</td>
            <td class="time-value">512ms</td>
            <td class="improvement-value">+516%</td>
            <td><span class="status-badge status-critical">Critical</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useMetricsStore } from "../stores/metricsStore";

export default defineComponent({
  name: "PerformanceChart",
  computed: {
    // Get all metrics from the store
    metrics() {
      return useMetricsStore();
    },
    // Get the performanceGain getter
    performanceGain() {
      return useMetricsStore().performanceGain;
    },
  },
});
</script>

<style scoped>
/* Page Layout */
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

/* KPI Cards */
.metrics-section {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}
.metric-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border-left: 4px solid;
}
.metric-card.legacy {
  border-left-color: #ff4444;
}
.metric-card.improvement {
  border-left-color: #0099cc;
}
.metric-card.cloud {
  border-left-color: #22cc88;
}
.metric-label {
  font-size: 12px;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
}
.metric-value {
  font-size: 32px;
  font-weight: bold;
  color: #001e50;
  margin-bottom: 4px;
}
.metric-card.legacy .metric-value {
  color: #ff4444;
}
.metric-card.improvement .metric-value {
  color: #0099cc;
}
.metric-card.cloud .metric-value {
  color: #22cc88;
}
.metric-subtitle {
  font-size: 11px;
  color: #999;
}

/* Chart Section */
.chart-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}
.chart-tabs {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
  border-bottom: 1px solid #eee;
  padding-bottom: 12px;
}
.chart-tab {
  font-size: 13px;
  color: #666;
  cursor: pointer;
  padding: 8px 12px;
  border-bottom: 2px solid transparent;
  transition: all 0.3s ease;
  font-weight: 500;
}
.chart-tab:hover {
  color: #001e50;
}
.chart-tab.active {
  color: #00d4ff;
  border-bottom-color: #00d4ff;
}
.chart-container {
  position: relative;
  height: 320px;
  padding-top: 10px;
}
.chart-legend {
  display: flex;
  gap: 24px;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #eee;
  font-size: 12px;
  justify-content: center;
}
.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
}
.legend-color {
  width: 12px;
  height: 2px;
  border-radius: 1px;
}
.legend-color.legacy {
  background-color: #ff4444;
}
.legend-color.cloud {
  background-color: #22cc88;
}
.legend-color.threshold {
  background-color: #ff9944;
  border: 1px dashed #ff9944;
  height: 1px;
}

/* Technical Details Table */
.technical-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}
.section-title {
  font-size: 14px;
  font-weight: bold;
  color: #001e50;
  margin-bottom: 16px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.tech-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 16px;
}
.tech-table thead {
  background-color: #f5f7fa;
}
.tech-table th {
  padding: 12px 16px;
  text-align: left;
  font-size: 11px;
  color: #666;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 1px solid #ddd;
}
.tech-table td {
  padding: 12px 16px;
  font-size: 13px;
  border-bottom: 1px solid #f0f0f0;
}
.tech-table tbody tr:hover {
  background-color: #f9fafb;
}
.component-name {
  color: #001e50;
  font-weight: 500;
}
.time-value {
  font-family: "Courier New", monospace;
  color: #666;
  font-weight: 600;
}
.improvement-value {
  color: #22cc88;
  font-weight: bold;
}
.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 10px;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.status-optimized {
  background-color: rgba(34, 204, 136, 0.1);
  color: #22cc88;
}
.status-critical {
  background-color: rgba(255, 68, 68, 0.1);
  color: #ff4444;
}
.status-pending {
  background-color: rgba(255, 153, 68, 0.1);
  color: #ff9944;
}
</style>
