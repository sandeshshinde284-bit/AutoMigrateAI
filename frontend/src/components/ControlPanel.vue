<template>
  <div class="section">
    <div class="page-title">
      <i class="ri-settings-3-line"></i>
      <h1>Migration Control Center</h1>
    </div>

    <!-- Global Migration Control -->
    <div class="section-card">
      <div class="section-title">
        <i class="ri-gamepad-line"></i>
        Global Migration Control
      </div>

      <!-- Slider -->
      <div class="slider-section">
        <label class="slider-label">
          Migration Percentage:
          <strong class="migration-percentage">{{ currentMigration }}%</strong>
        </label>
        <input
          type="range"
          v-model.number="sliderValue"
          min="0"
          max="100"
          class="migration-slider"
          @input="updateMigration"
        />
        <p class="slider-info">
          <strong>Legacy:</strong> {{ 100 - currentMigration }}% |
          <strong>Cloud:</strong> {{ currentMigration }}%
        </p>
      </div>
    </div>
    <!-- Subsystem Priority -->
    <div class="section-card">
      <div class="section-title">
        <i class="ri-settings-line"></i>
        Subsystem Priority (Planning)
      </div>
      <div class="control-item-list">
        <div class="control-item">
          <div class="control-label">
            <span class="control-name">Engine Management</span>
            <span class="priority-tag priority-high">High</span>
          </div>
          <div class="slider-container">
            <input type="range" min="0" max="100" value="85" class="slider" />
            <span class="slider-value">85%</span>
          </div>
        </div>
        <div class="control-item">
          <div class="control-label">
            <span class="control-name">Infotainment</span>
            <span class="priority-tag priority-medium">Medium</span>
          </div>
          <div class="slider-container">
            <input type="range" min="0" max="100" value="60" class="slider" />
            <span class="slider-value">60%</span>
          </div>
        </div>
        <div class="control-item">
          <div class="control-label">
            <span class="control-name">Diagnostics</span>
            <span class="priority-tag priority-low">Low</span>
          </div>
          <div class="slider-container">
            <input type="range" min="0" max="100" value="35" class="slider" />
            <span class="slider-value">35%</span>
          </div>
        </div>
      </div>
    </div>
    <!-- Resource Allocation -->
    <div class="section-card">
      <div class="section-title">
        <i class="ri-database-2-line"></i>
        Resource Allocation
      </div>
      <div class="resource-items">
        <div class="resource-item">
          <div class="resource-header">
            <span class="resource-name">Development</span>
            <span class="resource-percentage">40%</span>
          </div>
          <input
            type="range"
            min="0"
            max="100"
            value="40"
            class="resource-slider"
          />
        </div>
        <div class="resource-item">
          <div class="resource-header">
            <span class="resource-name">Testing</span>
            <span class="resource-percentage">35%</span>
          </div>
          <input
            type="range"
            min="0"
            max="100"
            value="35"
            class="resource-slider"
          />
        </div>
        <div class="resource-item">
          <div class="resource-header">
            <span class="resource-name">Deployment</span>
            <span class="resource-percentage">25%</span>
          </div>
          <input
            type="range"
            min="0"
            max="100"
            value="25"
            class="resource-slider"
          />
        </div>
      </div>
    </div>
    <!-- Schedule Adjustment -->
    <div class="section-card">
      <div class="section-title">
        <i class="ri-calendar-line"></i>
        Schedule Adjustment
      </div>

      <div class="schedule-grid">
        <div class="calendar-section">
          <div class="calendar">
            <div class="calendar-header">
              <span class="calendar-month" ref="calendarMonth"></span>
              <div class="calendar-nav">
                <button @click="prevMonth">&lt;</button>
                <button @click="nextMonth">&gt;</button>
              </div>
            </div>

            <div class="calendar-weekdays">
              <div class="weekday">Sun</div>
              <div class="weekday">Mon</div>
              <div class="weekday">Tue</div>
              <div class="weekday">Wed</div>
              <div class="weekday">Thu</div>
              <div class="weekday">Fri</div>
              <div class="weekday">Sat</div>
            </div>

            <div class="calendar-days" ref="calendarDays"></div>
          </div>
        </div>

        <div class="time-inputs">
          <div class="input-group">
            <label class="input-label">Start Time</label>
            <input type="time" class="input-field" value="09:00" />
          </div>
          <div class="input-group">
            <label class="input-label">End Time</label>
            <input type="time" class="input-field" value="17:00" />
          </div>
          <div class="input-group">
            <label class="input-label">Migration Window (Days)</label>
            <input type="number" class="input-field" value="14" />
          </div>
        </div>
      </div>
    </div>
    <!-- Control Buttons -->
    <div class="button-group">
      <button
        @click="startMigration"
        :disabled="isRunning || currentMigration === 100"
        class="btn btn-start"
      >
        <i class="ri-play-line"></i> START
      </button>
      <button
        @click="pauseMigration"
        :disabled="!isRunning"
        class="btn btn-pause"
      >
        <i class="ri-pause-line"></i> PAUSE
      </button>
      <button @click="rollback" class="btn btn-rollback">
        <i class="ri-arrow-go-back-line"></i> ROLLBACK
      </button>
      <button @click="reset" class="btn btn-reset">
        <i class="ri-refresh-line"></i> RESET
      </button>
    </div>
    <!-- Status Message -->
    <div class="status-text">{{ statusMessage }}</div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from "vue";
