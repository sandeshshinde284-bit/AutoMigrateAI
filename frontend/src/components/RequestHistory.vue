<template>
  <div class="section">
    <div class="page-title">
      <i class="ri-history-line"></i>
      <h1>Request History & Rollback</h1>
    </div>

    <!-- Rollback Info -->
    <div class="section-card rollback-card">
      <div class="section-title">
        <i class="ri-time-travel-line"></i>
        Debug Time Machine - Instant Rollback
      </div>
      <div class="rollback-info">
        <p><strong>Total Requests Tracked:</strong> {{ totalRequests }}</p>
        <p><strong>Last Request:</strong> {{ lastRequestTime }}</p>
        <p><strong>Current Migration:</strong> {{ currentMigration }}%</p>
        <button
          @click="executeRollback"
          class="btn btn-rollback-action"
          :disabled="currentMigration === 0"
        >
          <i class="ri-arrow-go-back-line"></i> ROLLBACK TO 0%
        </button>
      </div>
    </div>

    <!-- Request History Table -->
    <div class="section-card">
      <div class="section-title">
        <i class="ri-list-check-3"></i>
        Recent Requests (Click to Select)
      </div>
      <div class="history-table-wrapper">
        <table class="history-table">
          <thead>
            <tr>
              <th>Select</th>
              <th>ID</th>
              <th>Time</th>
              <th>Endpoint</th>
              <th>Source</th>
              <th>Response Time</th>
              <th>Status</th>
              <th>Migration %</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="req in requestHistory"
              :key="req.id"
              @click="selectRequest(req)"
              :class="[
                'history-row',
                { selected: selectedRequest?.id === req.id },
              ]"
            >
              <td>
                <input
                  type="radio"
                  :value="req.id"
                  v-model="selectedRequestId"
                  @click.stop
                />
              </td>
              <td>{{ req.id }}</td>
              <td class="time-cell">{{ formatTime(req.timestamp) }}</td>
              <td class="endpoint-cell">{{ req.endpoint }}</td>
              <td>
                <span :class="['source-badge', req.source]">{{
                  req.source
                }}</span>
              </td>
              <td class="time-value">{{ req.response_time }}ms</td>
              <td>
                <span
                  :class="['status-badge', req.error ? 'error' : 'success']"
                >
                  {{ req.error ? "❌ Error" : "✅ OK" }}
                </span>
              </td>
              <td>{{ req.migration_percentage }}%</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Request Details -->
    <div v-if="selectedRequest" class="section-card">
      <div class="section-title">
        <i class="ri-information-line"></i>
        Selected Request Details (ID: {{ selectedRequest.id }})
      </div>
      <div class="request-details">
        <div class="detail-section">
          <h4>Request Data</h4>
          <pre>{{ JSON.stringify(selectedRequest.request_data, null, 2) }}</pre>
        </div>
        <div class="detail-section">
          <h4>Response Data</h4>
          <pre>{{
            JSON.stringify(selectedRequest.response_data, null, 2)
          }}</pre>
        </div>
        <div class="detail-section">
          <h4>Metadata</h4>
          <p><strong>Endpoint:</strong> {{ selectedRequest.endpoint }}</p>
          <p><strong>Source:</strong> {{ selectedRequest.source }}</p>
          <p>
            <strong>Response Time:</strong>
            {{ selectedRequest.response_time }}ms
          </p>
          <p><strong>Timestamp:</strong> {{ selectedRequest.timestamp }}</p>
          <p><strong>Error:</strong> {{ selectedRequest.error || "None" }}</p>
          <p>
            <strong>Migration %:</strong>
            {{ selectedRequest.migration_percentage }}%
          </p>
        </div>
      </div>
    </div>

    <!-- Status Message -->
    <div
      v-if="rollbackMessage"
      :class="['status-message', rollbackMessage.type]"
    >
      {{ rollbackMessage.text }}
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { apiService } from "../services/api";
import { useMetricsStore } from "../stores/metricsStore";

interface Request {
  id: number;
  timestamp: string;
  endpoint: string;
  source: string;
  response_time: number;
  error: string | null;
  request_data: any;
  response_data: any;
  migration_percentage: number;
}

interface RollbackMessage {
  type: "success" | "error" | "info";
  text: string;
}

