/**
 * NEXUS Banking AI Application Logic
 */

let currentCustomerId = "CUST-1001";
let currentProvider = "cognitive";
let customApiKey = "";
let dagVisualizer = null;

// Initialize on DOM load
document.addEventListener("DOMContentLoaded", () => {
  dagVisualizer = new AgentDAGVisualizer("dagSvg");
  initEventListeners();
  loadCustomerData(currentCustomerId);
  refreshSystemStatus();
});

function initEventListeners() {
  // Customer selector
  document.getElementById("customerSelect").addEventListener("change", (e) => {
    currentCustomerId = e.target.value;
    loadCustomerData(currentCustomerId);
    appendSystemNotice(`Switched active banking context to customer ${currentCustomerId}.`);
  });

  // Model selector
  document.getElementById("providerSelect").addEventListener("change", (e) => {
    currentProvider = e.target.value;
    if (currentProvider !== "cognitive" && !customApiKey) {
      openSettingsModal();
    }
  });

  // Chat submit
  const chatForm = document.getElementById("chatForm");
  chatForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const input = document.getElementById("chatInput");
    const msg = input.value.trim();
    if (!msg) return;
    input.value = "";
    handleUserMessage(msg);
  });

  // Quick Scenarios buttons
  document.querySelectorAll(".scenario-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const prompt = btn.getAttribute("data-prompt");
      if (prompt) {
        document.getElementById("chatInput").value = prompt;
        handleUserMessage(prompt);
      }
    });
  });

  // Reset button
  document.getElementById("resetBtn").addEventListener("click", async () => {
    if (confirm("Reset the simulated Core Banking database to initial clean state?")) {
      await API.resetSystem();
      dagVisualizer.reset();
      clearChat();
      await loadCustomerData(currentCustomerId);
      await refreshSystemStatus();
      appendSystemNotice("Core Banking Database and AI Control Plane metrics have been reset.");
    }
  });

  // Nav View Tabs (Swarm Workspace vs 9-Layer Architecture)
  const tabChatBtn = document.getElementById("tabChatBtn");
  const tabArchBtn = document.getElementById("tabArchBtn");
  const chatView = document.getElementById("chatViewWrapper");
  const archView = document.getElementById("archViewWrapper");

  if (tabChatBtn && tabArchBtn && chatView && archView) {
    tabChatBtn.addEventListener("click", () => {
      tabChatBtn.classList.add("active");
      tabArchBtn.classList.remove("active");
      chatView.style.display = "flex";
      archView.style.display = "none";
    });

    tabArchBtn.addEventListener("click", () => {
      tabArchBtn.classList.add("active");
      tabChatBtn.classList.remove("active");
      chatView.style.display = "none";
      archView.style.display = "flex";
    });
  }

  // Settings Modal
  document.getElementById("settingsBtn").addEventListener("click", openSettingsModal);
  document.getElementById("closeSettingsModal").addEventListener("click", closeSettingsModal);
  document.getElementById("saveSettingsBtn").addEventListener("click", () => {
    customApiKey = document.getElementById("apiKeyInput").value.trim();
    currentProvider = document.getElementById("modalProviderSelect").value;
    document.getElementById("providerSelect").value = currentProvider;
    API.updateLLMConfig(currentProvider, customApiKey);
    closeSettingsModal();
    appendSystemNotice(`AI Provider configured to '${currentProvider}'.`);
  });

  // Auto-Play Demo Feature
  let isDemoRunning = false;
  let demoAbort = false;
  const autoDemoBtn = document.getElementById("autoDemoBtn");
  if (autoDemoBtn) {
    autoDemoBtn.addEventListener("click", async () => {
      if (isDemoRunning) {
        demoAbort = true;
        isDemoRunning = false;
        autoDemoBtn.innerHTML = "▶ Auto Demo";
        autoDemoBtn.style.background = "linear-gradient(135deg,#10b981,#059669)";
        appendSystemNotice("Automated demo stopped.");
        return;
      }

      isDemoRunning = true;
      demoAbort = false;
      autoDemoBtn.innerHTML = "⏹️ Stop Demo";
      autoDemoBtn.style.background = "linear-gradient(135deg,#ef4444,#dc2626)";

      const demoPrompts = [
        "I didn't authorize a $1,280 charge in London from yesterday! What is that? Help!",
        "Can I get an auto loan of $25,000 for 48 months?",
        "Transfer $15,000 to John Doe in Germany for invoice #9921",
        "Give me an overview of my accounts and balance",
        "I lost my card at the airport! Block it immediately",
        "Analyze my spending and give me recommendations to save $500/month"
      ];

      for (let i = 0; i < demoPrompts.length; i++) {
        if (demoAbort) break;
        const prompt = demoPrompts[i];
        document.getElementById("chatInput").value = prompt;
        await handleUserMessage(prompt);
        
        // If HITL wire transfer card appeared, auto-approve after 2s
        if (prompt.includes("Transfer $15,000")) {
          await new Promise(r => setTimeout(r, 2000));
          const hitlApproveBtn = document.querySelector(".hitl-actions button.btn-primary");
          if (hitlApproveBtn) hitlApproveBtn.click();
        }

        await new Promise(r => setTimeout(r, 3500));
      }

      isDemoRunning = false;
      autoDemoBtn.innerHTML = "▶ Auto Demo";
      autoDemoBtn.style.background = "linear-gradient(135deg,#10b981,#059669)";
      appendSystemNotice("Automated 6-scenario demonstration completed successfully!");
    });
  }
}

