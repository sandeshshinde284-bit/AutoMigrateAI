import { defineStore } from "pinia";
import { apiService } from "../services/api"; // Adjust path as needed

// Define the Metrics interface
interface MetricsState {
  total_requests: number;
  legacy_requests: number;
  cloud_requests: number;
  error_count: number;
  legacy_avg_time: number;
  cloud_avg_time: number;
  cost_saved: number;
  migration_percentage: number;
  performance_improvement: number;
}

export const useMetricsStore = defineStore("metrics", {
  // 1. STATE: The single source of truth
  state: (): MetricsState => ({
    total_requests: 0,
    legacy_requests: 0,
    cloud_requests: 0,
    error_count: 0,
    legacy_avg_time: 2847, // Default
    cloud_avg_time: 87, // Default
    cost_saved: 0,
    migration_percentage: 0,
    performance_improvement: 0,
  }),

  // 2. GETTERS: Your computed properties
  getters: {
    performanceGain: (state): number => {
      if (state.cloud_avg_time === 0) return 0;
      return Math.round(state.legacy_avg_time / state.cloud_avg_time);
    },
    costSavedLakhs: (state): number => {
      return Math.round(state.cost_saved / 100000);
    },
  },

  // 3. ACTIONS: Your methods to change the state
  actions: {
    async fetchMetrics() {
      try {
        const data = await apiService.getMetrics();
        // $patch updates the state with the new data
        this.$patch(data);
        console.log("[Pinia] Metrics updated:", this.migration_percentage);
      } catch (error) {
        console.error("[Pinia] Error fetching metrics:", error);
      }
    },
  },
});
