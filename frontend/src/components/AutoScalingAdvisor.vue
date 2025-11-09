<template>
  <div class="section">
    <div class="page-title">
      <i class="ri-speed-up-line"></i>
      <h1>Auto-Scaling Advisor</h1>
    </div>

    <!-- Current Metrics -->
    <div class="section-card">
      <div class="section-title">
        <i class="ri-bar-chart-line"></i>
        Current Load & Health
      </div>
      <div class="metrics-grid">
        <div class="metric-item">
          <div class="metric-label">Current Load</div>
          <div class="metric-value">{{ metrics.current_load }}</div>
          <div class="metric-unit">req/s</div>
        </div>
        <div class="metric-item">
          <div class="metric-label">Average Load</div>
          <div class="metric-value">{{ metrics.average_load }}</div>
          <div class="metric-unit">req/s</div>
        </div>
        <div class="metric-item">
          <div class="metric-label">Peak Load</div>
          <div class="metric-value">{{ metrics.peak_load }}</div>
          <div class="metric-unit">req/s</div>
        </div>
        <div class="metric-item">
          <div class="metric-label">Health Status</div>
          <div :class="['health-badge', getHealthClass(metrics.health_status)]">
            {{ metrics.health_status }}
          </div>
        </div>
        <div class="metric-item">
          <div class="metric-label">Trend</div>
          <div class="trend-badge">
            <i :class="getTrendIcon(metrics.trend)"></i>
            {{ metrics.trend }}
          </div>
        </div>
      </div>
    </div>

    <!-- Prediction -->
    <div class="section-card prediction-card">
      <div class="section-title">
        <i class="ri-eye-line"></i>
        Traffic Spike Prediction
      </div>

      <div
        v-if="prediction"
        class="prediction-box"
        :class="[prediction.spike_detected ? 'spike-detected' : 'normal']"
      >
        <div class="prediction-header">
          <div class="prediction-icon">
            <i v-if="prediction.spike_detected" class="ri-alert-line"></i>
            <i v-else class="ri-check-line"></i>
          </div>
          <div class="prediction-text">
            <h3>
              {{
                prediction.spike_detected
                  ? "⚠️ Spike Detected!"
                  : "✅ Normal Traffic"
              }}
            </h3>
            <p>
              Current: {{ prediction.current_load }} req/s | Baseline:
              {{ prediction.baseline_load }} req/s
            </p>
            <p v-if="prediction.spike_detected" class="spike-info">
              +{{ prediction.increase_percentage }}% above baseline
            </p>
          </div>
          <div class="confidence">
            <div class="confidence-score">{{ prediction.confidence }}%</div>
            <div class="confidence-label">Confidence</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recommendation -->
    <div v-if="recommendation" class="section-card recommendation-card">
      <div class="section-title">
        <i class="ri-lightbulb-line"></i>
        Scaling Recommendation
      </div>

      <div
        v-if="recommendation"
        class="recommendation-box"
        :class="[getRecommendationClass(recommendation?.action || 'MAINTAIN')]"
      >
        <div class="rec-header">
          <div class="rec-action">{{ recommendation.action }}</div>
          <div class="rec-confidence">
            {{ recommendation.confidence }}% confidence
          </div>
        </div>

        <div class="rec-details">
          <p class="rec-reason">
            {{ recommendation?.reason || "Analyzing traffic patterns..." }}
          </p>

          <div class="capacity-info">
            <div class="capacity-item">
              <span class="label">Current:</span>
              <span class="value"
                >{{ recommendation.current_capacity }} units</span
              >
            </div>
            <div class="capacity-arrow">→</div>
            <div class="capacity-item target">
              <span class="label">Target:</span>
              <span class="value"
                >{{ recommendation.target_capacity }} units</span
              >
            </div>
            <div class="scale-factor">
              <span>{{ recommendation.scale_factor }}x</span>
            </div>
          </div>
        </div>

        <div class="benefits-list">
          <div class="benefit-item">
            <i class="ri-check-line"></i>
            <span>{{
              recommendation?.benefits?.prevents_timeout || "Prevents timeouts"
            }}</span>
          </div>
          <div class="benefit-item">
            <i class="ri-zap-line"></i>
            <span>{{
              recommendation?.benefits?.response_time_improvement ||
              "20% faster response times"
            }}</span>
          </div>
          <div class="benefit-item">
            <i class="ri-wallet-line"></i>
            <span
              >Cost increase:
              {{ recommendation?.benefits?.cost_increase || "~10%" }}</span
            >
          </div>
        </div>
      </div>

      <div class="actions-steps">
        <h4>Recommended Actions:</h4>
        <ol>
          <li v-for="(action, idx) in recommendation?.actions || []" :key="idx">
            {{ action }}
          </li>
        </ol>
      </div>

      <button @click="applyRecommendation" class="btn btn-apply">
        <i class="ri-play-circle-line"></i>
        Apply Scaling Recommendation
      </button>
    </div>

    <!-- Auto-Refresh Info -->
    <div class="section-card info-card">
      <p>
        <i class="ri-info-line"></i>
        Metrics update every 2 seconds. Predictions are based on traffic
        patterns in the last 2 minutes.
      </p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

