from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from enum import Enum
import uuid
from datetime import datetime

class AgentRole(str, Enum):
    SUPERVISOR = "Supervisor / Orchestrator"
    CUSTOMER = "Customer Agent"
    PRODUCT = "Banking Product Agent"
    RISK = "Risk / Fraud Agent"
    CREDIT = "Credit Agent"
    COMPLIANCE = "Compliance Agent"
    ADVISORY = "Financial Advisory Agent"
    NOTIFICATION = "Notification Agent"

class StepType(str, Enum):
    GUARDRAIL = "GUARDRAIL"
    SUPERVISOR_PLAN = "SUPERVISOR_PLAN"
    DELEGATION = "DELEGATION"
    THOUGHT = "THOUGHT"
    TOOL_CALL = "TOOL_CALL"
    OBSERVATION = "OBSERVATION"
    HUMAN_ESCALATION = "HUMAN_ESCALATION"
    FINAL_OUTPUT = "FINAL_OUTPUT"

class AgentThoughtStep(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().strftime("%H:%M:%S.%f")[:-3])
    agent_name: str
    step_type: StepType
    title: str
    content: str
    tool_name: Optional[str] = None
    tool_args: Optional[Dict[str, Any]] = None
    tool_result: Optional[Dict[str, Any]] = None

class GuardrailReport(BaseModel):
    prompt_safe: bool = True
    violation_reason: Optional[str] = None
    pii_detected: List[str] = []
    sanitized_input: str
    tokens_evaluated: int = 0

class HumanApprovalPayload(BaseModel):
    action_type: str  # e.g., "INTERNATIONAL_WIRE", "CARD_FREEZE", "HIGH_RISK_OVERRIDE"
    title: str
    description: str
    severity: str = "HIGH"  # LOW, MEDIUM, HIGH, CRITICAL
    parameters: Dict[str, Any]
    approval_token: str = Field(default_factory=lambda: f"APPRV-{uuid.uuid4().hex[:8].upper()}")

class WorkflowExecutionTrace(BaseModel):
    trace_id: str = Field(default_factory=lambda: f"TRC-{uuid.uuid4().hex[:10].upper()}")
    session_id: str
    customer_id: str
    user_message: str
    sanitized_message: str
    intent: str = "GENERAL_INQUIRY"
    workflow_dag: List[str] = []
    active_agents: List[str] = []
    guardrail_report: GuardrailReport
    steps: List[AgentThoughtStep] = []
    final_response: str = ""
    human_approval_required: bool = False
    human_approval_payload: Optional[HumanApprovalPayload] = None
    execution_time_ms: float = 0.0
    token_usage: Dict[str, Any] = {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
        "estimated_cost_usd": 0.0000
    }

class ChatRequest(BaseModel):
    message: str
    customer_id: str = "CUST-1001"
    session_id: Optional[str] = None
    llm_provider: Optional[str] = "cognitive"
    api_key: Optional[str] = None

class ChatResponse(BaseModel):
    success: bool = True
    trace: WorkflowExecutionTrace
    customer_snapshot: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class HumanApprovalActionRequest(BaseModel):
    trace_id: str
    customer_id: str
    action: str  # "APPROVE" or "REJECT"
    approval_token: str
    action_type: str
    parameters: Dict[str, Any]

class Transaction(BaseModel):
    id: str
    account_id: str
    date: str
    description: str
    amount: float
    type: str  # DEBIT or CREDIT
    category: str
    merchant: str
    location: str
    device: str
    status: str  # COMPLETED, PENDING, FLAGGED, DISPUTED
    fraud_risk_score: int  # 0 to 100
    risk_flags: List[str] = []

class Card(BaseModel):
    id: str
    card_number_masked: str
    type: str  # DEBIT, CREDIT
    network: str  # VISA, MASTERCARD
    expiry: str
    status: str  # ACTIVE, LOCKED, CANCELLED
    spending_limit: float
    current_cycle_spend: float

class Account(BaseModel):
    id: str
    type: str  # CHECKING, SAVINGS, BUSINESS
    account_number_masked: str
    routing_number: str
    balance: float
    currency: str = "USD"
    status: str = "ACTIVE"

class Loan(BaseModel):
    id: str
    type: str  # AUTO, PERSONAL, MORTGAGE, BUSINESS_CREDIT
    original_principal: float
    remaining_balance: float
    interest_rate_apr: float
    term_months: int
    monthly_payment: float
    status: str  # ACTIVE, PENDING_APPROVAL, CLOSED

class CustomerProfile(BaseModel):
    id: str
    name: str
    email: str
    phone: str
    ssn_masked: str
    tier: str  # RETAIL, BUSINESS, WEALTH
    kyc_status: str  # VERIFIED, PENDING
    credit_score: int
    annual_income: float
    accounts: List[Account]
    cards: List[Card]
    loans: List[Loan]
