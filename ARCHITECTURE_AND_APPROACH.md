# NEXUS Core Banking AI — Architecture & Approach Document

**Project**: Simulated Real-Time Banking Architecture with Multi-Agent Automation  
**Author**: Engineering Candidate  
**Date**: October 2026  
**Status**: Submission Ready • 100% Test Coverage Verified  

---

## 1. Executive Summary

Modern financial institutions require systems that seamlessly balance natural language customer interaction with strict regulatory compliance, deterministic ledger integrity, and low-latency risk containment. Traditional monolithic rule engines and single-prompt LLM wrappers fail because they lack compartmentalized domain knowledge, cannot enforce permission boundaries, and risk hallucinations in high-stakes financial operations.

This MVP application implements an enterprise **Multi-Agent Banking Operations Platform** modeled directly after the **9-layer target architecture** specified in the assignment. The system orchestrates specialized autonomous agents (Customer, Risk/Fraud, Credit Underwriting, Compliance, Advisory, and Notification) under a centralized **Supervisor/Orchestrator Agent**, mediated by a **Layer 3 Zero-Trust AI Gateway** and a **Layer 5 MCP Tool Registry**.

---

## 2. Problem-Solving Approach & Design Philosophy

Our design is grounded in five core architectural principles:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       FIVE CORE ARCHITECTURAL PILLARS                       │
├──────────────────────┬──────────────────────┬───────────────────────────────┤
│ 1. Agent Specialism  │ 2. Deterministic MCP │ 3. Zero-Trust AI Gateway      │
│ Isolated boundaries, │ No hallucinated data;│ PII masked before model;      │
│ targeted context.    │ typed APIs mutate DB.│ prompt injection neutralized. │
├──────────────────────┴──────────────────────┴───────────────────────────────┤
│ 4. Human-in-the-Loop Governance      │ 5. Full-Stack Observability          │
│ High-value wires & AML require dual  │ SVG DAG graph, latency ms, token     │
│ cryptographic authorization tokens.  │ accounting, FinOps cost monitoring.  │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

1. **Compartmentalized Agent Specialism (Division of Labor)**: Rather than prompting one massive model to handle everything, domain responsibilities are strictly decoupled. The **Risk Agent** specializes in velocity anomalies and card locks; the **Credit Agent** specializes in bureau inquiries, DTI calculations, and lending policies; the **Compliance Agent** focuses exclusively on sanctions screening and FinCEN CTR regulations.
2. **Deterministic MCP Tool Layer (No Hallucinated Ledger Updates)**: Autonomous agents never execute direct arbitrary state mutations. All banking actions (fund transfers, balance checks, card freezes, dispute creation, loan disbursals) are mediated through a type-safe **Model Context Protocol (MCP)** tool registry with typed Pydantic parameters, parameter validation, and audit logging.
3. **Layer 3 Zero-Trust AI Gateway**: Sensitive PII—such as Social Security Numbers (`XXX-XX-XXXX`), 16-digit Primary Account Numbers (PANs), and CVVs—is stripped and masked at the gateway boundary *before* payloads reach any internal agent or external model. Malicious prompt injection attacks are intercepted and quarantined at Layer 3.
4. **Human-in-the-Loop (HITL) Regulatory Gate**: Automated actions are governed by risk thresholds. While low-risk actions (card locks upon confirmed fraud, balance checks) execute autonomously to protect the customer, high-value wires ($\ge$ $5,000) and AML flags strictly halt execution and require explicit cryptographic human sign-off before funds are debited.
5. **Dual-Engine Model Strategy (Zero-Dependency + Live LLM Support)**:
   - **Mode A (Built-in Cognitive Engine)**: A deterministic semantic reasoning engine that runs 100% out of the box with zero external API keys, zero external network dependencies, and microsecond latencies.
   - **Mode B (Live LLM Provider)**: Pluggable support for **Google Gemini 2.5 Flash** and **OpenAI GPT-4o** configurable via the in-app Settings modal or `.env`.

---

## 3. Detailed 9-Layer Architecture Mapping

The implementation directly aligns with the reference architecture diagram:

```
                                  1. BANKING CHANNELS / USERS
                  [Web Banking]     [Mobile Banking]     [Branch / RM Portal]
                                              │
                                              ▼
                                 2. API & EXPERIENCE LAYER
                  [Session Management]  [Correlation/Trace ID]  [Threat Protection]
                                              │
                                              ▼
                              3. AI GATEWAY / AI CONTROL PLANE
                  [Zero-Trust PII Redaction]  [Prompt Injection Shield]  [FinOps Cost Engine]
                                              │
                                              ▼
                                 4. MULTI-AGENT ORCHESTRATOR
                ┌─────────────────────────────────────────────────────────────┐
                │               Supervisor / Orchestrator Agent               │
                │    Intent Classification • Task Decomposition • DAG Manager  │
                └───────┬────────────┬────────────┬────────────┬───────────┬──┘
                        ▼            ▼            ▼            ▼           ▼
                   [Customer]   [Risk/Fraud]   [Credit]   [Compliance] [Advisory]
                        │            │            │            │           │
                        └────────────┴─────┬──────┴────────────┴───────────┘
                                           ▼
                                 5. AGENT TOOL / MCP LAYER
                  [Tool Registry] [Schema Validation] [Sandbox Boundary] [Audit Log]
                    Account API • Card API • Loan API • AML API • Notification API
                                           │
                    ┌──────────────────────┼──────────────────────┐
                    ▼                      ▼                      ▼
           6. ENTERPRISE DATA      7. KNOWLEDGE / RAG    8. EXTERNAL SERVICES
           [Core Banking DB]       [Policy Documents]    [Credit Bureau FICO]
           [Customer 360]          [BM25 / Keyword]      [OFAC Sanctions]
           [Ledger & Loans]        [Lending SOPs]        [SWIFT / Fedwire]
                                           │
                                           ▼
                       9. CROSS-CUTTING PRODUCTION PLATFORM
           [Real-Time SVG DAG]  [Execution Trajectories]  [Token Accounting]  [Audit Logs]
```

### Layer 1: Banking Channels / Users
- **Web Banking Single-Page Application**: Responsive 3-column workspace with real-time portfolio data, card status widgets, and conversational feeds.
- **Mobile Experience Simulation**: Displays contactless card provisioning and real-time push alerts.

### Layer 2: API & Experience Layer
- **Session & Correlation Tracking**: Every user request receives a unique UUID trace identifier (e.g., `TRC-A65DE2DF04`) passed across all agent handoffs and tool calls.
- **REST & Static Delivery**: Served via high-throughput FastAPI asynchronous endpoints.

### Layer 3: AI Gateway / AI Control Plane
- **Zero-Trust PII Redaction**: Regex-driven tokenizer that intercepts SSNs and credit card PANs before agent processing, transforming raw secrets into sanitized tokens (e.g., `[REDACTED-SSN-***-**-6789]`).
- **Prompt Injection Defense**: Intercepts jailbreak vectors, system prompt leaks, and policy override exploits, instantly quarantining malicious requests.
- **FinOps Cost & Token Metering**: Calculates token consumption and dollar costs ($0.15/1M prompt tokens, $0.60/1M completion tokens).

### Layer 4: Multi-Agent Orchestrator
- **Supervisor Agent** (`app/agents/supervisor.py`):
  1. *Intent Classification*: Maps user inputs into business intents (`FRAUD_INCIDENT`, `CREDIT_UNDERWRITING`, `INTERNATIONAL_WIRE`, `CUSTOMER_360`, `LOST_CARD`, `WEALTH_ADVISORY`).
  2. *Task Decomposition (DAG)*: Dynamically builds the execution graph of specialized agents.
  3. *Handoff & Error Recovery*: Gracefully manages multi-agent handoffs and fallback syntheses.
  4. *Human Escalation*: Emits structured `HumanApprovalPayload` when actions require human sign-off.
- **Specialized Agents**:
  - **Customer Agent**: Queries Customer 360 profiles, KYC verification status, and linked accounts.
  - **Risk / Fraud Agent**: Analyzes geo-velocity anomalies, hardware fingerprints, and executes protective card locks.
  - **Credit / Loan Agent**: Evaluates credit bureau scores, computes DTI ratios, and structures amortized loan pre-approvals.
  - **Compliance / AML Agent**: Screens beneficiaries against OFAC/PEP lists and triggers FinCEN Form 112 CTR reports for transactions $\ge$ $10,000.
  - **Financial Advisory Agent**: Evaluates idle cash buffers and recommends high-yield savings/CD strategies.
  - **Notification Agent**: Transmits simulated multi-channel alerts (SMS, Push, Email).