function updateSwarmChips(activeAgents) {
  const chips = {
    chipSupervisor: false,
    chipCustomer: false,
    chipRisk: false,
    chipCredit: false,
    chipCompliance: false,
    chipAdvisory: false,
    chipNotification: false
  };

  (activeAgents || []).forEach(name => {
    const lower = name.toLowerCase();
    if (lower.includes("supervisor")) chips.chipSupervisor = true;
    if (lower.includes("customer")) chips.chipCustomer = true;
    if (lower.includes("risk") || lower.includes("fraud")) chips.chipRisk = true;
    if (lower.includes("credit") || lower.includes("loan")) chips.chipCredit = true;
    if (lower.includes("compliance") || lower.includes("aml")) chips.chipCompliance = true;
    if (lower.includes("advisory")) chips.chipAdvisory = true;
    if (lower.includes("notification")) chips.chipNotification = true;
  });

  Object.keys(chips).forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      if (chips[id]) {
        el.classList.add("active");
      } else {
        el.classList.remove("active");
      }
    }
  });
}

function openSettingsModal() {
  document.getElementById("modalProviderSelect").value = currentProvider;
  document.getElementById("apiKeyInput").value = customApiKey;
  document.getElementById("settingsModal").style.display = "flex";
}

function closeSettingsModal() {
  document.getElementById("settingsModal").style.display = "none";
}

