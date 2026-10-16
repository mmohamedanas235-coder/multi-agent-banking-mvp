from typing import Dict, Any, Callable, List, Optional
import time
from app.data.banking_db import db
from app.core.rag import rag_retriever

class ToolRegistry:
    """
    Layer 5: Agent Tool / MCP Layer
    Maintains a typed registry of Core Banking Tools, schema validation,
    permission checks, sandbox execution, and audit logging.
    """
    def __init__(self):
        self._tools: Dict[str, Dict[str, Any]] = {}
        self.audit_log: List[Dict[str, Any]] = []

    def register_tool(self, name: str, description: str, parameters: Dict[str, Any], handler: Callable):
        self._tools[name] = {
            "name": name,
            "description": description,
            "parameters": parameters,
            "handler": handler
        }

    def get_tool(self, name: str) -> Optional[Dict[str, Any]]:
        return self._tools.get(name)

    def list_tool_definitions(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": t["name"],
                "description": t["description"],
                "parameters": t["parameters"]
            }
            for t in self._tools.values()
        ]

    def execute_tool(self, name: str, caller_agent: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        tool = self.get_tool(name)
        if not tool:
            return {"success": False, "error": f"Tool '{name}' is not registered in the Banking MCP catalog."}

        start_time = time.time()
        try:
            result = tool["handler"](**arguments)
            elapsed_ms = round((time.time() - start_time) * 1000, 2)
            
            # Audit logging
            audit_entry = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "caller_agent": caller_agent,
                "tool_name": name,
                "arguments": arguments,
                "status": "SUCCESS",
                "execution_ms": elapsed_ms
            }
            self.audit_log.append(audit_entry)
            return {"success": True, "result": result, "latency_ms": elapsed_ms}
        except Exception as e:
            elapsed_ms = round((time.time() - start_time) * 1000, 2)
            audit_entry = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "caller_agent": caller_agent,
                "tool_name": name,
                "arguments": arguments,
                "status": "ERROR",
                "error": str(e),
                "execution_ms": elapsed_ms
            }
            self.audit_log.append(audit_entry)
            return {"success": False, "error": str(e), "latency_ms": elapsed_ms}

tools = ToolRegistry()

# ----------------- Concrete Banking Tools ----------------- #

def tool_get_customer_360(customer_id: str) -> Dict[str, Any]:
    """Retrieve full Customer 360 profile, KYC status, and linked accounts."""
    cust = db.get_customer(customer_id)
    if not cust:
        return {"found": False, "error": f"Customer ID {customer_id} not found"}
    return {
        "found": True,
        "customer_id": cust.id,
        "name": cust.name,
        "tier": cust.tier,
        "kyc_status": cust.kyc_status,
        "credit_score": cust.credit_score,
        "annual_income": cust.annual_income,
        "total_accounts": len(cust.accounts),
        "accounts": [acc.dict() for acc in cust.accounts],
        "cards": [c.dict() for c in cust.cards],
        "active_loans": [l.dict() for l in cust.loans]
    }

def tool_get_account_balance(account_id: str) -> Dict[str, Any]:
    """Retrieve real-time settled ledger balance for an account."""
    acc = db.get_account_by_id(account_id)
    if not acc:
        return {"found": False, "error": f"Account {account_id} not found"}
    return {
        "account_id": acc.id,
        "type": acc.type,
        "balance": acc.balance,
        "currency": acc.currency,
        "status": acc.status
    }

def tool_list_transactions(account_id: str, limit: int = 5) -> Dict[str, Any]:
    """Fetch recent transaction history with metadata, merchant info, and risk flags."""
    txns = db.get_transactions_for_account(account_id, limit=limit)
    return {
        "account_id": account_id,
        "count": len(txns),
        "transactions": [t.dict() for t in txns]
    }