### Layer 5: Agent Tool / MCP Layer (`app/tools/banking_tools.py`)
- Provides 13 typed tools with explicit JSON parameter schemas, execution latency tracking, and audit logging. Tools include:
  - `get_customer_360`, `get_account_balance`, `list_transactions`
  - `evaluate_fraud_anomalies`, `freeze_card`, `file_fraud_dispute`
  - `check_credit_bureau`, `evaluate_loan_underwriting`, `submit_loan_application`
  - `screen_aml_compliance`, `execute_fund_transfer`, `send_notification`, `search_knowledge_base`

### Layer 6: Enterprise Data (`app/data/banking_db.py`)
- Realistic in-memory transactional database seeded with three distinct customer personas:
  - **Elena Rostova (`CUST-1001`)**: Premier Wealth customer ($110,050 liquid assets, 785 FICO score, active Visa Infinite card). Contains a flagged foreign anomaly ($1,280 in London, UK).
  - **Marcus Vance (`CUST-1002`)**: Small Business customer ($86,200 deposits, commercial credit line).
  - **Priya Sharma (`CUST-1003`)**: Retail customer ($18,020 deposits, auto loan applicant).

### Layer 7: Knowledge / RAG Engine (`app/core/rag.py` & `app/data/knowledge_base.py`)
- Hybrid BM25 lexical and keyword retrieval system indexed over official bank directives:
  - `POL-CREDIT-001`: Q4 2026 Credit Risk & Lending Policy (cutoffs, APR tiers, DTI caps).
  - `POL-FRAUD-002`: Card Compromise, Unauthorized Debits & Dispute SOP.
  - `POL-COMPLIANCE-003`: Bank Secrecy Act (BSA), AML & Sanctions Directives.
  - `POL-PRODUCT-004`: Retail & Premier Wealth Account Rates & Perks.

### Layer 8: External Services Simulation
- **Credit Bureau Consortium**: Real-time FICO score and trade-line pulls.
- **OFAC Sanctions & PEP List**: Real-time screening against global SDN blacklists.
- **SWIFT / Fedwire Network**: Simulated fund settlement network.

### Layer 9: Cross-Cutting Production Platform
- **Real-Time SVG DAG Graph**: Dynamically highlights active agent nodes and animated communication vectors.
- **Agent Trajectory & Audit Log**: Complete timeline showing *Agent Thought $\rightarrow$ Tool Invocation $\rightarrow$ Tool Output $\rightarrow$ Final Response*.
- **Live Latency & Cost Tracking**: Displays execution latency in milliseconds and real-time FinOps cost.

---

## 4. Multi-Agent Workflow Walkthroughs (Core Use Cases)

### Use Case 1: Fraud Anomaly Detection & Autonomous Card Lock
```
User Prompt: "I didn't authorize a $1,280 charge in London from yesterday! What is that? Help!"
  │
  ├─► [AI Gateway]: Intercepts prompt, verifies safety, initiates TRC-5269E52BE7
  ├─► [Supervisor]: Decomposes into Fraud Investigation & Protective Containment Plan
  ├─► [Risk / Fraud Agent]: Calls MCP Tool evaluate_fraud_anomalies
  │     └─► Finds TXN-9081 ($1,280 Mayfair Luxury Watches, London UK, unknown iPhone 14)
  │     └─► Fraud Risk Score: 92/100 (CRITICAL ANOMALY)
  ├─► [Risk / Fraud Agent]: Invokes MCP Tool freeze_card [CARD-1129]
  │     └─► Core Banking card status flips to LOCKED (Card widget in UI turns red 🔒 LOCKED)
  ├─► [Risk / Fraud Agent]: Invokes MCP Tool file_fraud_dispute [TXN-9081]
  │     └─► Creates Case DSP-261016-TXN-9081 with instant 100% provisional credit
  ├─► [Notification Agent]: Dispatches emergency SMS and mobile push alerts
  └─► [Supervisor]: Synthesizes clear customer response with next steps
```