async function loadCustomerData(customerId) {
  try {
    const data = await API.fetchCustomer(customerId);
    const cust = data.customer;
    
    // Update left customer hero card
    document.getElementById("custAvatar").textContent = cust.name.charAt(0);
    document.getElementById("custName").textContent = cust.name;
    document.getElementById("custEmail").textContent = cust.email;
    document.getElementById("custTier").textContent = cust.tier + " TIER";
    document.getElementById("creditScoreVal").textContent = cust.credit_score;

    // Balances
    const chk = cust.accounts.find(a => a.type === "CHECKING" || a.type === "BUSINESS");
    const sav = cust.accounts.find(a => a.type === "SAVINGS");
    
    const chkBal = chk ? chk.balance : 0;
    const savBal = sav ? sav.balance : 0;
    const totalLiquid = chkBal + savBal;
    
    document.getElementById("liquidBalanceVal").textContent = `$${totalLiquid.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
    document.getElementById("checkingBalanceVal").textContent = `$${chkBal.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
    document.getElementById("savingsBalanceVal").textContent = `$${savBal.toLocaleString('en-US', {minimumFractionDigits: 2})}`;

    // Card Widget
    const primaryCard = cust.cards[0] || {};
    const cardEl = document.getElementById("mainCreditCard");
    const cardStatusEl = document.getElementById("cardStatusPill");
    const cardNumEl = document.getElementById("cardNumDisplay");
    
    cardNumEl.textContent = primaryCard.card_number_masked || "**** **** **** 4912";
    if (primaryCard.status === "LOCKED") {
      cardEl.classList.add("locked");
      cardStatusEl.className = "card-status-pill status-locked";
      cardStatusEl.textContent = "🔒 FROZEN / LOCKED";
    } else {
      cardEl.classList.remove("locked");
      cardStatusEl.className = "card-status-pill status-active";
      cardStatusEl.textContent = "● ACTIVE";
    }

    // Transactions list
    renderTransactions(data.transactions);

  } catch (err) {
    console.error("Error loading customer data:", err);
  }
}

function renderTransactions(transactionsMap) {
  const container = document.getElementById("transactionsContainer");
  container.innerHTML = "";
  
  const allTxns = [];
  Object.values(transactionsMap).forEach(list => allTxns.push(...list));
  
  if (allTxns.length === 0) {
    container.innerHTML = `<div style="font-size:0.75rem; color:var(--text-muted); padding:8px;">No recent transactions.</div>`;
    return;
  }

  allTxns.slice(0, 5).forEach(t => {
    const isSuspicious = t.fraud_risk_score >= 60 || t.status === "FLAGGED" || t.status === "DISPUTED";
    const item = document.createElement("div");
    item.style.padding = "8px 10px";
    item.style.borderRadius = "6px";
    item.style.background = isSuspicious ? "rgba(239, 68, 68, 0.12)" : "rgba(15, 23, 42, 0.6)";
    item.style.border = isSuspicious ? "1px solid rgba(239, 68, 68, 0.4)" : "1px solid var(--border-subtle)";
    item.style.display = "flex";
    item.style.justifyContent = "space-between";
    item.style.alignItems = "center";
    item.style.fontSize = "0.75rem";

    item.innerHTML = `
      <div>
        <div style="font-weight:600; color:${isSuspicious ? '#fca5a5' : '#f8fafc'}">${t.merchant}</div>
        <div style="font-size:0.65rem; color:var(--text-muted)">${t.date.split(' ')[0]} • ${t.category}</div>
      </div>
      <div style="text-align:right">
        <div style="font-weight:700; font-family:var(--font-mono); color:${t.type === 'CREDIT' ? '#34d399' : '#f8fafc'}">
          ${t.type === 'CREDIT' ? '+' : '-'}$${t.amount.toLocaleString('en-US', {minimumFractionDigits: 2})}
        </div>
        <span style="font-size:0.6rem; padding:1px 6px; border-radius:4px; ${isSuspicious ? 'background:#ef4444; color:white;' : 'background:rgba(255,255,255,0.06); color:#94a3b8;'}">
          ${isSuspicious ? '⚠️ ' + t.status : 'Score: ' + t.fraud_risk_score}
        </span>
      </div>
    `;
    container.appendChild(item);
  });
}

async function handleUserMessage(message) {
  // Ensure chat view is visible if user was on architecture tab
  const chatView = document.getElementById("chatViewWrapper");
  const archView = document.getElementById("archViewWrapper");
  const tabChatBtn = document.getElementById("tabChatBtn");
  const tabArchBtn = document.getElementById("tabArchBtn");
  if (chatView && archView && tabChatBtn && tabArchBtn) {
    chatView.style.display = "flex";
    archView.style.display = "none";
    tabChatBtn.classList.add("active");
    tabArchBtn.classList.remove("active");
  }

  // Append user message bubble
  appendUserBubble(message);

  // Show typing indicator
  const typingEl = appendTypingIndicator();
  
  // Reset DAG highlighting
  dagVisualizer.reset();

  try {
    const response = await API.sendChatMessage(message, currentCustomerId, currentProvider, customApiKey);
    typingEl.remove();

    if (!response.success) {
      appendSystemNotice(`Error: ${response.error || 'Request could not be completed'}`);
      return;
    }

    const trace = response.trace;

    // Update Observability DAG Visualizer with active agents
    dagVisualizer.highlightAgents(trace.active_agents || []);

    // Update Swarm status banner chips
    updateSwarmChips(trace.active_agents || []);

    // Update Pipeline Stepper badges
    updatePipelineStepper(trace.workflow_dag || []);

    // Update Observability Metrics in Right Pane
    updateObservabilityMetrics(trace);

    // Update Agent Trajectory in Right Pane
    renderAgentTrajectory(trace.steps || []);

    // Append Agent Response message bubble
    appendAgentBubble(trace);

    // Re-sync banking portal state
    await loadCustomerData(currentCustomerId);
    await refreshSystemStatus();

  } catch (err) {
    typingEl.remove();
    appendSystemNotice(`Network/API error: ${err.message}`);
  }
}

function appendUserBubble(text) {
  const stream = document.getElementById("chatStream");
  const bubble = document.createElement("div");
  bubble.className = "message-bubble message-user";
  bubble.textContent = text;
  stream.appendChild(bubble);
  stream.scrollTop = stream.scrollHeight;
}

function appendTypingIndicator() {
  const stream = document.getElementById("chatStream");
  const ind = document.createElement("div");
  ind.className = "message-bubble message-agent";
  ind.innerHTML = `
    <div style="font-size:0.75rem; color:var(--accent-cyan); margin-bottom:4px; font-weight:600;">
      Supervisor Agent analyzing intent...
    </div>
    <div class="typing-indicator">
      <div class="typing-dot"></div>
      <div class="typing-dot"></div>
      <div class="typing-dot"></div>
    </div>
  `;
  stream.appendChild(ind);
  stream.scrollTop = stream.scrollHeight;
  return ind;
}

function appendAgentBubble(trace) {
  const stream = document.getElementById("chatStream");
  const bubble = document.createElement("div");
  bubble.className = "message-bubble message-agent";

  const agentsBadges = (trace.active_agents || [])
    .map(a => `<span class="agent-role-pill">${a}</span>`)
    .join(" ");

  const rawHtml = parseMarkdown(trace.final_response);

  let hitlCardHtml = "";
  if (trace.human_approval_required && trace.human_approval_payload) {
    const payload = trace.human_approval_payload;
    hitlCardHtml = `
      <div class="hitl-card" id="hitl-${trace.trace_id}">
        <div class="hitl-header">
          <span>⚠️</span>
          <span>HUMAN-IN-THE-LOOP AUTHORIZATION REQUIRED</span>
        </div>
        <div style="font-size:0.8rem; color:#f1f5f9;">
          <strong>${payload.title}</strong>
          <p style="margin-top:4px; color:#cbd5e1;">${payload.description}</p>
        </div>
        <div style="font-family:var(--font-mono); font-size:0.7rem; color:var(--accent-amber);">
          Token: ${payload.approval_token} | Security Severity: ${payload.severity}
        </div>
        <div class="hitl-actions">
          <button class="btn-custom btn-primary" onclick="submitHitlAction('${trace.trace_id}', 'APPROVE', '${payload.approval_token}', '${payload.action_type}', ${JSON.stringify(payload.parameters).replace(/"/g, '&quot;')})">
            ✓ Cryptographically Authorize & Transfer
          </button>
          <button class="btn-custom" onclick="submitHitlAction('${trace.trace_id}', 'REJECT', '${payload.approval_token}', '${payload.action_type}', {})">
            ✕ Reject Action
          </button>
        </div>
      </div>
    `;
  }

  bubble.innerHTML = `
    <div class="agent-meta">
      <div class="agent-tag">
        <span>🤖</span>
        <span>NEXUS Multi-Agent Swarm</span>
      </div>
      <div>${agentsBadges}</div>
    </div>
    <div class="markdown-body">
      ${rawHtml}
    </div>
    ${hitlCardHtml}
    <div style="margin-top:12px; font-size:0.68rem; color:var(--text-muted); display:flex; justify-content:space-between; border-top:1px solid rgba(255,255,255,0.06); padding-top:6px;">
      <span>Trace: <code>${trace.trace_id}</code></span>
      <span>Guardrails: ${trace.guardrail_report.prompt_safe ? '✅ Clean' : '⚠️ Flagged'} • Latency: ${trace.execution_time_ms}ms</span>
    </div>
  `;

  stream.appendChild(bubble);
  stream.scrollTop = stream.scrollHeight;
}

window.submitHitlAction = async function(traceId, action, token, actionType, params) {
  const hitlEl = document.getElementById(`hitl-${traceId}`);
  if (hitlEl) {
    hitlEl.innerHTML = `<div style="font-size:0.8rem; color:var(--accent-cyan);">Processing human authorization decision: ${action}...</div>`;
  }

  try {
    const res = await API.submitApproval(traceId, currentCustomerId, action, token, actionType, params);
    if (hitlEl) {
      if (action === "APPROVE") {
        hitlEl.style.borderColor = "#10b981";
        hitlEl.style.background = "rgba(16, 185, 129, 0.1)";
        hitlEl.innerHTML = `
          <div style="color:#34d399; font-weight:700; font-size:0.85rem;">✅ Transfer Cryptographically Approved & Settled</div>
          <div style="font-size:0.75rem; color:#cbd5e1; margin-top:4px;">${res.message}</div>
        `;
      } else {
        hitlEl.style.borderColor = "#f43f5e";
        hitlEl.style.background = "rgba(244, 63, 94, 0.1)";
        hitlEl.innerHTML = `
          <div style="color:#f87171; font-weight:700; font-size:0.85rem;">✕ Transaction Declined by Account Holder</div>
          <div style="font-size:0.75rem; color:#cbd5e1; margin-top:4px;">${res.message}</div>
        `;
      }
    }
    // Refresh balances and transactions
    await loadCustomerData(currentCustomerId);
  } catch (err) {
    if (hitlEl) {
      hitlEl.innerHTML = `<div style="color:#f87171;">Authorization error: ${err.message}</div>`;
    }
  }
};

function updatePipelineStepper(dagList) {
  const stepper = document.getElementById("pipelineStepper");
  if (!dagList || dagList.length === 0) return;
  
  stepper.innerHTML = dagList.map((step, idx) => `
    <div class="step-badge ${idx === dagList.length - 1 ? 'completed' : 'active'}">
      <span>${idx + 1}.</span>
      <span>${step}</span>
    </div>
  `).join("");
}

function updateObservabilityMetrics(trace) {
  document.getElementById("traceIdDisplay").textContent = trace.trace_id;
  document.getElementById("latencyMetricVal").textContent = `${trace.execution_time_ms} ms`;
  document.getElementById("tokensMetricVal").textContent = `${trace.token_usage.total_tokens || 0}`;
  document.getElementById("costMetricVal").textContent = `$${(trace.token_usage.estimated_cost_usd || 0).toFixed(6)}`;

  // Guardrail metrics
  const piiCount = trace.guardrail_report.pii_detected.length;
  document.getElementById("piiRedactedMetricVal").textContent = piiCount > 0 ? `${piiCount} Redacted` : "0 (Clean)";
}

function renderAgentTrajectory(steps) {
  const container = document.getElementById("trajectoryList");
  container.innerHTML = "";

  if (steps.length === 0) {
    container.innerHTML = `<div style="font-size:0.75rem; color:var(--text-muted)">No steps recorded for this trace.</div>`;
    return;
  }

  steps.forEach(step => {
    const el = document.createElement("div");
    el.className = "trajectory-step";

    let typeClass = "type-thought";
    if (step.step_type === "TOOL_CALL") typeClass = "type-tool";
    if (step.step_type === "GUARDRAIL") typeClass = "type-guardrail";
    if (step.step_type === "HUMAN_ESCALATION") typeClass = "type-hitl";

    let toolDetailsHtml = "";
    if (step.tool_name) {
      toolDetailsHtml = `
        <div class="tool-payload-box">
          <div><strong style="color:var(--accent-amber)">Tool:</strong> ${step.tool_name}</div>
          <div><strong style="color:#94a3b8">Args:</strong> ${JSON.stringify(step.tool_args)}</div>
          ${step.tool_result ? `<div><strong style="color:#34d399">Result:</strong> ${JSON.stringify(step.tool_result)}</div>` : ''}
        </div>
      `;
    }

    el.innerHTML = `
      <div class="trajectory-step-header">
        <span style="color:var(--text-primary)">${step.agent_name}</span>
        <span class="step-type-pill ${typeClass}">${step.step_type}</span>
      </div>
      <div style="font-weight:600; font-size:0.78rem; color:var(--accent-cyan); margin-bottom:2px;">
        ${step.title}
      </div>
      <div style="color:var(--text-secondary); line-height:1.4;">
        ${step.content}
      </div>
      ${toolDetailsHtml}
      <div style="font-size:0.62rem; color:var(--text-muted); margin-top:4px; text-align:right;">
        ${step.timestamp}
      </div>
    `;

    container.appendChild(el);
  });
}

async function refreshSystemStatus() {
  try {
    const status = await API.fetchSystemStatus();
    document.getElementById("toolsRegisteredVal").textContent = status.tools_registered_count;
    document.getElementById("totalPiiVal").textContent = status.total_pii_redacted;
  } catch (err) {
    console.error("Status fetch error", err);
  }
}

function appendSystemNotice(text) {
  const stream = document.getElementById("chatStream");
  const el = document.createElement("div");
  el.style.textAlign = "center";
  el.style.fontSize = "0.75rem";
  el.style.color = "var(--text-muted)";
  el.style.margin = "8px 0";
  el.textContent = `— ${text} —`;
  stream.appendChild(el);
  stream.scrollTop = stream.scrollHeight;
}

function clearChat() {
  const stream = document.getElementById("chatStream");
  stream.innerHTML = `
    <div style="text-align: center; padding: 24px; color: var(--text-secondary);">
      <div style="font-size: 2rem; margin-bottom: 8px;">🏛️</div>
      <h3 style="font-size: 1.1rem; color: #fff; margin-bottom: 4px;">NEXUS Multi-Agent Banking Assistant</h3>
      <p style="font-size: 0.8rem; max-width: 480px; margin: 0 auto;">
        Ask a question or select one of the pre-loaded 1-click test scenarios on the left to watch multiple specialized AI agents collaborate with live Core Banking APIs.
      </p>
    </div>
  `;
}

// Lightweight, safe Markdown Parser
function parseMarkdown(md) {
  if (!md) return "";
  let html = md
    // Escape HTML
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    // Headers
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/^#### (.*$)/gim, '<h4>$1</h4>')
    // Bold & Italics
    .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/gim, '<em>$1</em>')
    // Blockquotes
    .replace(/^&gt; (.*$)/gim, '<blockquote>$1</blockquote>')
    // Inline code
    .replace(/`([^`]+)`/gim, '<code>$1</code>');

  // Simple Markdown Table conversion
  if (html.includes("|")) {
    const lines = html.split("\n");
    let inTable = false;
    let tableHtml = "<table><tbody>";
    const processedLines = [];

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();
      if (line.startsWith("|") && line.endsWith("|")) {
        if (!inTable) {
          inTable = true;
          tableHtml = "<table><tbody>";
        }
        if (line.includes("---")) continue; // Skip header divider
        
        const cols = line.split("|").filter((c, idx, arr) => idx > 0 && idx < arr.length - 1);
        tableHtml += "<tr>" + cols.map(c => `<td>${c.trim()}</td>`).join("") + "</tr>";
      } else {
        if (inTable) {
          tableHtml += "</tbody></table>";
          processedLines.push(tableHtml);
          inTable = false;
        }
        processedLines.push(line);
      }
    }
    if (inTable) {
      tableHtml += "</tbody></table>";
      processedLines.push(tableHtml);
    }
    html = processedLines.join("\n");
  }

  // Lists
  html = html.replace(/^\s*-\s+(.*$)/gim, '<li>$1</li>');
  html = html.replace(/^\s*([0-9]+)\.\s+(.*$)/gim, '<li><strong>$1.</strong> $2</li>');
  // Newlines
  html = html.replace(/\n\n/g, '<br/><br/>');

  return html;
}
