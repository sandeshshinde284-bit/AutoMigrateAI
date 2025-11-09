<template>
  <div class="section">
    <div class="page-title">
      <i class="ri-wallet-line"></i>
      <h1>Financial Impact Analysis</h1>
    </div>

    <!-- Total Savings - REAL DATA -->
    <div class="section-card savings-card">
      <div class="savings-label">Total Cost Savings (Live)</div>
      <div class="savings-header">
        <div>
          <div class="savings-amount">
            ₹{{ Math.round(metrics.cost_saved / 100000) }}L
          </div>
        </div>
        <div class="savings-indicator">
          <i class="ri-arrow-up-line"></i>
          <span>Real-time calculation</span>
        </div>
      </div>
    </div>

    <!-- Cost Breakdown -->
    <div class="section-card">
      <div class="section-title">
        <i class="ri-money-dollar-circle-line"></i>
        Cost Savings Breakdown
      </div>
      <div class="breakdown-chart">
        <div class="breakdown-item">
          <div class="breakdown-label">
            <span class="breakdown-label-name">Infrastructure Savings</span>
            <span class="breakdown-label-value"
              >₹{{ Math.round((metrics.cost_saved * 0.43) / 100000) }}L</span
            >
          </div>
          <div class="breakdown-bar">
            <div class="breakdown-bar-fill" style="width: 43%"></div>
          </div>
        </div>
        <div class="breakdown-item">
          <div class="breakdown-label">
            <span class="breakdown-label-name">Maintenance Reduction</span>
            <span class="breakdown-label-value"
              >₹{{ Math.round((metrics.cost_saved * 0.29) / 100000) }}L</span
            >
          </div>
          <div class="breakdown-bar">
            <div class="breakdown-bar-fill" style="width: 29%"></div>
          </div>
        </div>
        <div class="breakdown-item">
          <div class="breakdown-label">
            <span class="breakdown-label-name">Operational Efficiency</span>
            <span class="breakdown-label-value"
              >₹{{ Math.round((metrics.cost_saved * 0.19) / 100000) }}L</span
            >
          </div>
          <div class="breakdown-bar">
            <div class="breakdown-bar-fill" style="width: 19%"></div>
          </div>
        </div>
        <div class="breakdown-item">
          <div class="breakdown-label">
            <span class="breakdown-label-name">License Consolidation</span>
            <span class="breakdown-label-value"
              >₹{{ Math.round((metrics.cost_saved * 0.09) / 100000) }}L</span
            >
          </div>
          <div class="breakdown-bar">
            <div class="breakdown-bar-fill" style="width: 9%"></div>
          </div>
        </div>
        <div class="breakdown-total">
          <div class="breakdown-total-bar">
            <span>Total Savings</span>
            <span>₹{{ Math.round(metrics.cost_saved / 100000) }}L</span>
          </div>
        </div>
      </div>
    </div>
    <div class="section-card">
      <div class="section-title">
        <i class="ri-lightbulb-flash-line"></i>
        Scenario Comparison
      </div>
      <div class="scenarios-grid">
        <div class="scenario-card">
          <div class="scenario-title">Conservative Pace</div>
          <div class="scenario-amount">₹3.1M</div>
          <div class="scenario-description">
            Slower implementation with minimal disruption.
          </div>
        </div>
        <div class="scenario-card recommended">
          <div class="scenario-badge">RECOMMENDED</div>
          <div class="scenario-title">Accelerated Pace</div>
          <div class="scenario-amount">₹5.7M</div>
          <div class="scenario-description">
            Increased investment for faster cloud adoption and greater savings.
          </div>
        </div>
        <div class="scenario-card">
          <div class="scenario-title">Aggressive Pace</div>
          <div class="scenario-amount">₹7.2M</div>
          <div class="scenario-description">
            Maximum resource allocation for fastest possible migration.
          </div>
        </div>
      </div>
    </div>

    <!-- ROI Info -->
    <div class="section-card">
      <div class="section-title">
        <i class="ri-git-compare-line"></i>
        ROI Metrics
      </div>
      <div class="roi-metrics">
        <div class="roi-item">
          <p class="roi-label">Investment Required</p>
          <p class="roi-value">
            ₹{{ (investmentRequired / 100000).toFixed(0) }}L
          </p>
        </div>
        <div class="roi-item">
          <p class="roi-label">Total Savings (Live)</p>
          <p class="roi-value">₹{{ costSavedLakhs }}L</p>
        </div>
        <div class="roi-item">
          <p class="roi-label">Payback Period</p>
          <p class="roi-value">{{ paybackMonths }} months</p>
        </div>
        <div class="roi-item">
          <p class="roi-label">5-Year ROI</p>
          <p class="roi-value">{{ fiveYearROI }}%</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { apiService } from "../services/api";
