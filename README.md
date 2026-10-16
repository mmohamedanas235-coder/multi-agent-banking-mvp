# NEXUS Core Banking AI — Autonomous Multi-Agent Operational System

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB.svg?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.120+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Status](https://img.shields.io/badge/Architecture-9--Layer%20Compliant-10b981.svg)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg)]()

> A functional, enterprise-grade MVP application demonstrating how specialized autonomous AI agents collaborate within a simulated core banking ecosystem.

---

## 🏛️ Executive Summary & Architectural Blueprint

The application implements the **9-layer enterprise banking architecture** provided in the assignment specification:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. BANKING CHANNELS / USERS (Web Banking, Mobile Simulator, RM Portal)      │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. API & EXPERIENCE LAYER (Session Management, Trace/Correlation ID)        │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. AI GATEWAY / CONTROL PLANE (Zero-Trust PII Redaction, Guardrails, FinOps)│
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. MULTI-AGENT ORCHESTRATOR                                                 │
│    ┌──────────────────────────────────────────────────────────────────┐     │
│    │ Supervisor / Orchestrator Agent                                  │     │
│    │ (Intent Routing, Task Decomposition, Workflow DAG, Aggregation)  │     │
│    └────────────┬──────────────┬──────────────┬─────────────┬─────────┘     │
│                 ▼              ▼              ▼             ▼               │
│         [Customer Agent] [Risk/Fraud]  [Credit/Loan]  [Compliance] ...      │
├─────────────────────────────────────────────────────────────────────────────┤
│ 5. AGENT TOOL / MCP LAYER (Typed Core Banking APIs, Permissions, Audits)    │
├─────────────────────────────────────────────────────────────────────────────┤
│ 6. ENTERPRISE DATA (Core Banking Ledger, Accounts, Transactions, Cards)     │
├─────────────────────────────────────────────────────────────────────────────┤
│ 7. KNOWLEDGE / RAG (Bank Lending Rules, Fraud SOPs, AML BSA Directives)    │
├─────────────────────────────────────────────────────────────────────────────┤
│ 8. EXTERNAL SERVICES (Bureau FICO Pull, OFAC Sanctions, Wire Clearing)      │
├─────────────────────────────────────────────────────────────────────────────┤
│ 9. OBSERVABILITY PLATFORM (Real-Time DAG Graph, Latency, Trajectory, HITL)  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Key Highlights & Differentiators

- **Zero-Dependency Startup (100% Out-of-the-Box)**: Equipped with a Built-in Cognitive Agent Engine that performs authentic chain-of-thought reasoning, tool execution, and response synthesis without requiring external API keys.
- **Pluggable Live LLM Support**: Supports **Google Gemini 2.5 Flash** and **OpenAI GPT-4o** toggleable directly via the UI Settings modal or `.env` configuration.
- **Layer 3 Zero-Trust AI Gateway**:
  - **PII Redaction**: Intercepts and masks SSNs (`[REDACTED-SSN-***-**-XXXX]`), 16-digit card PANs, and CVVs before payloads reach agent logic or external models.
  - **Prompt Injection Defense**: Blocks system prompt extraction, balance tampering, and safety policy overrides.
- **Human-in-the-Loop (HITL) Governance**: High-value wires (≥ $5,000) and AML flags trigger a cryptographic step-up approval card requiring user confirmation before core ledger balances are debited.
- **Interactive FinTech Web Portal**: Real-time 3-column UI featuring live customer portfolios, interactive credit cards (turning RED 🔒 LOCKED upon fraud alert), dynamic SVG Agent DAG visualizer, and step-by-step agent trajectory traces.

---

## 👥 Specialized Agents & Tool Registry

| Agent Name | Primary Responsibilities | Core Tools / MCP APIs |
| :--- | :--- | :--- |
| **Supervisor / Orchestrator** | Intent classification, task decomposition, DAG workflow scheduling, error recovery, response aggregation | Workflow coordinator |
| **Customer Agent** | Customer 360 profile retrieval, account balances, transaction ledgers | `get_customer_360`, `get_account_balance`, `list_transactions` |
| **Risk / Fraud Agent** | Geo-velocity anomaly scoring, device integrity checks, emergency card freeze, dispute ticket creation | `evaluate_fraud_anomalies`, `freeze_card`, `file_fraud_dispute` |
| **Credit & Loan Agent** | Simulated bureau inquiry, Debt-to-Income (DTI) computation, policy RAG retrieval, loan pre-approval amortization | `check_credit_bureau`, `evaluate_loan_underwriting`, `submit_loan_application` |
| **Compliance / AML Agent**| OFAC / PEP sanctions screening, FinCEN Form 112 CTR filings (> $10k), Human-in-the-Loop authorization gate | `screen_aml_compliance`, `search_knowledge_base` |
| **Financial Advisory Agent**| Cashflow optimization, spending analysis, CD yield strategies, budget recommendations | `list_transactions`, `search_knowledge_base` |
| **Notification Agent** | Multi-channel dispatch (Simulated SMS, Mobile Push, Email alerts) with delivery receipts | `send_notification` |

---

## 💼 6 Working Banking Use Cases

### 1. 🚨 Fraud Anomaly Detection & Autonomous Card Lock
- **User Prompt**: *"I didn't authorize a $1,280 charge in London from yesterday! What is that? Help!"*
- **Agent Orchestration**:
  1. Supervisor routes query to **Risk / Fraud Agent**.
  2. Risk Agent queries `evaluate_fraud_anomalies` on checking ledger.
  3. Detects transaction `TXN-9081` ($1,280 at Mayfair Luxury Watches) from London, UK on an unrecognized iPhone 14 (Fraud Score: 92/100).
  4. Autonomously calls `freeze_card` (`CARD-1129` status flips to `LOCKED`).
  5. Calls `file_fraud_dispute` (issues provisional credit under Visa Zero-Liability).
  6. Dispatches emergency SMS/Push via **Notification Agent**.

### 2. 🚗 Real-Time Credit Underwriting & Auto Loan Pre-Approval ($25k)
- **User Prompt**: *"Can I get an auto loan of $25,000 for 48 months?"*
- **Agent Orchestration**:
  1. Supervisor routes to **Customer Agent** (verifies income $185k/yr) and **Credit Agent**.
  2. Credit Agent calls `check_credit_bureau` (FICO: 785 Prime).
  3. Executes RAG search on `POL-CREDIT-001` lending policy.
  4. Calls `evaluate_loan_underwriting` calculating fixed APR (4.89%), monthly installment ($574.49/mo), and projected DTI (7.68%).
  5. Returns formal conditional pre-approval offer.

### 3. 🌐 High-Value International Wire & AML/CTR Gate (HITL)
- **User Prompt**: *"Transfer $15,000 to John Doe in Germany for invoice #9921"*
- **Agent Orchestration**:
  1. Supervisor routes to **Customer Agent** (verifies balance $24,850.40) and **Compliance Agent**.
  2. Compliance Agent runs `screen_aml_compliance` against OFAC SDN and PEP lists (Cleared).
  3. Amount exceeds $10,000 USD: triggers mandatory FinCEN Form 112 Currency Transaction Report (CTR).
  4. Outgoing wire ≥ $5,000 triggers **Human-in-the-Loop** gate.
  5. Generates approval token `APPRV-XXXXXXXX`.
  6. User clicks *"✓ Cryptographically Authorize & Transfer"*; funds are settled in Core Banking.

### 4. 📊 Customer 360 & Multi-Account Spending Audit
- **User Prompt**: *"Give me an overview of my accounts and balance"*
- **Agent Orchestration**: Aggregates balances across Checking ($24.8k) and High-Yield Savings ($85.2k), active credit lines, and auto loan balance.

### 5. 🔒 Lost Card Emergency Lock & Virtual Card Replacement
- **User Prompt**: *"I lost my card at the airport! Block it immediately"*
- **Agent Orchestration**: Deactivates physical card, orders priority replacement, and provisions an instant digital card for Apple/Google Pay.

### 6. 💡 Wealth Optimization & Financial Advisory
- **User Prompt**: *"Analyze my spending and give me recommendations to save $500/month"*
- **Agent Orchestration**: Advisory Agent detects $15k excess idle cash in checking and designs a strategy to sweep $10,000 into a 5.25% APY Certificate of Deposit.

---

## 🛠️ Setup & Execution Instructions

### Prerequisites
- **Python 3.10+** (Tested on Python 3.11.9)
- Operating System: Windows, macOS, or Linux

### 1-Click Launch (Windows)
Double-click `run.bat` or execute in PowerShell:
```powershell
.\run.bat
```

### Manual Launch
1. Clone or navigate to the repository directory:
   ```bash
   cd multi-agent-banking-mvp
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the FastAPI application server:
   ```bash
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```
4. Open your web browser:
   - **Interactive Web Banking Portal**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
   - **Interactive Swagger REST API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 Automated Testing & Verification

The repository includes a comprehensive unit and integration test suite covering database operations, AI Gateway security filters, tool calls, and all core banking workflows:

```bash
python run_tests.py
```

Expected Output:
```text
==================================================
 RUNNING NEXUS MULTI-AGENT BANKING TEST SUITE     
==================================================
 [PASS] 1. Core Banking Database initialization & seed integrity
 [PASS] 2. Layer 3 AI Gateway (PII Redaction & Security Guardrails)
 [PASS] 3. Layer 5 MCP Tool Registry & Banking APIs
 [PASS] 4. Use Case 1: Fraud Anomaly Detection & Autonomous Card Lock
 [PASS] 5. Use Case 2: Credit Underwriting & Instant Loan Offer
 [PASS] 6. Use Case 3: High-Value Wire & AML/CTR Human-in-the-Loop
 [PASS] 7. Full REST API & Chat Orchestration Endpoint
==================================================
 SUCCESS: ALL 7 TESTS PASSED WITH 100% ACCURACY! 
==================================================
```

### End-to-End Walkthrough Script
Run the automated CLI demo script that triggers all 6 scenarios in sequence:
```bash
python demo_walkthrough.py
```

---

## 📂 Project Directory Structure

```
multi-agent-banking-mvp/
├── README.md                     # Comprehensive architecture & setup documentation
├── run.bat                       # 1-click Windows startup script
├── run_tests.py                  # Test runner executing all unit & integration tests
├── demo_walkthrough.py           # Automated CLI demonstration of all 6 banking use cases
├── requirements.txt              # Production dependencies
├── .env.example                  # Environment configuration template
├── app/
│   ├── config.py                 # Application configuration & parameters
│   ├── main.py                   # FastAPI server, REST API endpoints, static mount
│   ├── core/
│   │   ├── models.py             # Domain models (Customer, Account, Trace, Steps, HITL)
│   │   ├── gateway.py            # Layer 3 AI Gateway (PII detection, Guardrails, FinOps)
│   │   └── rag.py                # Layer 7 RAG retriever (BM25 + keyword policy search)
│   ├── data/
│   │   ├── banking_db.py         # Layer 6 Enterprise Data (Core banking store & personas)
│   │   └── knowledge_base.py     # Banking policies (Credit, Fraud, BSA/AML, Rates)
│   ├── tools/
│   │   └── banking_tools.py      # Layer 5 Agent Tool / MCP Layer (13 typed banking tools)
│   ├── agents/
│   │   ├── base_agent.py         # Abstract base agent with logging & tool execution
│   │   └── supervisor.py         # Layer 4 Supervisor Orchestrator Agent
│   ├── llm/
│   │   ├── provider.py           # LLM manager (Cognitive Engine, Gemini, OpenAI)
│   │   └── cognitive_engine.py   # Built-in zero-key multi-agent reasoning engine
│   └── static/
│       ├── index.html            # 3-column responsive FinTech portal
│       ├── css/
│       │   └── style.css         # Dark-mode styling, glassmorphism, animations
│       └── js/
│           ├── api.js            # Frontend REST API client
│           ├── visualizer.js     # Real-time SVG Multi-Agent DAG graph renderer
│           └── app.js            # Portal state, scenario runners, and markdown parser
└── tests/
    ├── __init__.py
    └── test_agents.py            # Unit & integration test cases
```

---

## 🎥 Video Demonstration Script (5–10 Minutes)

When recording your video demo, follow this structured walkthrough:

1. **Architecture Introduction (1–2 min)**:
   - Click the **"🏛️ Architecture"** button in the header.
   - Walk through the 9 layers: Channels, AI Gateway (Layer 3), Multi-Agent Orchestrator (Layer 4), MCP Tools (Layer 5), and Observability Platform (Layer 9).
2. **Core Banking Interface Walkthrough (1 min)**:
   - Introduce customer persona Elena Rostova (Premier Wealth tier, checking/savings balances, active Visa Infinite card).
   - Point out the active AI Gateway status indicator.
3. **Use Case 1: Fraud Anomaly & Immediate Card Freeze (2 min)**:
   - Click Scenario 1 or type: *"I didn't authorize a $1,280 charge in London from yesterday! What is that? Help!"*
   - Highlight the **Supervisor Plan**, **Risk Agent** anomaly scan (Fraud Score 92/100), and card freeze action.
   - Show how the left-hand credit card widget updates live to **🔒 FROZEN / LOCKED**.
   - Show the Notification Agent alert.
4. **Use Case 2: Credit Underwriting & Auto Loan (1.5 min)**:
   - Click Scenario 2: *"Can I get an auto loan of $25,000 for 48 months?"*
   - Show Credit Agent checking credit bureau (785 FICO), retrieving lending policy, calculating 4.89% APR and monthly payments.
5. **Use Case 3: International Wire & Human-in-the-Loop AML Gate (2 min)**:
   - Click Scenario 3: *"Transfer $15,000 to John Doe in Germany for invoice #9921"*
   - Show Compliance Agent checking OFAC sanctions and flagging FinCEN Form 112 CTR filing.
   - Highlight the **Human-in-the-Loop authorization card**.
   - Click **"✓ Cryptographically Authorize & Transfer"** and show the instant settlement and balance update.
6. **Observability & AI Control Plane (1 min)**:
   - Show the dynamic SVG Agent DAG Graph highlighting active nodes.
   - Show latency metrics, token consumption, FinOps cost calculation, and PII masking filter.

---

## 🛡️ Security, Governance & Compliance

- **Zero-Trust PII Redaction**: Sensitive data like Social Security Numbers and card numbers are never passed raw to agent reasoning engines.
- **Audit Trails**: Every MCP tool execution is logged with timestamp, calling agent name, input arguments, execution latency, and return status.
- **Dual-Control HITL**: Financial transactions exceeding policy thresholds cannot be finalized by autonomous agents alone; explicit human step-up tokens are strictly enforced.

---

*Built for the Multi-Agent Banking Assignment • Submission Ready • October 2026*
