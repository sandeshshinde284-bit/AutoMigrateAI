import axios from "axios";

const API_URL = "http://localhost:8000";

interface MetricsResponse {
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

interface MigrationRequest {
  percentage: number;
}

interface MigrationResponse {
  success: boolean;
  migration_percentage: number;
  timestamp: string;
}

// Create axios instance with proper config
const apiClient = axios.create({
  baseURL: API_URL,
  timeout: 5000,
  headers: {
    "Content-Type": "application/json",
  },
});

export const apiService = {
  // Get real metrics from proxy
  async getMetrics(): Promise<MetricsResponse> {
    try {
      console.log("[API] Fetching metrics from:", `${API_URL}/proxy/metrics`);
      const response = await apiClient.get<MetricsResponse>("/proxy/metrics");
      console.log("[API] Metrics received:", response.data);
      return response.data;
    } catch (error) {
      console.error("[API] Error fetching metrics:", error);
      // Return default values if backend not available
      return {
        total_requests: 0,
        legacy_requests: 0,
        cloud_requests: 0,
        error_count: 0,
        legacy_avg_time: 2847,
        cloud_avg_time: 87,
        cost_saved: 0,
        migration_percentage: 0,
        performance_improvement: 0,
      };
    }
  },

  async setMigration(percentage: number): Promise<MigrationResponse> {
    try {
      console.log("[API] Setting migration to:", percentage);
      const response = await apiClient.post<MigrationResponse>(
        "/proxy/set_migration",
        {
          percentage: Math.round(percentage),
        } as MigrationRequest
      );
      console.log("[API] Migration set response:", response.data);
      return response.data;
    } catch (error) {
      console.error("[API] Error setting migration:", error);
      return {
        success: false,
        migration_percentage: 0,
        timestamp: new Date().toISOString(),
      };
    }
  },

  async resetMetrics(): Promise<{ success: boolean }> {
    try {
      console.log("[API] Resetting metrics");
      const response = await apiClient.post("/proxy/reset");
      console.log("[API] Reset response:", response.data);
      return response.data;
    } catch (error) {
      console.error("[API] Error resetting metrics:", error);
      return { success: false };
    }
  },

  async getConfig(): Promise<any> {
    try {
      console.log("[API] Fetching config");
      const response = await apiClient.get("/proxy/config");
      return response.data.config;
    } catch (error) {
      console.error("[API] Error fetching config:", error);
      // Return a fallback on error
      return { investment_required: 2500000 };
    }
  },

  async generateTestRequest(): Promise<any> {
    try {
      console.log("[API] Generating test request");
      const testData = {
        endpoint: "inventory/get_part",
        method: "POST",
        data: {
          part_number: "PART001",
        },
      };
      const response = await apiClient.post("/proxy/request", testData);
      return response.data;
    } catch (error) {
      console.error("[API] Error generating test request:", error);
      return { success: false, error: String(error) };
    }
  },
};
