<template>
  <div class="section">
    <div class="page-title">
      <i class="ri-bar-chart-line"></i>
      <h1>System Traffic Analytics</h1>
    </div>

    <div class="section-card">
      <div class="section-title">
        <i class="ri-line-chart-line"></i>
        Traffic Overview
      </div>

      <div class="metrics-grid">
        <div class="metric-card">
          <div class="metric-label">Requests</div>
          <div class="metric-value">{{ metrics.total_requests }}</div>
          <div class="metric-change">+15%</div>
        </div>
        <div class="metric-card">
          <div class="metric-label">Availability</div>
          <div class="metric-value">{{ availability }}%</div>
          <div class="metric-change">+2.3%</div>
        </div>
        <div class="metric-card">
          <div class="metric-label">Avg. Response</div>
          <div class="metric-value">{{ metrics.cloud_avg_time }}ms</div>
          <div class="metric-change negative">-32%</div>
        </div>
        <div class="metric-card">
          <div class="metric-label">Error Rate</div>
          <div class="metric-value">{{ errorRate }}%</div>
          <div class="metric-change negative">-1.2%</div>
        </div>
      </div>

      <div class="chart-container">
        <div class="chart-title">Traffic Distribution by Source</div>
        <div class="bar-chart">
          <div class="bar-item">
            <div class="bar-label">Web Traffic</div>
            <div class="bar-wrapper">
              <div class="bar-fill" style="width: 65%">65%</div>
            </div>
            <div class="bar-value">780K</div>
          </div>
          <div class="bar-item">
            <div class="bar-label">Mobile Traffic</div>
            <div class="bar-wrapper">
              <div class="bar-fill" style="width: 25%">25%</div>
            </div>
            <div class="bar-value">300K</div>
          </div>
          <div class="bar-item">
            <div class="bar-label">API Traffic</div>
            <div class="bar-wrapper">
              <div class="bar-fill" style="width: 8%">8%</div>
            </div>
            <div class="bar-value">96K</div>
          </div>
          <div class="bar-item">
            <div class="bar-label">Other</div>
            <div class="bar-wrapper">
              <div class="bar-fill" style="width: 2%">2%</div>
            </div>
            <div class="bar-value">24K</div>
          </div>
        </div>
      </div>
    </div>

    <div class="section-card">
      <div class="section-title">
        <i class="ri-table-2"></i>
        Performance Metrics
      </div>

      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>System</th>
              <th>Requests</th>
              <th>Response Time</th>
              <th>Error Rate</th>
              <th>Availability</th>
              <th>Trend</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Cloud Core</td>
              <td>420,000</td>
              <td>85ms</td>
              <td><span class="status-badge status-good">0.2%</span></td>
              <td>99.8%</td>
              <td>
                <span class="trend-indicator trend-up"
                  ><i class="ri-arrow-up-line"></i>+8%</span
                >
              </td>
            </tr>
            <tr>
              <td>Edge Nodes</td>
              <td>300,000</td>
              <td>92ms</td>
              <td><span class="status-badge status-good">0.3%</span></td>
              <td>99.5%</td>
              <td>
                <span class="trend-indicator trend-up"
                  ><i class="ri-arrow-up-line"></i>+5%</span
                >
              </td>
            </tr>
            <tr>
              <td>API Gateway</td>
              <td>240,000</td>
              <td>78ms</td>
              <td><span class="status-badge status-warning">0.6%</span></td>
              <td>98.9%</td>
              <td>
                <span class="trend-indicator trend-down"
                  ><i class="ri-arrow-down-line"></i>-2%</span
                >
              </td>
            </tr>
            <tr>
              <td>Database</td>
              <td>180,000</td>
              <td>95ms</td>
              <td><span class="status-badge status-good">0.1%</span></td>
              <td>99.9%</td>
              <td>
                <span class="trend-indicator trend-up"
                  ><i class="ri-arrow-up-line"></i>+3%</span
                >
              </td>
            </tr>
            <tr>
              <td>Cache Layer</td>
              <td>60,000</td>
              <td>45ms</td>
              <td><span class="status-badge status-good">0.05%</span></td>
              <td>99.95%</td>
              <td>
                <span class="trend-indicator trend-up"
                  ><i class="ri-arrow-up-line"></i>+12%</span
                >
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useMetricsStore } from "../stores/metricsStore";

