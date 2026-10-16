# NEXUS Core Banking AI — Short Demo Video Walkthrough Guide (5–10 Minutes)

**Submission Requirement**: Short Demo Video (5–10 minutes) demonstrating your application  
**Target Duration**: 6–8 minutes  
**Application URL**: `http://127.0.0.1:8000`  

---

## 🛠️ Quick Video Recording Instructions

You can record your screen using any of the following free tools:
1. **Windows Game Bar (Built-in)**: Press `Win + Alt + R` to start/stop recording, or `Win + G` to open the overlay.
2. **Loom / Clipchamp (Browser / Windows 11)**: Great for screen + webcam recording.
3. **OBS Studio / Zoom**: Share screen and record locally.

> 💡 **PRO TIP — Use the Built-in `▶ Auto Demo` Button**:  
> In the top navigation bar at `http://127.0.0.1:8000`, click the green **`▶ Auto Demo`** button.  
> It will automatically type prompts, run through all 6 banking scenarios with realistic pauses, approve the wire transfer, update the card status, and highlight the agents on the SVG DAG graph while you speak!

---

## 🎬 Timestamped Spoken Presentation Script

### [0:00 – 1:15] Section 1: Introduction & Architecture Blueprint
- **Screen Action**: Start at `http://127.0.0.1:8000`. Click the **`🏛️ 9-Layer Architecture`** tab in the top header.
- **Spoken Script**:
  > *"Hello everyone! Today I am demonstrating our Multi-Agent Banking MVP, built for a simulated enterprise banking environment.*
  > 
  > *Our implementation models the complete 9-layer banking architecture specified in the assignment:*
  > *- At the top, we have our Banking Channels and API Experience Layer.*
  > *- At Layer 3, we have built an AI Gateway with Zero-Trust PII redaction and prompt injection guardrails.*
  > *- At Layer 4, our Multi-Agent Orchestrator features a Supervisor Agent that classifies intent, decomposes workflows into dynamic Directed Acyclic Graphs (DAGs), and delegates tasks to specialized autonomous agents: Customer 360, Risk & Fraud, Credit Underwriting, AML Compliance, Financial Advisory, and Notifications.*
  > *- At Layer 5, our Model Context Protocol (MCP) tool registry provides 13 typed banking tools that interact with our simulated Core Banking Ledger, RAG policy knowledge base, and external credit bureau services.*
  > 
  > *Let's now jump into the live system."*

---

### [1:15 – 2:30] Section 2: Core Banking Interface Tour
- **Screen Action**: Click the **`💬 Swarm Workspace`** tab. Point your cursor across the 3 columns.
- **Spoken Script**:
  > *"Here is our responsive 3-column operational workspace:*
  > 
  > *On the left is the Core Banking Portal. We are looking at customer persona Elena Rostova, a Premier Wealth client with $110,000 in liquid assets ($24,850 in Checking, $85,200 in Savings), a prime FICO score of 785, and her active Visa Infinite card.*
  > 
  > *In the center is our Multi-Agent Conversational Center, featuring our active swarm status bar showing the state of all specialized agents and our workflow stepper.*
  > 
  > *On the right is our Real-Time Observability Platform. It features an interactive SVG Multi-Agent DAG Topology Graph, live latency tracking, token counters, FinOps cost estimation, and step-by-step agent trajectory traces.*
  > 
  > *Let's now test our core use cases."*

---

### [2:30 – 4:30] Section 3: Use Case 1 — Fraud Anomaly & Autonomous Card Lock
- **Screen Action**: Click the first scenario button: **`🚨 Fraud Anomaly & Card Lock`** (or click `▶ Auto Demo`).
- **Spoken Script**:
  > *"In our first use case, the customer asks:*
  > *'I didn't authorize a $1,280 charge in London from yesterday! What is that? Help!'*
  > 
  > *Notice what happens in real time:*
  > *1. The Supervisor Agent classifies the intent as a potential security incident and delegates the audit to the Risk / Fraud Agent.*
  > *2. The Risk Agent calls the `evaluate_fraud_anomalies` tool against the checking ledger. It detects transaction TXN-9081 at Mayfair Luxury Watches in London from an unrecognized iPhone 14. Because Elena lives in Minneapolis with no travel notice, the fraud risk score hits 92 out of 100!*
  > *3. Under bank policy POL-FRAUD-002, the agent takes immediate protective containment: it invokes the `freeze_card` tool. Notice on the left that Elena's Visa Infinite card widget immediately flips to glowing RED with a 🔒 FROZEN / LOCKED status!*
  > *4. Next, it calls `file_fraud_dispute`, creating dispute case DSP-261016 and crediting $1,280 provisional credit back under Visa Zero-Liability protection.*
  > *5. Finally, the Notification Agent dispatches emergency SMS and mobile push alerts.*
  > *6. In the right panel, observe the SVG DAG visualizer: the Supervisor, Risk Agent, and Notification Agent illuminate, and the trajectory log displays the exact tool parameters and sub-millisecond execution times."*

