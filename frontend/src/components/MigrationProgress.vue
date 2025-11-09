<template>
  <div class="section">
    <div class="page-title">
      <i class="ri-git-branch-line"></i>
      <h1>Overall Migration Progress</h1>
    </div>

    <!-- Progress Overview -->
    <div class="section-card progress-overview">
      <div class="progress-circle-container">
        <div
          class="progress-circle"
          :style="{ '--progress-deg': (migration / 100) * 360 + 'deg' }"
        >
          <div class="progress-text">
            <div class="progress-percentage">{{ migration }}%</div>
            <div class="progress-label">Complete</div>
          </div>
        </div>
      </div>

      <div class="progress-bars">
        <div class="progress-item">
          <div class="progress-item-label">
            <span class="progress-item-label-text"
              >Legacy Systems Remaining</span
            >
            <span class="progress-item-value">{{ 100 - migration }}%</span>
          </div>
          <div class="progress-bar">
            <div
              class="progress-bar-fill legacy"
              :style="{ width: 100 - migration + '%' }"
            ></div>
          </div>
        </div>

        <div class="progress-item">
          <div class="progress-item-label">
            <span class="progress-item-label-text">Cloud Systems Complete</span>
            <span class="progress-item-value">{{ migration }}%</span>
          </div>
          <div class="progress-bar">
            <div
              class="progress-bar-fill cloud"
              :style="{ width: migration + '%' }"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Subsystem Breakdown -->
    <div class="section-card">
      <div class="section-title">
        <i class="ri-layers-line"></i>
        Subsystem Breakdown
      </div>
      <div class="subsystem-grid">
        <div
          v-for="subsystem in subsystems"
          :key="subsystem.name"
          class="subsystem-card"
        >
          <div class="subsystem-header">
            <span class="subsystem-name">{{ subsystem.name }}</span>
            <span class="subsystem-percentage"
              >{{ subsystem.percentage }}%</span
            >
          </div>
          <div class="subsystem-progress-bar">
            <div
              class="subsystem-progress-fill"
              :style="{ width: subsystem.percentage + '%' }"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <div class="section-card">
      <div class="section-title">
        <i class="ri-car-line"></i>
        Fleet Migration Status
      </div>
      <div class="fleet-status">
        <div class="fleet-info">
          <div class="fleet-vehicles">125/500</div>
          <div class="fleet-label">Vehicles Migrated</div>
        </div>
        <div class="fleet-chart">
          <div
            class="pie-chart"
            :style="{
              background: `conic-gradient(#00d4ff 0deg ${
                migration * 3.6
              }deg, #ff4757 ${migration * 3.6}deg 360deg)`,
            }"
          ></div>
        </div>
        <div class="fleet-map">
          <div class="fleet-map-content">
            <div class="map-icon"><i class="ri-map-pin-line"></i></div>
            <div>Geographic Distribution</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useMetricsStore } from "../stores/metricsStore";

interface Subsystem {
  name: string;
  percentage: number;
}

