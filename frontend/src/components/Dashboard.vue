<template>
  <div class="section">
    <div class="page-title">
      <i class="ri-dashboard-fill"></i>
      <h1>Dashboard Overview</h1>
    </div>

    <div class="kpi-cards">
      <div class="kpi-card">
        <div class="kpi-header">
          <div class="kpi-label">Migration</div>
          <div class="kpi-trend"><i class="ri-arrow-up-line"></i></div>
        </div>
        <div class="kpi-value">{{ metrics.migration_percentage }}%</div>
        <div class="progress-bar">
          <div
            class="progress-fill"
            :style="{ width: metrics.migration_percentage + '%' }"
          ></div>
        </div>
        <div class="progress-text">Complete</div>
      </div>

      <div class="kpi-card">
        <div class="kpi-header">
          <div class="kpi-label">Performance</div>
          <div class="kpi-trend"><i class="ri-arrow-up-line"></i></div>
        </div>
        <div class="kpi-value">{{ performanceGain }}x</div>
        <div class="progress-text">Faster than baseline</div>
      </div>

      <div class="kpi-card">
        <div class="kpi-header">
          <div class="kpi-label">Cost Savings</div>
          <div class="kpi-trend"><i class="ri-arrow-down-line"></i></div>
        </div>
        <div class="kpi-value">₹{{ costSavedLakhs }}L</div>
        <div class="progress-text">Total savings achieved</div>
      </div>
    </div>

    <div class="dashboard-columns">
      <div class="column-left">
        <div class="section-title">
          <i class="ri-history-line"></i>
          Recent Activity
        </div>
        <div class="activity-section">
          <div class="activity-timeline">
            <div
              class="activity-item"
              v-for="item in recentActivity"
              :key="item.time"
            >
              <div class="activity-dot"></div>
              <div class="activity-time">{{ item.time }}</div>
              <div class="activity-text">{{ item.text }}</div>
            </div>
          </div>
        </div>
      </div>

      <div class="column-right">
        <div class="section-title">
          <i class="ri-server-line"></i>
          System Status
        </div>
        <div class="status-section">
          <div class="status-content">
            <div class="status-indicator"></div>
            <div>
              <div class="status-text">All Systems Operational</div>
              <div class="status-detail">
                {{ metrics.cloud_requests }} Cloud /
                {{ metrics.legacy_requests }} Legacy
              </div>
            </div>
          </div>
          <div class_="status-detail-text">Last updated: Just now</div>
        </div>

        <div class="section-title" style="margin-top: 20px">
          <i class="ri-lightning-fill"></i>
          Quick Actions
        </div>
        <div class="actions-section">
          <button class="action-button">
            <i class="action-icon ri-file-chart-line"></i>
            View Report
          </button>
          <button class="action-button">
            <i class="action-icon ri-calendar-schedule-line"></i>
            Schedule Migration
          </button>
          <button class="action-button">
            <i class="action-icon ri-search-line"></i>
            Run Analysis
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useMetricsStore } from "../stores/metricsStore"; // <-- IMPORT

// interface Metrics {
//   total_requests: number;
//   legacy_requests: number;
//   cloud_requests: number;
//   error_count: number;
//   legacy_avg_time: number;
//   cloud_avg_time: number;
//   cost_saved: number;
//   migration_percentage: number;
// }

