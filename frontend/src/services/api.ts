import axios from "axios";

//local
// const API_URL = "http://localhost:8000";

// This is the SINGLE source of truth for your backend URL
const API_URL =
  "https://automigrateai-service-157263375859.us-central1.run.app";

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

// Create axios instance
const apiClient = axios.create({
  baseURL: API_URL,
  timeout: 10000, // Increased timeout for AI calls
  headers: {
    "Content-Type": "application/json",
  },
});

// --- HELPER for handling errors ---
const handleApiError = (error: any, functionName: string): any => {
  console.error(`[API] Error in ${functionName}:`, error);
  if (axios.isAxiosError(error) && error.code === "ERR_BAD_RESPONSE") {
    // Handle 500-level errors from the server
    return {
      success: false,
      error: error.response?.data?.error || "Internal Server Error",
    };
  }
  // Handle network errors (CORS, connection refused)
  return { success: false, error: error.message || "Network Error" };
};

export const apiService = {
  // --- Pinia / Control Panel ---
  async getMetrics(): Promise<MetricsResponse> {
    try {
      const response = await apiClient.get<MetricsResponse>("/proxy/metrics");
      console.log("[API] Metrics received:", response.data);
      return response.data;
    } catch (error) {
      handleApiError(error, "getMetrics");
      // Return defaults on error
      return {
        total_requests: 0,
        legacy_requests: 0,
        cloud_requests: 0,
        error_count: 0,
        legacy_avg_time: 0,
        cloud_avg_time: 0,
        cost_saved: 0,
        migration_percentage: 0,
        performance_improvement: 0,
      };
    }
  },

  async setMigration(percentage: number): Promise<MigrationResponse> {
    const response = await apiClient.post<MigrationResponse>(
      "/proxy/set_migration",
      { percentage: Math.round(percentage) } as MigrationRequest
    );
    return response.data;
  },

  async resetMetrics(): Promise<{ success: boolean }> {
    const response = await apiClient.post("/proxy/reset");
    return response.data;
  },

  async generateTestRequest(): Promise<any> {
    const testData = {
      endpoint: "inventory/get_part",
      method: "POST",
      data: { part_number: "PART001" },
    };
    const response = await apiClient.post("/proxy/request", testData);
    return response.data;
  },

  async saveMigrationPlan(planData: any): Promise<any> {
    const response = await apiClient.post("/proxy/plan/save", planData);
    return response.data;
  },

  // --- CostMeter ---
  async getConfig(): Promise<any> {
    try {
      const response = await apiClient.get("/proxy/config");
      return response.data.config;
    } catch (error) {
      handleApiError(error, "getConfig");
      return { investment_required: 2500000 }; // Fallback
    }
  },

  // --- RequestHistory ---
  async fetchRequestHistory(limit: number = 30): Promise<any> {
    try {
      const response = await apiClient.get(`/proxy/history?limit=${limit}`);
      return response.data;
    } catch (error) {
      return handleApiError(error, "fetchRequestHistory");
    }
  },

  // --- CodeAnalyzer ---
  async analyzeCode(file: string): Promise<any> {
    try {
      const response = await apiClient.post("/proxy/analyze-code", { file });
      return response.data;
    } catch (error) {
      return handleApiError(error, "analyzeCode");
    }
  },

  // --- DigitalTwinValidator ---
  async validateMigration(
    percentage: number,
    duration: number,
    traffic_volume: number
  ): Promise<any> {
    try {
      const response = await apiClient.post("/proxy/validate-migration", {
        percentage,
        duration,
        traffic_volume,
      });
      return response.data;
    } catch (error) {
      return handleApiError(error, "validateMigration");
    }
  },
  async fetchNextStep(current: number): Promise<any> {
    try {
      const response = await apiClient.get(
        `/proxy/next-migration-step?current=${current}`
      );
      return response.data;
    } catch (error) {
      return handleApiError(error, "fetchNextStep");
    }
  },

  // --- AutoScalingAdvisor ---
  async fetchAutoScalingMetrics(): Promise<any> {
    try {
      const response = await apiClient.get("/proxy/auto-scaling/metrics");
      return response.data;
    } catch (error) {
      return handleApiError(error, "fetchAutoScalingMetrics");
    }
  },
  async fetchAutoScalingPrediction(): Promise<any> {
    try {
      const response = await apiClient.get("/proxy/auto-scaling/predict");
      return response.data;
    } catch (error) {
      return handleApiError(error, "fetchAutoScalingPrediction");
    }
  },
  async fetchAutoScalingRecommendation(capacity: number): Promise<any> {
    try {
      const response = await apiClient.get(
        `/proxy/auto-scaling/recommendation?capacity=${capacity}`
      );
      return response.data;
    } catch (error) {
      return handleApiError(error, "fetchAutoScalingRecommendation");
    }
  },

  // --- ComplianceCard ---
  async fetchComplianceStatus(): Promise<any> {
    try {
      const response = await apiClient.get("/proxy/compliance/status");
      return response.data;
    } catch (error) {
      return handleApiError(error, "fetchComplianceStatus");
    }
  },
  async runComplianceCheck(request: any, response: any): Promise<any> {
    try {
      const resp = await apiClient.post("/proxy/compliance/check", {
        request,
        response,
      });
      return resp.data;
    } catch (error) {
      return handleApiError(error, "runComplianceCheck");
    }
  },
};