interface Metrics {
  current_load: number;
  average_load: number;
  peak_load: number;
  health_status: string;
  trend: string;
  data_points: number;
}

interface Prediction {
  spike_detected: boolean;
  current_load: number;
  baseline_load: number;
  increase_percentage: number;
  confidence: number;
  trend: string;
}

interface Recommendation {
  action: string;
  reason: string;
  current_capacity: number;
  target_capacity: number;
  scale_factor: number;
  confidence: number;
  benefits: any;
  actions: string[];
}

export default defineComponent({
  name: "AutoScalingAdvisor",
  data() {
    return {
      metrics: {
        current_load: 0,
        average_load: 0,
        peak_load: 0,
        health_status: "LOADING",
        trend: "STABLE",
        data_points: 0,
      } as Metrics,
      prediction: null as Prediction | null,
      recommendation: null as Recommendation | null,
      refreshInterval: null as NodeJS.Timeout | null,
    };
  },
  methods: {
    async fetchMetrics() {
      try {
        const response = await fetch(
          "http://localhost:8000/proxy/auto-scaling/metrics"
        );
        const data = await response.json();
        if (data.success) {
          this.metrics = data.metrics;
        }
      } catch (error) {
        console.error("[AutoScaling] Error fetching metrics:", error);
      }
    },
    async fetchPrediction() {
      try {
        const response = await fetch(
          "http://localhost:8000/proxy/auto-scaling/predict"
        );
        const data = await response.json();
        if (data.success) {
          this.prediction = data.prediction;
        }
      } catch (error) {
        console.error("[AutoScaling] Error fetching prediction:", error);
      }
    },
    async fetchRecommendation() {
      try {
        const response = await fetch(
          `http://localhost:8000/proxy/auto-scaling/recommendation?capacity=${
            this.metrics.current_load + 50
          }`
        );
        const data = await response.json();
        if (data.success) {
          this.recommendation = data.recommendation;
        }
      } catch (error) {
        console.error("[AutoScaling] Error fetching recommendation:", error);
      }
    },
    applyRecommendation() {
      alert(
        `Scaling to ${this.recommendation?.target_capacity} units applied!\n\nThis would trigger:\n- Provisioning new instances\n- Load balancer updates\n- Health checks`
      );
    },
    getHealthClass(status: string): string {
      switch (status) {
        case "NORMAL":
          return "healthy";
        case "ELEVATED":
          return "warning";
        case "UNDER_LOAD":
          return "critical";
        case "IDLE":
          return "idle";
        default:
          return "unknown";
      }
    },
    getTrendIcon(trend: string): string {
      switch (trend) {
        case "RISING":
          return "ri-arrow-up-line";
        case "FALLING":
          return "ri-arrow-down-line";
        default:
          return "ri-minus-line";
      }
    },
    getRecommendationClass(action: string): string {
      if (action.includes("AGGRESSIVE")) return "urgent";
      if (action.includes("MODERATE")) return "warning";
      if (action.includes("LIGHT")) return "caution";
      return "normal";
    },
  },
  mounted() {
    console.log("[AutoScalingAdvisor] Mounted");
    this.fetchMetrics();
    this.fetchPrediction();
    this.fetchRecommendation();

    this.refreshInterval = setInterval(() => {
      this.fetchMetrics();
      this.fetchPrediction();
      this.fetchRecommendation();
    }, 2000);
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

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
}

.metric-item {
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
  font-weight: 500;
}

.metric-value {
  font-size: 28px;
  font-weight: bold;
  color: #001e50;
  margin-bottom: 4px;
}

.metric-unit {
  font-size: 11px;
  color: #999;
}

.health-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: bold;
}

.health-badge.healthy {
  background: rgba(81, 207, 102, 0.2);
  color: #51cf66;
}

.health-badge.warning {
  background: rgba(255, 153, 68, 0.2);
  color: #ff9944;
}

.health-badge.critical {
  background: rgba(255, 107, 107, 0.2);
  color: #ff6b6b;
}

.health-badge.idle {
  background: rgba(150, 150, 150, 0.2);
  color: #999;
}

.trend-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: 600;
  color: #00d4ff;
}

