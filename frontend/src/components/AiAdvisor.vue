<template>
  <div class="section">
    <div class="page-title">
      <i class="ri-robot-2-line"></i>
      <h1>AI Migration Advisor (Aura)</h1>
    </div>

    <div class="chat-container">
      <div class="chat-history" ref="chatHistory">
        <div
          v-for="(message, index) in history"
          :key="index"
          :class="['chat-message', message.role]"
        >
          <div class="message-bubble">
            <div v-if="message.role === 'model'" class="model-icon">Aura</div>
            <div class="message-text">{{ message.parts[0]?.text }}</div>
          </div>
        </div>
        <div v-if="loading" class="chat-message model">
          <div class="message-bubble">
            <div class="model-icon">Aura</div>
            <div class="message-text typing-indicator">
              <span></span><span></span><span></span>
            </div>
          </div>
        </div>
      </div>

      <div class="chat-input-area">
        <input
          type="text"
          class="chat-input"
          v-model="userPrompt"
          placeholder="Ask about risk, code, or your migration plan..."
          @keyup.enter="sendMessage"
          :disabled="loading"
        />
        <button
          class="send-button"
          @click="sendMessage"
          :disabled="loading || !userPrompt"
        >
          <i class="ri-send-plane-line"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, nextTick } from "vue";
import { apiService } from "../services/api";

interface ChatPart {
  text: string;
}
interface ChatMessage {
  role: "user" | "model";
  parts: ChatPart[];
}

export default defineComponent({
  name: "AiAdvisor",
  data() {
    return {
      userPrompt: "",
      loading: false,
      history: [
        {
          role: "model",
          parts: [
            {
              text: "Hello! I am Aura, your AI Migration Advisor. I have access to your legacy code and migration plan. How can I help you?",
            },
          ],
        },
      ] as ChatMessage[],
    };
  },
  methods: {
    async sendMessage() {
      if (!this.userPrompt || this.loading) return;

      const prompt = this.userPrompt;
      this.history.push({ role: "user", parts: [{ text: prompt }] });
      this.userPrompt = "";
      this.loading = true;
      this.scrollToBottom();

      try {
        // We send the history *except* for the initial welcome message
        const historyForApi = this.history.slice(1);

        const data = await apiService.getAiChatResponse(prompt, historyForApi);

        if (data.success) {
          this.history.push({
            role: "model",
            parts: [{ text: data.response }],
          });
        } else {
          this.history.push({
            role: "model",
            parts: [{ text: `Error: ${data.error}` }],
          });
        }
      } catch (error) {
        this.history.push({
          role: "model",
          parts: [{ text: `Network error: ${String(error)}` }],
        });
      } finally {
        this.loading = false;
        this.scrollToBottom();
      }
    },
    scrollToBottom() {
      nextTick(() => {
        const historyEl = this.$refs.chatHistory as HTMLElement;
        if (historyEl) {
          historyEl.scrollTop = historyEl.scrollHeight;
        }
      });
    },
  },
});
</script>

<style scoped>
.section {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 130px); /* Full viewport height minus padding/header */
}
.page-title {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
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
.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  border: 1px solid #e8eef5;
  overflow: hidden;
}
.chat-history {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.chat-message {
  display: flex;
  max-width: 80%;
}
.chat-message.user {
  align-self: flex-end;
}
.chat-message.model {
  align-self: flex-start;
}
.message-bubble {
  display: flex;
  gap: 10px;
  padding: 12px 16px;
  border-radius: 18px;
  font-size: 14px;
  line-height: 1.6;
}
.chat-message.user .message-bubble {
  background: #00d4ff;
  color: white;
  border-bottom-right-radius: 4px;
}
.chat-message.model .message-bubble {
  background: #f0f4f8;
  color: #333;
  border-bottom-left-radius: 4px;
}
.model-icon {
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #001e50;
  color: #00d4ff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: bold;
}
.message-text {
  padding-top: 4px;
}
.chat-input-area {
  display: flex;
  padding: 16px;
  border-top: 1px solid #e8eef5;
  background: #f8f9fa;
}
.chat-input {
  flex: 1;
  padding: 12px 16px;
  border: 2px solid #e8eef5;
  border-radius: 24px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s ease;
}
.chat-input:focus {
  border-color: #00d4ff;
}
.send-button {
  width: 48px;
  height: 48px;
  margin-left: 12px;
  border: none;
  border-radius: 50%;
  background: #00d4ff;
  color: white;
  font-size: 20px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.send-button:hover:not(:disabled) {
  background: #0099cc;
}
.send-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.typing-indicator span {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #999;
  margin: 0 2px;
  animation: typing 1s infinite;
}
.typing-indicator span:nth-child(2) {
  animation-delay: 0.1s;
}
.typing-indicator span:nth-child(3) {
  animation-delay: 0.2s;
}
@keyframes typing {
  0%,
  100% {
    opacity: 0.3;
  }
  50% {
    opacity: 1;
  }
}
</style>