export default defineComponent({
  name: "TrafficStats",
  computed: {
    // Get all metrics from the store
    metrics() {
      return useMetricsStore();
    },
    // Calculate availability
    availability(): string {
      const store = useMetricsStore();
      if (store.total_requests === 0) return "100.0";
      const avail =
        ((store.total_requests - store.error_count) / store.total_requests) *
        100;
      return avail.toFixed(1);
    },
    // Calculate error rate
    errorRate(): string {
      const store = useMetricsStore();
      if (store.total_requests === 0) return "0.0";
      const rate = (store.error_count / store.total_requests) * 100;
      return rate.toFixed(1);
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

/* Section Card */
.section-card {
  background-color: white;
  border-radius: 8px;
  padding: 25px;
  margin-bottom: 25px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
  border: 1px solid #e8ecf1;
}
.section-title {
  font-size: 18px;
  font-weight: bold;
  color: #001e50;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}
.section-title i {
  color: #00d4ff;
  font-size: 20px;
}

/* Traffic Overview */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
  margin-bottom: 25px;
}
.metric-card {
  background: linear-gradient(135deg, #f8fafc 0%, #eef4f9 100%);
  border: 1px solid #e0e8f0;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
}
.metric-value {
  font-size: 28px;
  font-weight: bold;
  color: #001e50;
  margin-bottom: 8px;
}
.metric-label {
  font-size: 13px;
  color: #666;
  margin-bottom: 8px;
}
.metric-change {
  font-size: 12px;
  color: #00a86b;
  font-weight: 500;
}
.metric-change.negative {
  color: #ff6b6b;
}

/* Bar Chart */
.chart-container {
  margin-top: 25px;
  padding-top: 20px;
  border-top: 1px solid #e8ecf1;
}
.chart-title {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin-bottom: 15px;
}
.bar-chart {
  display: flex;
  flex-direction: column;
  gap: 15px;
}
.bar-item {
  display: flex;
  align-items: center;
  gap: 12px;
}
.bar-label {
  font-size: 13px;
  color: #666;
  width: 100px;
  flex-shrink: 0;
}
.bar-wrapper {
  flex: 1;
  height: 28px;
  background-color: #f0f4f8;
  border-radius: 4px;
  overflow: hidden;
  position: relative;
}
.bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #00d4ff, #0099cc);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 8px;
  color: white;
  font-size: 12px;
  font-weight: 600;
  transition: all 0.3s ease;
}
.bar-value {
  font-size: 12px;
  color: #666;
  width: 50px;
  text-align: right;
  flex-shrink: 0;
}

/* Table Section */
.table-wrapper {
  overflow-x: auto;
}
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}
thead {
  background-color: #f8fafc;
  border-bottom: 2px solid #e8ecf1;
}
th {
  padding: 12px 16px;
  text-align: left;
  font-weight: 600;
  color: #333;
  white-space: nowrap;
}
td {
  padding: 14px 16px;
  border-bottom: 1px solid #e8ecf1;
  color: #666;
}
tbody tr:hover {
  background-color: #f8fafc;
}
.status-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}
.status-good {
  background-color: #d4f4dd;
  color: #00a86b;
}
.status-warning {
  background-color: #fff4d4;
  color: #ff9800;
}
.status-critical {
  background-color: #ffd4d4;
  color: #ff6b6b;
}
.trend-indicator {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-weight: 600;
}
.trend-up {
  color: #00a86b;
}
.trend-down {
  color: #ff6b6b;
}
</style>