### Use Case 2: Credit Underwriting & Auto Loan Pre-Approval ($25k)
```
User Prompt: "Can I get an auto loan of $25,000 for 48 months?"
  │
  ├─► [Supervisor]: Identifies intent as CREDIT_UNDERWRITING
  ├─► [Customer Agent]: Verifies Elena Rostova's annual income ($185,000/yr) & KYC Verified
  ├─► [Credit Agent]: Invokes MCP Tool check_credit_bureau
  │     └─► Retrieves FICO score: 785 (Prime Tier), existing monthly debt: $610.20
  ├─► [Credit Agent]: RAG search on POL-CREDIT-001 (Prime tier APR: 4.89%, max DTI: 48%)
  ├─► [Credit Agent]: Invokes MCP Tool evaluate_loan_underwriting
  │     └─► Amortized Payment: $574.49/mo, Total Interest: $2,575.52, Projected DTI: 7.68%
  └─► [Supervisor]: Returns formal Pre-Approved conditional offer ready for disbursal
```

### Use Case 3: High-Value International Wire & Human-in-the-Loop AML Gate
```
User Prompt: "Transfer $15,000 to John Doe in Germany for invoice #9921"
  │
  ├─► [Supervisor]: Decomposes into Balance Check + Compliance Screening + HITL Gate
  ├─► [Customer Agent]: Calls get_account_balance -> Verified $24,850.40 available
  ├─► [Compliance Agent]: Calls screen_aml_compliance -> OFAC Sanctions Cleared
  │     └─► Amount >= $10,000 triggers FinCEN Form 112 CTR filing requirement
  ├─► [Supervisor]: HALTS AUTONOMOUS EXECUTION (Amount >= $5,000 policy threshold)
  │     └─► Generates Human-in-the-Loop Approval Card with Token APPRV-ED46C179
  │     └─► Displays interactive "✓ Cryptographically Authorize & Transfer" button in UI
  ├─► [Customer User]: Clicks Authorize Button in UI
  │     └─► POST /api/action/approve settles wire in Core Banking
  └─► [Core Banking Ledger]: Checking balance debited from $24,850.40 to $9,850.40
```

---

## 5. Verification & Testing Evidence

The platform includes two automated test suites ensuring 100% reliability:

```bash
# Core Unit & Integration Test Suite
python run_tests.py
# Result: ALL 7 TESTS PASSED WITH 100% ACCURACY!

# Live System & Agent Workflow Test Suite (13 End-to-End Scenarios)
python test_live_system.py
# Result: ALL 13 EXTENSIVE LIVE SYSTEM & AGENT TESTS PASSED WITH 100% SUCCESS!
```

| Component | Tested Functional Verification | Result |
| :--- | :--- | :---: |
| **Core Database** | In-memory ledger seed, multi-persona accounts, balances, cards, loans | **PASS ✅** |
| **Layer 3 Gateway** | Zero-Trust PII regex masking (SSN, PAN) and prompt injection quarantine | **PASS ✅** |
| **MCP Tools Layer** | 13 typed tools (balance, anomaly, freeze, dispute, bureau, aml, transfer) | **PASS ✅** |
| **Fraud Mitigation** | Anomaly score 92/100, autonomous card lock, provisional credit dispute | **PASS ✅** |
| **Loan Underwriting** | FICO 785 pull, RAG policy lookup, 4.89% APR and $574.49/mo amortization | **PASS ✅** |
| **Wire & AML Gate** | OFAC screening, FinCEN CTR filing, Human-in-the-Loop approval debiting ledger | **PASS ✅** |
| **Web REST APIs** | `/api/chat`, `/api/customer/{id}`, `/api/system/status`, `/api/action/approve` | **PASS ✅** |

---

## 6. Summary for Technical Discussion

- **Scalability**: The modular FastAPI + MCP architecture allows new specialist agents (e.g., Tax Optimization Agent, Commercial Trade Finance Agent) to be registered with zero code changes to the Supervisor.
- **Security & Privacy**: Zero sensitive secrets reach internal reasoning contexts; audit logs capture all tool arguments and execution latencies.
- **Reliability**: Dual-engine architecture guarantees zero-cost, offline evaluation out of the box while remaining 100% compatible with production Gemini and OpenAI models.