---

### [4:30 – 6:00] Section 4: Use Case 2 — Real-Time Credit Underwriting & Auto Loan ($25k)
- **Screen Action**: Click the second scenario button: **`🚗 Auto Loan Pre-Approval`**.
- **Spoken Script**:
  > *"In our second use case, Elena asks: 'Can I get an auto loan of $25,000 for 48 months?'*
  > 
  > *Watch the specialized agents collaborate:*
  > *1. The Supervisor delegates to the Customer Agent to verify Elena's verified KYC standing and $185,000 annual income.*
  > *2. The Credit Agent invokes `check_credit_bureau`, pulling her 785 FICO score and existing debt liabilities ($610/mo).*
  > *3. The Credit Agent performs a RAG knowledge base search against `POL-CREDIT-001` (our lending policy).*
  > *4. It calls `evaluate_loan_underwriting`. Based on her prime tier, the system assigns a 4.89% fixed APR, calculates a monthly amortized payment of $574.49, total interest of $2,575, and a projected Debt-to-Income ratio of 7.68%, which easily passes our 48% policy cap.*
  > *5. The Supervisor synthesizes a transparent conditional pre-approval letter ready for immediate disbursal."*

---

### [6:00 – 7:45] Section 5: Use Case 3 — International Wire & AML Human-in-the-Loop Gate
- **Screen Action**: Click the third scenario button: **`🌐 Wire Transfer & AML Gate`**. Wait for the Human-in-the-Loop card to appear, then click **`✓ Cryptographically Authorize & Transfer`**.
- **Spoken Script**:
  > *"In our third use case, we demonstrate AML compliance and Human-in-the-Loop governance.*
  > 
  > *Elena requests an international wire of $15,000 to John Doe in Germany for an invoice.*
  > *1. The Customer Agent confirms sufficient settled checking funds ($24,850 available).*
  > *2. The Compliance Agent calls `screen_aml_compliance`, cross-referencing against OFAC sanctions and PEP blacklists (Passed).*
  > *3. Because the amount exceeds $10,000 USD, it triggers a mandatory Bank Secrecy Act FinCEN Form 112 Currency Transaction Report.*
  > *4. Furthermore, because outgoing wires over $5,000 represent significant financial impact, autonomous execution is halted. Notice the amber Human-in-the-Loop authorization card in the center workspace with token APPRV-ED46C179.*
  > 
  > *Let's click '✓ Cryptographically Authorize & Transfer'.*
  > *Instantly, the wire settles. Look at the left panel: Elena's checking balance is debited by exactly $15,000 down to $9,850.40!"*

---

### [7:45 – 9:00] Section 6: AI Gateway Security, Observability & Conclusion
- **Screen Action**: In the chat input, type: `"My SSN is 123-45-6789 and card is 4111-2222-3333-4912. What is my balance?"` and send.
- **Spoken Script**:
  > *"Finally, let's verify Layer 3 security. I will send a prompt containing a raw Social Security Number and a 16-digit credit card number.*
  > 
  > *Look at the right panel: our Zero-Trust AI Gateway instantly intercepted and redacted the SSN and PAN before downstream agents saw them.*
  > 
  > *Our application runs completely out of the box using our Built-in Cognitive Agent Engine without requiring any external API keys, while also supporting live Google Gemini and OpenAI models.*
  > 
  > *All 13 automated live system tests pass with 100% accuracy. Thank you for watching!"*

---

## 📋 Evaluation Checklist Covered in Video

- [x] Demonstrates Supervisor / Orchestrator routing and task decomposition.
- [x] Demonstrates specialized agents (Customer, Risk, Credit, Compliance, Notification).
- [x] Demonstrates typed Core Banking MCP Tools (`evaluate_fraud_anomalies`, `freeze_card`, `evaluate_loan_underwriting`, `screen_aml_compliance`).
- [x] Demonstrates 3–5 core banking use cases with real-time UI updates (card lock, loan calculation, wire debit).
- [x] Demonstrates Layer 3 AI Gateway (PII redaction & safety).
- [x] Demonstrates Human-in-the-Loop authorization gate.
- [x] Explains 9-layer architectural alignment.
