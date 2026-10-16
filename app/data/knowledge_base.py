from typing import List, Dict

BANK_KNOWLEDGE_DOCS: List[Dict[str, str]] = [
    {
        "id": "POL-CREDIT-001",
        "category": "Lending & Underwriting",
        "title": "NEXUS Credit Risk & Retail Lending Policy (Q4 2026)",
        "content": (
            "1. Minimum Credit Score Threshold: Prime tier >= 740 (APR: 4.89% - 5.49%), "
            "Near-Prime tier 680-739 (APR: 6.25% - 7.50%), Sub-Prime < 640 (Automated rejection). "
            "2. Maximum Debt-to-Income (DTI) ratio is 43% for unsecured personal loans and 48% for auto loans. "
            "3. Loan Limits: Auto loans up to $75,000; Personal unsecured loans up to $50,000; Business working capital up to $250,000. "
            "4. Term options: 24, 36, 48, 60, or 72 months. Prepayment penalty: None. "
            "5. Instant Pre-Approval criteria: Customer KYC must be VERIFIED, active checking account in good standing for >= 6 months, and credit score >= 680."
        ),
        "tags": "credit loan auto personal lending apr interest dti underwrite borrow financing"
    },
    {
        "id": "POL-FRAUD-002",
        "category": "Fraud & Security Operations",
        "title": "Card Compromise, Unauthorized Transactions & Dispute Resolution SOP",
        "content": (
            "1. Anomaly Detection Triggers: A fraud risk score >= 75 requires immediate protective action. "
            "Key anomaly vectors include foreign geo-velocity (transaction >1,000 miles from registered home address within 6 hours), "
            "unrecognized hardware/device fingerprint, and luxury merchant category without prior spend history. "
            "2. Immediate Containment: When a cardholder questions or confirms an unauthorized transaction, the agent must immediately freeze "
            "the compromised card to prevent sequential fraudulent authorization attempts. "
            "3. Dispute & Zero-Liability: Under Regulation E and Visa/Mastercard Zero Liability, customers are not liable for unauthorized charges. "
            "A dispute ticket (DSP-XXXX) must be created immediately, and instant provisional credit of 100% of the disputed amount is credited back. "
            "4. Multi-Channel Alert: The customer must receive instant push notification and SMS confirmation containing the dispute reference and confirmation of card lock."
        ),
        "tags": "fraud suspicious unauthorized transaction freeze lock card dispute chargeback stolen compromised security"
    },
    {
        "id": "POL-COMPLIANCE-003",
        "category": "AML & Regulatory Compliance",
        "title": "Bank Secrecy Act (BSA), Anti-Money Laundering (AML) & Sanctions Directive",
        "content": (
            "1. Currency Transaction Report (CTR): Any single transaction or aggregated batch exceeding $10,000 USD triggers mandatory "
            "BSA/FinCEN CTR filing (Form 112). The system must log regulatory audit telemetry. "
            "2. Sanctions & OFAC Screening: All international wires and beneficiaries must be cross-referenced against OFAC Specially Designated Nationals (SDN) "
            "and PEP (Politically Exposed Persons) databases. High-risk jurisdictions (FATF blacklist) are strictly blocked. "
            "3. Step-Up Authentication / Human-in-the-Loop (HITL): Any outgoing wire transfer >= $5,000 or any transaction with high fraud risk "
            "MUST require dual authorization: an explicit Customer Step-Up confirmation token (APPRV-XXXX) before fund debit can be finalized in the Core Banking ledger."
        ),
        "tags": "aml compliance sanctions wire transfer ofac bsa ctr money laundering regulations international hitl approval"
    },
    {
        "id": "POL-PRODUCT-004",
        "category": "Banking Products & Wealth Management",
        "title": "Retail & Premier Wealth Banking Products Guide",
        "content": (
            "1. Deposit Accounts: High-Yield Savings Account offers 4.85% APY with zero monthly maintenance fee for balances over $5,000. "
            "Standard Checking offers 0.25% APY with unlimited free debit transactions and fee-free ATM access worldwide. "
            "2. Premier Wealth Tier: Elena Rostova qualifies for Wealth tier benefits including zero domestic/international wire fees, "
            "dedicated Relationship Manager, 1.5% cashback on all Visa Infinite purchases, and expedited loan processing. "
            "3. Certificates of Deposit (CD): 6-Month CD yields 5.05% APY, 12-Month CD yields 5.25% APY, $1,000 minimum deposit."
        ),
        "tags": "savings checking accounts interest apy wealth products rates certificates deposit tier perks"
    },
    {
        "id": "POL-SECURITY-005",
        "category": "Security & AI Gateway",
        "title": "AI Safety, PII Masking and Prompt Injection Defense Policy",
        "content": (
            "1. Zero-Trust PII Redaction: Social Security Numbers, Full 16-digit Primary Account Numbers (PAN), CVVs, and sensitive PINs "
            "must be masked at Layer 3 (AI Gateway) before prompt payloads reach any internal or external LLM. "
            "2. Prompt Injection Guardrails: Any prompt attempting system prompt leaks, unauthorized administrative balance modifications, "
            "or security policy overrides must be flagged, quarantined, and audited."
        ),
        "tags": "pii security guardrails mask safety injection privacy compliance token budget"
    }
]