export default defineComponent({
  name: "Dashboard",
  // data() {
  //   return {
  //     metrics: {
  //       total_requests: 0,
  //       legacy_requests: 0,
  //       cloud_requests: 0,
  //       error_count: 0,
  //       legacy_avg_time: 2847,
  //       cloud_avg_time: 87,
  //       cost_saved: 0,
  //       migration_percentage: 0,
  //     } as Metrics,
  //     refreshInterval: null as NodeJS.Timeout | null,
  //   };
  // },
  data() {
    return {
      // Static data for the new "Recent Activity" timeline
      recentActivity: [
        {
          time: "Today, 14:32",
          text: "Engine Management migration completed successfully",
        },
        {
          time: "Today, 12:15",
          text: "Performance threshold reached for Infotainment System",
        },
        {
          time: "Yesterday, 16:45",
          text: "Cost savings report updated with latest metrics",
        },
        {
          time: "Yesterday, 09:00",
          text: "Scheduled migration for Diagnostics System initiated",
        },
      ],
    };
  },
  computed: {
    //   performanceGain(): number {
    //     if (this.metrics.cloud_avg_time === 0) return 0;
    //     return Math.round(
    //       this.metrics.legacy_avg_time / this.metrics.cloud_avg_time
    //     );
    //   },
    metrics() {
      return useMetricsStore();
    },
    performanceGain() {
      return useMetricsStore().performanceGain;
    },
    costSavedLakhs() {
      return useMetricsStore().costSavedLakhs;
    },
  },
  // methods: {
  //   async fetchMetrics() {
  //     try {
  //       const data = await apiService.getMetrics();
  //       this.metrics = data;
  //       console.log(
  //         "[Dashboard] Metrics updated:",
  //         this.metrics.migration_percentage
  //       );
  //     } catch (error) {
  //       console.error("[Dashboard] Error fetching metrics:", error);
  //     }
  //   },
  //},
  //   mounted() {
  //     console.log("[Dashboard] Mounted");
  //     // Fetch immediately
  //     this.fetchMetrics();

  //     // Refresh independently every 2 seconds
  //     this.refreshInterval = setInterval(() => {
  //       this.fetchMetrics();
  //     }, 2000);
  //   },
  //   beforeUnmount() {
  //     console.log("[Dashboard] Unmounting");
  //     if (this.refreshInterval) clearInterval(this.refreshInterval);
  //   },
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

.kpi-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 40px;
}

.kpi-card {
  background: white;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 2px 8px rgba(0, 30, 80, 0.08);
  border: 1px solid #e8eef5;
  transition: all 0.3s ease;
}

.kpi-card:hover {
  box-shadow: 0 4px 16px rgba(0, 30, 80, 0.12);
}

.kpi-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.kpi-label {
  font-size: 13px;
  color: #7a8a9a;
  font-weight: 500;
  text-transform: uppercase;
}

.kpi-trend {
  font-size: 18px;
  color: #00d4ff;
}

.kpi-value {
  font-size: 32px;
  font-weight: bold;
  color: #001e50;
  margin-bottom: 12px;
}

.progress-bar {
  width: 100%;
  height: 6px;
  background-color: #e8eef5;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #00d4ff, #0099cc);
  transition: width 0.5s ease;
}

.progress-text {
  font-size: 12px;
  color: #7a8a9a;
  margin-top: 8px;
}

.section-card {
  background: white;
  border-radius: 12px;
  padding: 25px;
  margin-bottom: 40px;
  box-shadow: 0 2px 8px rgba(0, 30, 80, 0.08);
  border: 1px solid #e8eef5;
}

.section-title {
  font-size: 14px;
  font-weight: bold;
  color: #001e50;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 10px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.section-title i {
  color: #00d4ff;
  font-size: 18px;
}

.status-info {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.status-info p {
  font-size: 13px;
  color: #666;
  padding: 8px 12px;
  background: #f8f9fa;
  border-radius: 6px;
}

.status-info strong {
  color: #001e50;
}
.dashboard-columns {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 30px;
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
.activity-section {
  background: white;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 2px 8px rgba(0, 30, 80, 0.08);
  border: 1px solid #e8eef5;
}
.activity-timeline {
  position: relative;
  padding-left: 20px;
}
.activity-timeline::before {
  content: "";
  position: absolute;
  left: 8px;
  top: 5px;
  bottom: 5px;
  width: 2px;
  background: #e8eef5;
}
.activity-item {
  position: relative;
  margin-bottom: 20px;
}
.activity-item:last-child {
  margin-bottom: 0;
}
.activity-dot {
  position: absolute;
  left: -17px;
  top: 5px;
  width: 10px;
  height: 10px;
  background-color: #00d4ff;
  border-radius: 50%;
  border: 2px solid white;
  box-shadow: 0 0 0 2px #00d4ff;
}
.activity-time {
  font-size: 12px;
  color: #7a8a9a;
  margin-bottom: 4px;
}
.activity-text {
  font-size: 14px;
  color: #333;
  line-height: 1.5;
}
.status-section {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 30, 80, 0.08);
  border: 1px solid #e8eef5;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}
.status-content {
  display: flex;
  align-items: center;
  gap: 15px;
}
.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: #22c55e;
  box-shadow: 0 0 8px rgba(34, 197, 94, 0.4);
  animation: pulse 2s infinite;
}
.status-text {
  font-size: 14px;
  font-weight: 500;
  color: #001e50;
}
.status-detail {
  font-size: 12px;
  color: #7a8a9a;
}
.status-detail-text {
  font-size: 12px;
  color: #7a8a9a;
}
.actions-section {
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
}
.action-button {
  background: white;
  border: 1px solid #e8eef5;
  border-radius: 8px;
  padding: 15px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  color: #001e50;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 10px;
}
.action-button:hover {
  background-color: #f5f7fa;
  color: #00d4ff;
  border-color: #00d4ff;
}
.action-icon {
  font-size: 18px;
}

@keyframes pulse {
  0%,
  100% {
    box-shadow: 0 0 8px rgba(34, 197, 94, 0.4);
  }
  50% {
    box-shadow: 0 0 16px rgba(34, 197, 94, 0.6);
  }
}
</style>