.prediction-card {
  background: linear-gradient(135deg, #f0f9ff, #f0f4ff);
  border-left: 4px solid #00d4ff;
}

.prediction-box {
  background: white;
  padding: 20px;
  border-radius: 8px;
  border-left: 4px solid;
}

.prediction-box.normal {
  border-left-color: #51cf66;
}

.prediction-box.spike-detected {
  border-left-color: #ff6b6b;
  background: #fff5f5;
}

.prediction-header {
  display: flex;
  gap: 20px;
  align-items: center;
}

.prediction-icon {
  font-size: 32px;
  width: 50px;
  text-align: center;
}

.prediction-box.normal .prediction-icon {
  color: #51cf66;
}

.prediction-box.spike-detected .prediction-icon {
  color: #ff6b6b;
}

.prediction-text {
  flex: 1;
}

.prediction-text h3 {
  margin: 0 0 8px 0;
  font-size: 16px;
  color: #001e50;
}

.prediction-text p {
  margin: 4px 0;
  font-size: 13px;
  color: #666;
}

.spike-info {
  color: #ff6b6b;
  font-weight: bold;
}

.confidence {
  text-align: center;
}

.confidence-score {
  font-size: 24px;
  font-weight: bold;
  color: #00d4ff;
}

.confidence-label {
  font-size: 11px;
  color: #999;
}

.recommendation-card {
  background: linear-gradient(135deg, #fff9f0, #f0f9ff);
}

.recommendation-box {
  background: white;
  padding: 20px;
  border-radius: 8px;
  border-left: 4px solid;
  margin-bottom: 16px;
}

.recommendation-box.urgent {
  border-left-color: #ff6b6b;
  background: #fff5f5;
}

.recommendation-box.warning {
  border-left-color: #ff9944;
  background: #fff9f0;
}

.recommendation-box.caution {
  border-left-color: #ffd666;
  background: #fffbe6;
}

.recommendation-box.normal {
  border-left-color: #51cf66;
  background: #f0fff4;
}

.rec-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid #e8ecf1;
}

.rec-action {
  font-size: 14px;
  font-weight: bold;
  color: #001e50;
}

.rec-confidence {
  font-size: 12px;
  color: #666;
}

.rec-details {
  margin-bottom: 16px;
}

.rec-reason {
  margin: 0 0 12px 0;
  font-size: 13px;
  color: #333;
  line-height: 1.5;
}

.capacity-info {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #f8f9fa;
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 12px;
}

.capacity-item {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.capacity-item.target {
  background: #f0fff4;
  padding: 8px;
  border-radius: 4px;
}

.capacity-item .label {
  font-size: 11px;
  color: #999;
}

.capacity-item .value {
  font-size: 16px;
  font-weight: bold;
  color: #001e50;
}

.capacity-arrow {
  font-size: 20px;
  color: #00d4ff;
  font-weight: bold;
}

.scale-factor {
  background: #00d4ff;
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: bold;
  font-size: 14px;
}

.benefits-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 6px;
  margin-bottom: 16px;
}

.benefit-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 12px;
  color: #333;
}

.benefit-item i {
  color: #51cf66;
  font-weight: bold;
}

.actions-steps {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 6px;
  margin-bottom: 16px;
}

.actions-steps h4 {
  margin: 0 0 12px 0;
  color: #001e50;
  font-size: 13px;
}

.actions-steps ol {
  margin: 0;
  padding-left: 20px;
  list-style: decimal;
}

.actions-steps li {
  margin: 6px 0;
  font-size: 12px;
  color: #666;
  line-height: 1.5;
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

.btn-apply {
  background: linear-gradient(135deg, #00d4ff, #0099cc);
  color: white;
  width: 100%;
  justify-content: center;
}

.btn-apply:hover {
  box-shadow: 0 4px 12px rgba(0, 212, 255, 0.3);
}

.info-card {
  background: linear-gradient(135deg, #f0f9ff, #f9fafc);
  border-left: 4px solid #00d4ff;
  padding: 16px;
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
  font-size: 16px;
}
</style>
