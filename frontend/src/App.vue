<template>
  <div class="container">
    <!-- Header -->
    <div class="header">
      <div class="header-left">
        <div class="vw-logo">VW</div>
        <div class="header-title">AutoMigrate AI - Dashboard</div>
      </div>
      <div class="header-right">
        <div
          class="status-badge"
          :class="globalMigration >= 100 ? 'complete' : ''"
        >
          {{ globalMigration }}%
        </div>
      </div>
    </div>

    <!-- Main Layout -->
    <div class="main-wrapper">
      <!-- Sidebar Navigation -->
      <div class="sidebar">
        <div
          v-for="nav in navItems"
          :key="nav.id"
          @click="currentPage = nav.id"
          :class="['nav-item', { active: currentPage === nav.id }]"
        >
          <i :class="nav.icon"></i>
          <span>{{ nav.label }}</span>
        </div>
      </div>

      <!-- Content Area -->
      <div class="main-content">
        <Dashboard v-show="currentPage === 'dashboard'" />
        <MigrationProgress v-show="currentPage === 'migration'" />
        <PerformanceChart v-show="currentPage === 'performance'" />
        <CostMeter v-show="currentPage === 'cost'" />
        <ControlPanel
          v-show="currentPage === 'control'"
          @update:migration="handleMigrationUpdate"
        />
        <TrafficStats v-show="currentPage === 'traffic'" />
        <!-- NEW: Request History Component -->
        <RequestHistory v-show="currentPage === 'history'" />
        <CodeAnalyzer v-show="currentPage === 'analyzer'" />
        <DigitalTwinValidator v-show="currentPage === 'validator'" />
        <AutoScalingAdvisor v-show="currentPage === 'autoscaling'" />
        <ComplianceCard v-show="currentPage === 'compliance'" />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import Dashboard from "./components/Dashboard.vue";
import MigrationProgress from "./components/MigrationProgress.vue";
import PerformanceChart from "./components/PerformanceChart.vue";
import CostMeter from "./components/CostMeter.vue";
import ControlPanel from "./components/ControlPanel.vue";
import TrafficStats from "./components/TrafficStats.vue";
import RequestHistory from "./components/RequestHistory.vue";
import CodeAnalyzer from "./components/CodeAnalyzer.vue";
import { apiService } from "./services/api";
import DigitalTwinValidator from "./components/DigitalTwinValidator.vue";
import AutoScalingAdvisor from "./components/AutoScalingAdvisor.vue";
import ComplianceCard from "./components/ComplianceCard.vue";
import { useMetricsStore } from "./stores/metricsStore";
import { mapState, mapActions } from "pinia";

interface NavItem {
  id: string;
  label: string;
  icon: string;
}

export default defineComponent({
  name: "App",
  components: {
    Dashboard,
    MigrationProgress,
    PerformanceChart,
    CostMeter,
    ControlPanel,
    TrafficStats,
    RequestHistory,
    CodeAnalyzer,
    DigitalTwinValidator,
    AutoScalingAdvisor,
    ComplianceCard,
  },
  data() {
    return {
      currentPage: "dashboard" as string,
      // globalMigration: 0 as number,
      globalRefreshInterval: null as NodeJS.Timeout | null,
      refreshKey: 0 as number,
      navItems: [
        { id: "dashboard", label: "Dashboard", icon: "ri-dashboard-line" },
        { id: "migration", label: "Migration", icon: "ri-git-branch-line" },
        { id: "performance", label: "Performance", icon: "ri-line-chart-line" },
        { id: "cost", label: "Cost", icon: "ri-wallet-line" },
        { id: "control", label: "Control", icon: "ri-settings-3-line" },
        { id: "traffic", label: "Traffic", icon: "ri-bar-chart-2-line" },
        { id: "history", label: "History", icon: "ri-history-line" },
        { id: "analyzer", label: "Analyzer", icon: "ri-file-code-line" },
        { id: "validator", label: "Validator", icon: "ri-test-tube-line" },
        { id: "autoscaling", label: "Scaling", icon: "ri-speed-up-line" },
        { id: "compliance", label: "Compliance", icon: "ri-shield-check-line" },
      ] as NavItem[],
    };
  },
  computed: {
    // GET migration_percentage directly from the store's state
    ...mapState(useMetricsStore, ["migration_percentage"]),

    // Alias it for your template
    globalMigration() {
      return this.migration_percentage;
    },
  },
  methods: {
    // async globalFetchMetrics() {
    //   try {
    //     const data = await apiService.getMetrics();
    //     this.globalMigration = data.migration_percentage || 0;
    //     console.log("[App] Global migration:", this.globalMigration);
    //     this.refreshKey += 1;
    //   } catch (error) {
    //     console.error("[App] Error fetching metrics:", error);
    //   }
    // },

    // MAP the action from the store
    ...mapActions(useMetricsStore, ["fetchMetrics"]),

    handleMigrationUpdate() {
      console.log("[App] Migration update event received");
      //this.globalFetchMetrics();
      this.fetchMetrics();
    },
  },
  mounted() {
    console.log("[App] Mounted - starting global refresh");
    //this.globalFetchMetrics();
    this.fetchMetrics();
    this.globalRefreshInterval = setInterval(() => {
      //this.globalFetchMetrics();
      this.fetchMetrics();
    }, 3000);
  },
  beforeUnmount() {
    console.log("[App] Unmounting - clearing intervals");
    if (this.globalRefreshInterval) {
      clearInterval(this.globalRefreshInterval);
    }
  },
});
</script>

<style scoped>
.container {
  width: 100%;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f5f7fa;
}

.header {
  background-color: #001e50;
  color: white;
  padding: 0 30px;
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 8px rgba(0, 30, 80, 0.15);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.vw-logo {
  font-size: 24px;
  font-weight: bold;
  letter-spacing: 2px;
  color: #00d4ff;
}

.header-title {
  font-size: 16px;
  font-weight: 500;
  color: white;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.status-badge {
  background: linear-gradient(135deg, #ff6b6b, #ff8a9b);
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: bold;
  font-size: 14px;
  transition: all 0.3s ease;
}

.status-badge.complete {
  background: linear-gradient(135deg, #51cf66, #69db7c);
}

.main-wrapper {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.sidebar {
  width: 80px;
  background-color: #001e50;
  padding: 20px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
}

.nav-item {
  width: 60px;
  height: 60px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 5px;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.3s ease;
  color: #8899bb;
  font-size: 10px;
  text-align: center;
}

.nav-item i {
  font-size: 24px;
}

.nav-item:hover {
  color: #00d4ff;
}

.nav-item.active {
  color: #00d4ff;
  background-color: rgba(0, 212, 255, 0.1);
  border-left: 3px solid #00d4ff;
  padding-left: 3px;
}

.main-content {
  flex: 1;
  padding: 30px;
  overflow-y: auto;
}

.main-content::-webkit-scrollbar {
  width: 8px;
}

.main-content::-webkit-scrollbar-track {
  background: transparent;
}

.main-content::-webkit-scrollbar-thumb {
  background: #d0d8e0;
  border-radius: 4px;
}

.main-content::-webkit-scrollbar-thumb:hover {
  background: #b0b8c0;
}
</style>
