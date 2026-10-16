/**
 * NEXUS Banking AI API Client
 */

const API = {
  async fetchCustomer(customerId) {
    const res = await fetch(`/api/customer/${customerId}`);
    if (!res.ok) throw new Error("Failed to fetch customer profile");
    return await res.json();
  },

  async sendChatMessage(message, customerId, provider = "cognitive", apiKey = "") {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message,
        customer_id: customerId,
        llm_provider: provider,
        api_key: apiKey
      })
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Error processing chat");
    }
    return await res.json();
  },

  async submitApproval(traceId, customerId, action, token, actionType, parameters) {
    const res = await fetch("/api/action/approve", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        trace_id: traceId,
        customer_id: customerId,
        action,
        approval_token: token,
        action_type: actionType,
        parameters
      })
    });
    if (!res.ok) throw new Error("Approval processing failed");
    return await res.json();
  },

  async resetSystem() {
    const res = await fetch("/api/system/reset", { method: "POST" });
    return await res.json();
  },

  async fetchSystemStatus() {
    const res = await fetch("/api/system/status");
    return await res.json();
  },

  async updateLLMConfig(provider, apiKey) {
    const res = await fetch("/api/config/llm", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ provider, api_key: apiKey })
    });
    return await res.json();
  }
};