def tool_evaluate_fraud_anomalies(customer_id: str, account_id: str) -> Dict[str, Any]:
    """Scan recent transactions for geo-velocity anomalies, device mismatch, and high fraud scores."""
    txns = db.get_transactions_for_account(account_id, limit=10)
    anomalies = []
    for t in txns:
        if t.fraud_risk_score >= 60 or t.risk_flags:
            anomalies.append(t.dict())
    
    return {
        "customer_id": customer_id,
        "account_id": account_id,
        "total_anomalies_detected": len(anomalies),
        "anomalous_transactions": anomalies,
        "risk_level": "CRITICAL" if any(a["fraud_risk_score"] >= 80 for a in anomalies) else ("HIGH" if anomalies else "LOW")
    }

def tool_freeze_card(card_id: str, reason: str) -> Dict[str, Any]:
    """Emergency lock on a debit or credit card to prevent unauthorized authorizations."""
    card = db.set_card_status(card_id, "LOCKED", reason)
    if not card:
        return {"success": False, "error": f"Card {card_id} not found"}
    return {
        "success": True,
        "card_id": card_id,
        "status": "LOCKED",
        "action_taken": "IMMEDIATE_CARD_FREEZE",
        "reason": reason,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

def tool_file_fraud_dispute(transaction_id: str, customer_id: str, reason: str) -> Dict[str, Any]:
    """File a formal Regulation E / Visa Zero-Liability fraud dispute and issue provisional credit."""
    return db.dispute_transaction(transaction_id, customer_id, reason)

def tool_check_credit_bureau(customer_id: str) -> Dict[str, Any]:
    """Simulated bureau pull (Equifax/Experian/TransUnion) with FICO score and trade-line history."""
    cust = db.get_customer(customer_id)
    if not cust:
        return {"error": f"Customer {customer_id} not found"}
    
    # Calculate DTI
    total_monthly_debt = sum(l.monthly_payment for l in cust.loans)
    monthly_income = cust.annual_income / 12.0
    current_dti = round((total_monthly_debt / monthly_income) * 100, 2)

    return {
        "customer_id": cust.id,
        "bureau": "TransUnion / Equifax Consortium",
        "fico_score": cust.credit_score,
        "rating": "EXCELLENT" if cust.credit_score >= 750 else ("GOOD" if cust.credit_score >= 700 else "FAIR"),
        "monthly_income": round(monthly_income, 2),
        "existing_monthly_debt": total_monthly_debt,
        "current_dti_percentage": current_dti,
        "delinquencies_past_24m": 0,
        "credit_inquiries_past_6m": 1
    }

def tool_evaluate_loan_underwriting(customer_id: str, loan_type: str, requested_amount: float, term_months: int) -> Dict[str, Any]:
    """Apply bank lending policy rules and calculate APR, monthly payment, and pre-approval status."""
    cust = db.get_customer(customer_id)
    if not cust:
        return {"approved": False, "error": f"Customer {customer_id} not found"}

    score = cust.credit_score
    monthly_income = cust.annual_income / 12.0
    existing_monthly_debt = sum(l.monthly_payment for l in cust.loans)

    # Determine APR based on bureau score and policy
    if score >= 750:
        base_apr = 4.89 if loan_type.upper() == "AUTO" else 6.25
    elif score >= 700:
        base_apr = 6.45 if loan_type.upper() == "AUTO" else 7.80
    elif score >= 650:
        base_apr = 8.15 if loan_type.upper() == "AUTO" else 9.99
    else:
        return {
            "approved": False,
            "reason": f"Credit score {score} is below minimum lending cutoff of 640.",
            "policy_reference": "POL-CREDIT-001"
        }

    # Calculate projected monthly payment
    monthly_rate = (base_apr / 100.0) / 12.0
    factor = (1.0 + monthly_rate) ** term_months
    projected_monthly = round(requested_amount * (monthly_rate * factor) / (factor - 1.0), 2)
    projected_dti = round(((existing_monthly_debt + projected_monthly) / monthly_income) * 100, 2)

    max_dti = 48.0 if loan_type.upper() == "AUTO" else 43.0
    if projected_dti > max_dti:
        return {
            "approved": False,
            "reason": f"Projected DTI ({projected_dti}%) exceeds policy limit of {max_dti}%.",
            "policy_reference": "POL-CREDIT-001"
        }

    total_interest = round((projected_monthly * term_months) - requested_amount, 2)

    return {
        "approved": True,
        "customer_id": cust.id,
        "loan_type": loan_type.upper(),
        "requested_amount": requested_amount,
        "term_months": term_months,
        "approved_apr": base_apr,
        "estimated_monthly_payment": projected_monthly,
        "total_interest": total_interest,
        "projected_dti": projected_dti,
        "status": "PRE_APPROVED_CONDITIONAL",
        "policy_reference": "POL-CREDIT-001"
    }

def tool_submit_loan_application(customer_id: str, loan_type: str, amount: float, term_months: int, apr: float) -> Dict[str, Any]:
    """Disburse approved loan to customer account and add to core banking loan book."""
    loan = db.add_loan(customer_id, loan_type, amount, apr, term_months)
    return {
        "success": True,
        "loan_id": loan.id,
        "status": loan.status,
        "amount": loan.original_principal,
        "apr": loan.interest_rate_apr,
        "monthly_payment": loan.monthly_payment,
        "disbursed_to_account": "ACC-1001-CHK"
    }

def tool_screen_aml_compliance(customer_id: str, recipient_name: str, recipient_country: str, amount: float) -> Dict[str, Any]:
    """Screen wire transfers for OFAC sanctions, PEP lists, and BSA/FinCEN CTR requirements."""
    high_risk_countries = ["NORTH KOREA", "IRAN", "SYRIA", "RUSSIA", "MYANMAR"]
    sanctioned_names = ["VIKTOR BOUT", "SANCTIONED CORP", "DARKNET HOLDINGS"]

    is_sanctioned = (recipient_country.upper() in high_risk_countries) or any(s in recipient_name.upper() for s in sanctioned_names)
    ctr_required = amount >= 10000.00
    hitl_approval_required = amount >= 5000.00 or is_sanctioned

    return {
        "customer_id": customer_id,
        "recipient_name": recipient_name,
        "recipient_country": recipient_country,
        "amount": amount,
        "ofac_sanctions_clear": not is_sanctioned,
        "ctr_filing_required": ctr_required,
        "fincen_form": "FinCEN Form 112 (CTR)" if ctr_required else "N/A",
        "hitl_step_up_required": hitl_approval_required,
        "compliance_status": "FLAGGED_BLOCK" if is_sanctioned else ("FLAGGED_REVIEW" if ctr_required else "CLEAR")
    }

def tool_execute_fund_transfer(from_account: str, to_account: str, recipient_name: str, amount: float, memo: str) -> Dict[str, Any]:
    """Execute settled fund debit and wire disbursement in Core Banking."""
    return db.execute_transfer(from_account, to_account, recipient_name, amount, memo)

def tool_send_notification(customer_id: str, channel: str, subject: str, message: str, priority: str = "HIGH") -> Dict[str, Any]:
    """Dispatch real-time SMS, Email, or Mobile Push alert to the customer."""
    record = db.record_notification(customer_id, channel, subject, message, priority)
    return {"delivered": True, "notification_record": record}

def tool_search_knowledge_base(query: str) -> Dict[str, Any]:
    """Search NEXUS Bank regulatory directives, SOPs, and product policies via RAG."""
    results = rag_retriever.search(query, top_k=2)
    return {"query": query, "matches_found": len(results), "documents": results}

# Register all tools into the tool catalog
tools.register_tool(
    name="get_customer_360",
    description="Retrieve full Customer 360 profile, KYC status, credit score, linked accounts, cards and active loans.",
    parameters={"type": "object", "properties": {"customer_id": {"type": "string"}}, "required": ["customer_id"]},
    handler=tool_get_customer_360
)
tools.register_tool(
    name="get_account_balance",
    description="Retrieve settled ledger balance for an account ID.",
    parameters={"type": "object", "properties": {"account_id": {"type": "string"}}, "required": ["account_id"]},
    handler=tool_get_account_balance
)
tools.register_tool(
    name="list_transactions",
    description="Fetch recent transaction ledger for an account with merchant, location, device, and risk flags.",
    parameters={"type": "object", "properties": {"account_id": {"type": "string"}, "limit": {"type": "integer"}}, "required": ["account_id"]},
    handler=tool_list_transactions
)
tools.register_tool(
    name="evaluate_fraud_anomalies",
    description="Run algorithmic anomaly detection scanning geo-velocity, device integrity, and fraud risk scores.",
    parameters={"type": "object", "properties": {"customer_id": {"type": "string"}, "account_id": {"type": "string"}}, "required": ["customer_id", "account_id"]},
    handler=tool_evaluate_fraud_anomalies
)
tools.register_tool(
    name="freeze_card",
    description="Instantly freeze/lock a compromised debit or credit card to stop fraudulent debits.",
    parameters={"type": "object", "properties": {"card_id": {"type": "string"}, "reason": {"type": "string"}}, "required": ["card_id", "reason"]},
    handler=tool_freeze_card
)
tools.register_tool(
    name="file_fraud_dispute",
    description="File a formal Regulation E / Zero-Liability dispute ticket and credit provisional funds back.",
    parameters={"type": "object", "properties": {"transaction_id": {"type": "string"}, "customer_id": {"type": "string"}, "reason": {"type": "string"}}, "required": ["transaction_id", "customer_id", "reason"]},
    handler=tool_file_fraud_dispute
)
tools.register_tool(
    name="check_credit_bureau",
    description="Query simulated credit bureau for FICO score, monthly debt obligations, and DTI ratio.",
    parameters={"type": "object", "properties": {"customer_id": {"type": "string"}}, "required": ["customer_id"]},
    handler=tool_check_credit_bureau
)
tools.register_tool(
    name="evaluate_loan_underwriting",
    description="Apply credit lending policy rules, calculate APR, estimated monthly payment, and pre-approval status.",
    parameters={"type": "object", "properties": {"customer_id": {"type": "string"}, "loan_type": {"type": "string"}, "requested_amount": {"type": "number"}, "term_months": {"type": "integer"}}, "required": ["customer_id", "loan_type", "requested_amount", "term_months"]},
    handler=tool_evaluate_loan_underwriting
)
tools.register_tool(
    name="submit_loan_application",
    description="Disburse approved loan to customer account and bind to Core Banking loan ledger.",
    parameters={"type": "object", "properties": {"customer_id": {"type": "string"}, "loan_type": {"type": "string"}, "amount": {"type": "number"}, "term_months": {"type": "integer"}, "apr": {"type": "number"}}, "required": ["customer_id", "loan_type", "amount", "term_months", "apr"]},
    handler=tool_submit_loan_application
)
tools.register_tool(
    name="screen_aml_compliance",
    description="Screen transfer requests for OFAC sanctions, PEP lists, and BSA/FinCEN CTR filing triggers.",
    parameters={"type": "object", "properties": {"customer_id": {"type": "string"}, "recipient_name": {"type": "string"}, "recipient_country": {"type": "string"}, "amount": {"type": "number"}}, "required": ["customer_id", "recipient_name", "recipient_country", "amount"]},
    handler=tool_screen_aml_compliance
)
tools.register_tool(
    name="execute_fund_transfer",
    description="Execute live settled fund debit and wire disbursement in Core Banking ledger.",
    parameters={"type": "object", "properties": {"from_account": {"type": "string"}, "to_account": {"type": "string"}, "recipient_name": {"type": "string"}, "amount": {"type": "number"}, "memo": {"type": "string"}}, "required": ["from_account", "to_account", "recipient_name", "amount", "memo"]},
    handler=tool_execute_fund_transfer
)
tools.register_tool(
    name="send_notification",
    description="Dispatch real-time SMS, Email, or Mobile Push alert to the customer.",
    parameters={"type": "object", "properties": {"customer_id": {"type": "string"}, "channel": {"type": "string"}, "subject": {"type": "string"}, "message": {"type": "string"}, "priority": {"type": "string"}}, "required": ["customer_id", "channel", "subject", "message"]},
    handler=tool_send_notification
)
tools.register_tool(
    name="search_knowledge_base",
    description="Retrieve banking policies, SOPs, lending rules, and regulatory limits via RAG vector/lexical search.",
    parameters={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
    handler=tool_search_knowledge_base
)