import { apiService } from "../services/api";
import { useMetricsStore } from "../stores/metricsStore";

export default defineComponent({
  name: "ControlPanel",
  emits: ["update:migration"],
  data() {
    return {
      sliderValue: 0 as number,
      isRunning: false as boolean,
      autoIncrement: null as ReturnType<typeof setInterval> | null,
      currentCalendarDate: new Date() as Date,
      selectedDay: null as number | null,
      selectedMonth: new Date().getMonth() as number,
      selectedYear: new Date().getFullYear() as number,
      _calendarClickHandler: null as any,
      autoIncrementCount: 0,
    };
  },
  setup() {
    const metricsStore = useMetricsStore();
    const currentMigration = computed(() => {
      return metricsStore.migration_percentage;
    });

    return {
      currentMigration,
    };
  },
  computed: {
    statusMessage(): string {
      if (this.isRunning) return "⏳ Migration in progress...";
      if (this.currentMigration === 0) return "✅ Ready to start migration";
      if (this.currentMigration === 100)
        return "✅ Migration complete - 100% cloud";
      return `⏸️ Paused at ${this.currentMigration}%`;
    },
  },
  watch: {
    currentMigration(newPercentage: number) {
      if (!this.isRunning) {
        this.sliderValue = newPercentage;
      }
    },
  },
  methods: {
    async startMigration() {
      this.isRunning = true;
      this.autoIncrementCount = 0;
      this.autoIncrement = setInterval(async () => {
        let newMigrationValue = this.currentMigration + 1;

        if (newMigrationValue >= 100) {
          newMigrationValue = 100;
          this.isRunning = false;
          if (this.autoIncrement) clearInterval(this.autoIncrement);
        }

        // Update local slider
        this.sliderValue = newMigrationValue;
        // Send to backend
        await apiService.setMigration(newMigrationValue);
        this.autoIncrementCount++;
        // Every 10 ticks (which is 5 seconds), send a test request
        if (this.autoIncrementCount % 10 === 0 && newMigrationValue < 100) {
          console.log(
            `[ControlPanel] Auto-migration at ${newMigrationValue}%: Sending test request.`
          );
          await apiService.generateTestRequest();
        }
        this.$emit("update:migration");
      }, 500);
    },

    pauseMigration() {
      this.isRunning = false;
      if (this.autoIncrement) {
        clearInterval(this.autoIncrement);
        this.autoIncrement = null;
      }
    },

    async rollback() {
      this.isRunning = false;
      if (this.autoIncrement) {
        clearInterval(this.autoIncrement);
        this.autoIncrement = null;
      }
      this.sliderValue = 0;
      await apiService.setMigration(0);
      this.$emit("update:migration");
      console.log("[ControlPanel] Rolled back to 0%");
    },

    async reset() {
      this.isRunning = false;
      if (this.autoIncrement) {
        clearInterval(this.autoIncrement);
        this.autoIncrement = null;
      }
      this.sliderValue = 0;
      await apiService.setMigration(0);
      this.$emit("update:migration");
      console.log("[ControlPanel] Reset to 0%");
    },

    async updateMigration() {
      if (this.autoIncrement) {
        clearInterval(this.autoIncrement);
        this.autoIncrement = null;
        this.isRunning = false;
      }
      await apiService.setMigration(this.sliderValue);
      this.$emit("update:migration");
      console.log("[ControlPanel] Manual update:", this.sliderValue);
    },

    getDaysInMonth(date: Date) {
      return new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
    },

    getFirstDayOfMonth(date: Date) {
      return new Date(date.getFullYear(), date.getMonth(), 1).getDay();
    },

    prevMonth() {
      this.currentCalendarDate = new Date(
        this.currentCalendarDate.getFullYear(),
        this.currentCalendarDate.getMonth() - 1
      );
      this.renderCalendar();
    },

    nextMonth() {
      this.currentCalendarDate = new Date(
        this.currentCalendarDate.getFullYear(),
        this.currentCalendarDate.getMonth() + 1
      );
      this.renderCalendar();
    },

    renderCalendar() {
      const date = this.currentCalendarDate;
      const year = date.getFullYear();
      const month = date.getMonth();

      const monthEl = this.$refs.calendarMonth as HTMLElement;
      const daysEl = this.$refs.calendarDays as HTMLElement;

      if (!monthEl || !daysEl) {
        return;
      }

      const monthNames = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
      ];

      monthEl.textContent = `${monthNames[month]} ${year}`;

      const firstDay = this.getFirstDayOfMonth(this.currentCalendarDate);
      const daysInMonth = this.getDaysInMonth(this.currentCalendarDate);

      daysEl.innerHTML = "";

      // Get today's date for comparison
      const today = new Date();
      const todayDate = new Date(
        today.getFullYear(),
        today.getMonth(),
        today.getDate()
      );

      // Add padding for previous month's days
      for (let i = 0; i < firstDay; i++) {
        const dayEl = document.createElement("div");
        dayEl.classList.add("calendar-day", "other-month");
        daysEl.appendChild(dayEl);
      }

      // Add days for the current month
      for (let i = 1; i <= daysInMonth; i++) {
        const dayEl = document.createElement("div");
        dayEl.classList.add("calendar-day");
        dayEl.textContent = i.toString();
        dayEl.dataset.day = String(i);
        dayEl.dataset.month = String(month);
        dayEl.dataset.year = String(year);

        // Check if this day is in the past
        const currentDayDate = new Date(year, month, i);
        const isPastDay = currentDayDate < todayDate;

        if (isPastDay) {
          dayEl.classList.add("other-month");
          dayEl.style.color = "#ccc";
          dayEl.style.backgroundColor = "#f9fafb";
          dayEl.style.cursor = "not-allowed";
          dayEl.style.borderColor = "transparent";
          dayEl.style.pointerEvents = "none";
        } else {
          // Check if this is today
          const isToday =
            i === today.getDate() &&
            month === today.getMonth() &&
            year === today.getFullYear();

          if (isToday) {
            dayEl.classList.add("today");
          }

          // Check if this day is selected
          const isSelectedDay =
            i === this.selectedDay &&
            month === this.selectedMonth &&
            year === this.selectedYear;

          if (isSelectedDay) {
            dayEl.classList.add("selected");
            // ALSO ADD INLINE STYLES as backup
            dayEl.style.background =
              "linear-gradient(135deg, #00d4ff 0%, #0099cc 100%)";
            dayEl.style.color = "white";
            dayEl.style.borderColor = "#0099cc";
            dayEl.style.fontWeight = "700";
            dayEl.style.boxShadow = "0 6px 16px rgba(0, 212, 255, 0.4)";
            dayEl.style.transform = "scale(1.05)";
            dayEl.style.zIndex = "10";
          }
        }

        daysEl.appendChild(dayEl);
      }

      // Setup event delegation
      if (this._calendarClickHandler) {
        daysEl.removeEventListener("click", this._calendarClickHandler);
      }

      this._calendarClickHandler = (event: MouseEvent) => {
        const target = event.target as HTMLElement;
        const dayEl = target.closest(
          ".calendar-day:not(.other-month)"
        ) as HTMLElement;

        if (!dayEl) return;

        const day = parseInt(dayEl.dataset.day || "0");
        const clickMonth = parseInt(dayEl.dataset.month || "0");
        const clickYear = parseInt(dayEl.dataset.year || "0");

        this.selectedDay = day;
        this.selectedMonth = clickMonth;
        this.selectedYear = clickYear;

        this.renderCalendar();
      };

      daysEl.addEventListener("click", this._calendarClickHandler);
    },
  },

  mounted() {
    this.sliderValue = this.currentMigration;

    this.$nextTick(() => {
      this.renderCalendar();

      // Update planning slider values
      const planningSliders = this.$el.querySelectorAll(
        ".slider-container .slider"
      );

      planningSliders.forEach((slider: any) => {
        slider.addEventListener("input", () => {
          const value = slider.value;
          const sliderValueEl =
            slider.parentElement.querySelector(".slider-value");
          if (sliderValueEl) sliderValueEl.textContent = value + "%";
        });
      });

      // Update resource slider values
      const resourceSliders = this.$el.querySelectorAll(".resource-slider");
      resourceSliders.forEach((slider: any) => {
        slider.addEventListener("input", () => {
          const value = slider.value;
          const percentageEl = slider.parentElement.querySelector(
            ".resource-percentage"
          );
          if (percentageEl) percentageEl.textContent = value + "%";
        });
      });
    });
  },

  beforeUnmount() {
    if (this.autoIncrement) clearInterval(this.autoIncrement);

    if (this._calendarClickHandler && this.$refs.calendarDays) {
      (this.$refs.calendarDays as HTMLElement).removeEventListener(
        "click",
        this._calendarClickHandler
      );
    }
  },
});
</script>