export default defineComponent({
  name: "RequestHistory",
  data() {
    return {
      requestHistory: [] as Request[],
      selectedRequest: null as Request | null,
      selectedRequestId: null as number | null,
      refreshInterval: null as ReturnType<typeof setInterval> | null,
      totalRequests: 0,
      //currentMigration: 0,
      rollbackMessage: null as RollbackMessage | null,
    };
  },
  computed: {
    lastRequestTime(): string {
      if (this.requestHistory.length === 0) return "N/A";
      return this.formatTime(this.requestHistory[0]!.timestamp);
    },
    currentMigration() {
      return useMetricsStore().migration_percentage;
    },
  },
  methods: {
    async fetchRequestHistory() {
      try {
        // const response = await fetch(
        //   "http://localhost:8000/proxy/history?limit=30"
        // );
        // const data = await response.json();
        const data = await apiService.fetchRequestHistory(30);
        if (data.success) {
          this.requestHistory = data.history;
          this.totalRequests = data.total_requests;
          console.log(
            "[RequestHistory] Fetched:",
            data.history.length,
            "requests"
          );
        }
      } catch (error) {
        console.error("[RequestHistory] Error:", error);
      }
    },
    // async fetchCurrentMigration() {
    //   try {
    //     const response = await fetch("http://localhost:8000/proxy/metrics");
    //     const data = await response.json();
    //     this.currentMigration = data.migration_percentage;
    //   } catch (error) {
    //     console.error("[RequestHistory] Error fetching migration:", error);
    //   }
    // },
    selectRequest(req: Request) {
      this.selectedRequest = req;
      this.selectedRequestId = req.id;
    },
    // async executeRollback() {
    //   if (!this.selectedRequest) {
    //     this.showMessage("Please select a request", "error");
    //     return;
    //   }

    //   try {
    //     const response = await fetch("http://localhost:8000/proxy/rollback", {
    //       method: "POST",
    //       headers: { "Content-Type": "application/json" },
    //       body: JSON.stringify({
    //         request_id: this.selectedRequest.id,
    //       }),
    //     });

    //     const data = await response.json();

    //     if (data.success) {
    //       this.showMessage(
    //         `✅ Rollback successful! Rolled back ${data.rolled_back_request_count} requests`,
    //         "success"
    //       );
    //       // Refresh history after rollback
    //       setTimeout(() => this.fetchRequestHistory(), 500);
    //     } else {
    //       this.showMessage(`❌ Rollback failed: ${data.message}`, "error");
    //     }
    //   } catch (error) {
    //     this.showMessage(`❌ Error: ${error}`, "error");
    //   }
    // },
    async executeRollback() {
      // We can just roll back to 0, no need to select a request
      // if (!this.selectedRequest) {
      //   this.showMessage("Please select a request", "error");
      //   return;
      // }

      try {
        // 1. ACTUALLY set the migration back to 0
        await apiService.setMigration(0);

        // 2. FORCE the Pinia store to update immediately
        useMetricsStore().fetchMetrics();

        // 3. Show success
        this.showMessage(
          `✅ Rollback successful! Migration set to 0%`,
          "success"
        );

        // 4. Refresh the history table
        setTimeout(() => this.fetchRequestHistory(), 500);
      } catch (error) {
        this.showMessage(`❌ Error: ${String(error)}`, "error");
      }
    },
    formatTime(timestamp: string): string {
      try {
        const date = new Date(timestamp);
        return date.toLocaleTimeString();
      } catch {
        return timestamp;
      }
    },
    showMessage(text: string, type: "success" | "error" | "info") {
      this.rollbackMessage = { text, type };
      setTimeout(() => {
        this.rollbackMessage = null;
      }, 5000);
    },
  },
  mounted() {
    console.log("[RequestHistory] Mounted");
    this.fetchRequestHistory();
    // this.fetchCurrentMigration();

    this.refreshInterval = setInterval(() => {
      this.fetchRequestHistory();
      //this.fetchCurrentMigration();
    }, 2000);
  },
  beforeUnmount() {
    console.log("[RequestHistory] Unmounting");
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

.rollback-card {
  background: linear-gradient(135deg, #f0f4ff, #f9fafc);
  border-left: 4px solid #00d4ff;
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

.rollback-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.rollback-info p {
  margin: 0;
  font-size: 14px;
  color: #333;
}

.rollback-info strong {
  color: #001e50;
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

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-rollback-action {
  background: #ff6b6b;
  color: white;
  width: fit-content;
}

.btn-rollback-action:hover:not(:disabled) {
  background: #ff5252;
  box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3);
}

.history-table-wrapper {
  overflow-x: auto;
}

.history-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
}

.history-table thead {
  background-color: #f8fafc;
  border-bottom: 2px solid #e8ecf1;
}

.history-table th {
  padding: 12px;
  text-align: left;
  font-weight: 600;
  color: #333;
}

.history-table td {
  padding: 10px 12px;
  border-bottom: 1px solid #e8ecf1;
  color: #666;
}

.history-row {
  cursor: pointer;
  transition: all 0.2s ease;
}

.history-row:hover {
  background-color: #f9fafb;
}

.history-row.selected {
  background-color: rgba(0, 212, 255, 0.1);
  border-left: 3px solid #00d4ff;
}

.time-cell {
  font-family: "Courier New", monospace;
  font-size: 11px;
}

.endpoint-cell {
  font-weight: 500;
  color: #001e50;
}

.source-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 10px;
  font-weight: bold;
  display: inline-block;
}

.source-badge.legacy {
  background: rgba(255, 107, 107, 0.2);
  color: #ff6b6b;
}

.source-badge.cloud {
  background: rgba(81, 207, 102, 0.2);
  color: #51cf66;
}

.time-value {
  font-family: "Courier New", monospace;
  font-weight: bold;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 10px;
  font-weight: bold;
}

.status-badge.success {
  background: rgba(81, 207, 102, 0.2);
  color: #51cf66;
}

.status-badge.error {
  background: rgba(255, 107, 107, 0.2);
  color: #ff6b6b;
}

.request-details {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.detail-section {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
  border-left: 3px solid #00d4ff;
}

.detail-section h4 {
  margin: 0 0 12px 0;
  color: #001e50;
  font-size: 14px;
}

.detail-section pre {
  margin: 0;
  background: white;
  padding: 12px;
  border-radius: 4px;
  overflow-x: auto;
  font-size: 11px;
  color: #333;
  border: 1px solid #e8ecf1;
}

.detail-section p {
  margin: 8px 0;
  font-size: 13px;
  color: #666;
}

.detail-section strong {
  color: #001e50;
}

.status-message {
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 24px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 10px;
}

.status-message.success {
  background: rgba(81, 207, 102, 0.15);
  color: #51cf66;
  border-left: 4px solid #51cf66;
}

.status-message.error {
  background: rgba(255, 107, 107, 0.15);
  color: #ff6b6b;
  border-left: 4px solid #ff6b6b;
}

.status-message.info {
  background: rgba(0, 212, 255, 0.15);
  color: #00d4ff;
  border-left: 4px solid #00d4ff;
}
</style>