export default defineComponent({
  name: "MigrationProgress",
  data() {
    return {
      // migration: 0 as number,
      // refreshInterval: null as NodeJS.Timeout | null,
      subsystems: [
        { name: "Engine Management", percentage: 75 },
        { name: "Infotainment", percentage: 90 },
        { name: "Diagnostics", percentage: 45 },
        { name: "Telematics", percentage: 60 },
      ] as Subsystem[],
    };
  },
  computed: {
    // Get the migration percentage directly from the store
    migration() {
      return useMetricsStore().migration_percentage;
    },
  },
  methods: {
    // async fetchMigrationData() {
    //   try {
    //     const data = await apiService.getMetrics();
    //     this.migration = data.migration_percentage || 0;
    //     console.log("[MigrationProgress] Updated:", this.migration);
    //   } catch (error) {
    //     console.error("[MigrationProgress] Error:", error);
    //   }
    // },
  },
  // mounted() {
  //   console.log("[MigrationProgress] Mounted");
  //   // Fetch immediately
  //   this.fetchMigrationData();

  //   // Refresh independently every 2 seconds
  //   this.refreshInterval = setInterval(() => {
  //     this.fetchMigrationData();
  //   }, 2000);
  // },
  // beforeUnmount() {
  //   console.log("[MigrationProgress] Unmounting");
  //   if (this.refreshInterval) clearInterval(this.refreshInterval);
  // },
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

.progress-overview {
  display: flex;
  gap: 40px;
  align-items: center;
}

.progress-circle-container {
  flex-shrink: 0;
}

.progress-circle {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  background: conic-gradient(
    #00d4ff 0deg,
    #00d4ff var(--progress-deg),
    #e5e7eb var(--progress-deg),
    #e5e7eb 360deg
  );
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 212, 255, 0.2);
}

.progress-text {
  text-align: center;
  z-index: 1;
}

.progress-percentage {
  font-size: 48px;
  font-weight: bold;
  color: #00d4ff;
}

.progress-label {
  font-size: 12px;
  color: #7a8fa3;
  margin-top: 5px;
}

.progress-bars {
  flex: 1;
}

.progress-item {
  margin-bottom: 20px;
}

.progress-item-label {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 13px;
  font-weight: 500;
}

.progress-item-label-text {
  color: #333;
}

.progress-item-value {
  color: #00d4ff;
  font-weight: bold;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: #e8eef5;
  border-radius: 4px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-bar-fill.legacy {
  background: linear-gradient(90deg, #ff4757 0%, #ff6b7a 100%);
}

.progress-bar-fill.cloud {
  background: linear-gradient(90deg, #00d4ff 0%, #00a8cc 100%);
}

.subsystem-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.subsystem-card {
  background: #f9fafb;
  border: 1px solid #e8eef5;
  border-radius: 8px;
  padding: 20px;
  transition: all 0.3s ease;
}

.subsystem-card:hover {
  border-color: #00d4ff;
  box-shadow: 0 4px 12px rgba(0, 212, 255, 0.1);
}

.subsystem-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.subsystem-name {
  font-size: 14px;
  font-weight: 600;
  color: #001e50;
}

.subsystem-percentage {
  font-size: 16px;
  font-weight: bold;
  color: #00d4ff;
}

.subsystem-progress-bar {
  width: 100%;
  height: 6px;
  background: #e8eef5;
  border-radius: 3px;
  overflow: hidden;
}

.subsystem-progress-fill {
  height: 100%;
  border-radius: 3px;
  background: linear-gradient(90deg, #00d4ff 0%, #00a8cc 100%);
  transition: width 0.3s ease;
}

/* ADD THESE NEW STYLES */
.fleet-status {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 25px;
  align-items: center;
}

.fleet-info {
  text-align: center;
}

.fleet-vehicles {
  font-size: 32px;
  font-weight: bold;
  color: #00d4ff;
  margin-bottom: 5px;
}

.fleet-label {
  font-size: 13px;
  color: #7a8fa3;
}

.fleet-chart {
  display: flex;
  justify-content: center;
  align-items: center;
}

.pie-chart {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: background 0.5s ease;
}

.fleet-map {
  background: linear-gradient(135deg, #e8eef5 0%, #f5f7fa 100%);
  border-radius: 6px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #7a8fa3;
  font-size: 12px;
  position: relative;
  overflow: hidden;
  border: 1px solid #e8eef5;
}

.fleet-map::before {
  content: "";
  position: absolute;
  width: 100%;
  height: 100%;
  background-image: radial-gradient(
      circle at 20% 30%,
      rgba(0, 212, 255, 0.05) 0%,
      transparent 50%
    ),
    radial-gradient(
      circle at 80% 70%,
      rgba(0, 212, 255, 0.05) 0%,
      transparent 50%
    );
}

.fleet-map-content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

.map-icon {
  font-size: 24px;
  color: #00d4ff;
}
</style>