<style>
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
  gap: 8px;
}

.section-title i {
  color: #00d4ff;
  font-size: 18px;
}

.slider-section {
  margin-bottom: 25px;
}

.slider-label {
  display: block;
  margin-bottom: 10px;
  font-weight: 600;
  color: #333;
}

.migration-percentage {
  color: #00d4ff;
}

.migration-slider {
  width: 100%;
  height: 8px;
  cursor: pointer;
  accent-color: #00d4ff;
}

.slider-info {
  font-size: 12px;
  color: #7a8a9a;
  margin-top: 8px;
}

.button-group {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin-bottom: 20px;
}

.btn {
  padding: 12px 16px;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-start {
  background: #51cf66;
  color: white;
}

.btn-start:hover:not(:disabled) {
  background: #40c057;
  box-shadow: 0 4px 12px rgba(81, 207, 102, 0.3);
}

.btn-pause {
  background: #ffa94d;
  color: white;
}

.btn-pause:hover:not(:disabled) {
  background: #ff9500;
}

.btn-rollback {
  background: #ff6b6b;
  color: white;
}

.btn-rollback:hover:not(:disabled) {
  background: #ff5252;
}

.btn-reset {
  background: #868e96;
  color: white;
}

.btn-reset:hover:not(:disabled) {
  background: #748087;
}

.status-text {
  text-align: center;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 6px;
  font-weight: 600;
  color: #001e50;
}

/* CONTROL ITEMS */
.control-item-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.control-item {
  margin-bottom: 0;
}

.control-label {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.control-name {
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.priority-tag {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.priority-high {
  background-color: #001e50;
  color: white;
}

.priority-medium {
  background-color: #b3d9ff;
  color: #001e50;
}

.priority-low {
  background-color: #d4d4d4;
  color: #666;
}

.slider-container {
  display: flex;
  align-items: center;
  gap: 12px;
}

.slider {
  flex: 1;
  height: 6px;
  border-radius: 3px;
  background: #e8eef5;
  outline: none;
  -webkit-appearance: none;
  appearance: none;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background-color: #00d4ff;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.slider::-webkit-slider-thumb:hover {
  transform: scale(1.1);
}

.slider::-moz-range-thumb {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background-color: #00d4ff;
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.slider-value {
  font-size: 14px;
  font-weight: 500;
  color: #001e50;
  min-width: 40px;
  text-align: right;
}

/* RESOURCE ALLOCATION */
.resource-items {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.resource-item {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.resource-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.resource-name {
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.resource-percentage {
  font-size: 16px;
  font-weight: 600;
  color: #00d4ff;
}

.resource-slider {
  height: 8px;
  border-radius: 4px;
  background: #e8eef5;
  outline: none;
  -webkit-appearance: none;
  appearance: none;
}

.resource-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background-color: #001e50;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.resource-slider::-webkit-slider-thumb:hover {
  background-color: #00d4ff;
  transform: scale(1.1);
}

.resource-slider::-moz-range-thumb {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background-color: #001e50;
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* ============================================ */
/* CALENDAR STYLES - CRITICAL SECTION */
/* ============================================ */

.schedule-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.calendar-section {
  display: flex;
  flex-direction: column;
}

.calendar {
  border: 2px solid #e8ecf1;
  border-radius: 12px;
  padding: 20px;
  background: linear-gradient(135deg, #f9fafb 0%, #f0f4f8 100%);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 2px solid #e8ecf1;
}

.calendar-month {
  font-size: 18px;
  font-weight: 700;
  color: #001e50;
  letter-spacing: 0.5px;
}

.calendar-nav {
  display: flex;
  gap: 8px;
}

.calendar-nav button {
  width: 36px;
  height: 36px;
  border: 2px solid #e8ecf1;
  background-color: white;
  border-radius: 8px;
  cursor: pointer;
  color: #001e50;
  font-size: 16px;
  font-weight: 700;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.calendar-nav button:hover {
  background-color: #00d4ff;
  border-color: #00d4ff;
  color: white;
  box-shadow: 0 4px 12px rgba(0, 212, 255, 0.3);
  transform: translateY(-2px);
}

.calendar-nav button:active {
  transform: translateY(0);
}

.calendar-weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
  margin-bottom: 12px;
}

.weekday {
  text-align: center;
  font-size: 13px;
  font-weight: 700;
  color: #001e50;
  padding: 10px 0;
  text-transform: uppercase;
  letter-spacing: 1px;
  background: linear-gradient(135deg, #e8ecf1 0%, #d4dce8 100%);
  border-radius: 6px;
}

.calendar-days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
}

/* BASE CALENDAR DAY */
.calendar-day {
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  color: #333;
  background-color: white;
  border: 2px solid #e8ecf1;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  user-select: none;
}

/* HOVER STATE - ONLY FOR ACTIVE DAYS */
.calendar-day:not(.other-month):hover {
  background-color: #f0f4f8;
  border-color: #00d4ff;
  color: #001e50;
  box-shadow: 0 4px 12px rgba(0, 212, 255, 0.15);
  transform: translateY(-2px);
}

/* TODAY INDICATOR */
.calendar-day.today {
  border: 2px solid #00d4ff;
  font-weight: 700;
  color: #00d4ff;
  background-color: rgba(0, 212, 255, 0.05);
}

/* ⭐ SELECTED STATE - HIGHEST PRIORITY */
.calendar-day.selected {
  background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%) !important;
  color: white !important;
  border-color: #0099cc !important;
  font-weight: 700 !important;
  box-shadow: 0 6px 16px rgba(0, 212, 255, 0.4) !important;
  transform: scale(1.05) !important;
  z-index: 10 !important;
}

.calendar-day.selected::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: 8px;
  box-shadow: inset 0 0 0 2px rgba(255, 255, 255, 0.3);
  pointer-events: none;
}

.calendar-day.selected:hover {
  background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%) !important;
  color: white !important;
  border-color: #0099cc !important;
  transform: scale(1.05) !important;
}

/* DISABLED DAYS */
.calendar-day.other-month {
  color: #ccc;
  background-color: #f9fafb;
  cursor: not-allowed;
  border-color: transparent;
  pointer-events: none;
}

/* TIME INPUTS */
.time-inputs {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.input-label {
  font-size: 13px;
  font-weight: 700;
  color: #001e50;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.input-field {
  padding: 12px 16px;
  border: 2px solid #e8ecf1;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #333;
  background-color: white;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.input-field:hover {
  border-color: #b3d9ff;
  box-shadow: 0 2px 8px rgba(0, 212, 255, 0.1);
}

.input-field:focus {
  outline: none;
  border-color: #00d4ff;
  background-color: #f9fafb;
  box-shadow: 0 0 0 4px rgba(0, 212, 255, 0.15);
}

/* RESPONSIVE */
@media (max-width: 768px) {
  .schedule-grid {
    grid-template-columns: 1fr;
  }

  .calendar {
    padding: 16px;
  }

  .calendar-month {
    font-size: 16px;
  }

  .calendar-nav button {
    width: 32px;
    height: 32px;
  }

  .calendar-day {
    font-size: 12px;
  }
}
</style>