import { useMetricsStore } from "../stores/metricsStore";

interface Metrics {
  cost_saved: number;
}

export default defineComponent({
  name: "CostMeter",
  data() {
    return {
      // metrics: {
      //   cost_saved: 0,
      // } as Metrics,
      // refreshInterval: null as NodeJS.Timeout | null,
      investmentRequired: 2500000, // Default fallback
    };
  },
  computed: {
    paybackMonths(): number {
      const investmentRequired = this.investmentRequired; // ₹25L
      const monthlySavings = this.metrics.cost_saved / 12;
      if (monthlySavings === 0) return 0;
      return Math.round(investmentRequired / monthlySavings);
    },
    fiveYearROI(): number {
      const investmentRequired = this.investmentRequired; // ₹25L
      const fiveYearSavings = this.metrics.cost_saved * 5;
      if (investmentRequired === 0) return 0;
      return Math.round(
        ((fiveYearSavings - investmentRequired) / investmentRequired) * 100
      );
    },
    metrics() {
      return useMetricsStore();
    },
    costSavedLakhs() {
      return useMetricsStore().costSavedLakhs;
    },
  },
  methods: {
    // async fetchMetrics() {
    //   try {
    //     const data = await apiService.getMetrics();
    //     this.metrics = {
    //       cost_saved: data.cost_saved,
    //     };
    //   } catch (error) {
    //     console.error("Error fetching metrics:", error);
    //   }
    // },
    async fetchAppConfig() {
      try {
        const config = await apiService.getConfig();
        this.investmentRequired = config.investment_required;
      } catch (error) {
        console.error("Error fetching config:", error);
      }
    },
  },
  mounted() {
    // Fetch immediately
    //this.fetchMetrics();
    this.fetchAppConfig();
    // Refresh every 3 seconds
    // this.refreshInterval = setInterval(() => {
    //   this.fetchMetrics();
    //   this.fetchAppConfig();
    // }, 3000);
  },
  beforeUnmount() {
    // if (this.refreshInterval) clearInterval(this.refreshInterval);
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

.savings-card {
  background: white;
}

.savings-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 12px;
}

.savings-header {
  display: flex;
  align-items: flex-end;
  gap: 32px;
}

.savings-amount {
  font-size: 48px;
  font-weight: bold;
  color: #001e50;
  line-height: 1;
}

.savings-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #00a86b;
  font-weight: 500;
}

.savings-indicator i {
  font-size: 18px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
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

.breakdown-chart {
  margin-bottom: 20px;
}

.breakdown-item {
  margin-bottom: 16px;
}

.breakdown-label {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 13px;
}

.breakdown-label-name {
  color: #333;
  font-weight: 500;
}

.breakdown-label-value {
  color: #001e50;
  font-weight: 600;
}

.breakdown-bar {
  width: 100%;
  height: 24px;
  background-color: #e8eef5;
  border-radius: 12px;
  overflow: hidden;
}

.breakdown-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #00d4ff, #0099cc);
  border-radius: 12px;
  transition: width 0.5s ease;
}

.breakdown-total {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 2px solid #e8eef5;
}

.breakdown-total-bar {
  width: 100%;
  height: 28px;
  background: linear-gradient(90deg, #001e50, #00d4ff);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  color: white;
  font-weight: 600;
  font-size: 14px;
}

.roi-metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
}

.roi-item {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
  text-align: center;
  border: 1px solid #e8eef5;
}

.scenarios-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}
.scenario-card {
  background: #f5f7fa;
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #e8eef5;
  transition: all 0.3s;
}
.scenario-card:hover {
  border-color: #00d4ff;
  box-shadow: 0 4px 16px rgba(0, 212, 255, 0.15);
}
.scenario-card.recommended {
  background: linear-gradient(135deg, #f0f9ff, #e6f4ff);
  border-color: #00d4ff;
  box-shadow: 0 4px 16px rgba(0, 212, 255, 0.2);
}
.scenario-badge {
  display: inline-block;
  background-color: #00d4ff;
  color: #001e50;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  margin-bottom: 12px;
}
.scenario-title {
  font-size: 16px;
  font-weight: 600;
  color: #001e50;
  margin-bottom: 8px;
}
.scenario-amount {
  font-size: 24px;
  font-weight: bold;
  color: #00d4ff;
  margin-bottom: 8px;
}
.scenario-description {
  font-size: 12px;
  color: #666;
  line-height: 1.5;
}

.roi-label {
  font-size: 12px;
  color: #666;
  margin-bottom: 8px;
  font-weight: 600;
}

.roi-value {
  font-size: 24px;
  font-weight: bold;
  color: #001e50;
}
</style>
