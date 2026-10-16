import time
import uuid
from typing import Optional, Dict, Any
from app.core.models import (
    WorkflowExecutionTrace, AgentThoughtStep, StepType, AgentRole, GuardrailReport
)
from app.core.gateway import ai_gateway
from app.llm.provider import llm_manager
from app.data.banking_db import db

class SupervisorAgent:
    """
    Layer 4: Supervisor / Multi-Agent Orchestrator
    Responsibilities:
    - Intent Classification & Task Decomposition
    - Agent Selection & Workflow Management (DAG)
    - State Management & Correlation Tracing
    - Guardrail Inspection
    - Error Recovery & Fallbacks
    - Result Aggregation & Human Escalation Handling
    """
    def __init__(self):
        self.role = AgentRole.SUPERVISOR

    def process_request(
        self,
        user_message: str,
        customer_id: str = "CUST-1001",
        session_id: Optional[str] = None,
        llm_provider: Optional[str] = None,
        api_key: Optional[str] = None
    ) -> WorkflowExecutionTrace:
        start_time = time.time()
        sid = session_id or f"SES-{uuid.uuid4().hex[:8].upper()}"

        # 1. AI Gateway / AI Control Plane (Layer 3)
        sanitized_msg, guardrail_report = ai_gateway.process_incoming_request(user_message)

        # Initialize Execution Trace
        trace = WorkflowExecutionTrace(
            session_id=sid,
            customer_id=customer_id,
            user_message=user_message,
            sanitized_message=sanitized_msg,
            guardrail_report=guardrail_report
        )

        # Log Guardrail Inspection Step
        if not guardrail_report.prompt_safe:
            trace.steps.append(AgentThoughtStep(
                agent_name="AI Gateway / Control Plane",
                step_type=StepType.GUARDRAIL,
                title="SECURITY GUARDRAIL TRIGGERED - REQUEST QUARANTINED",
                content=f"Violation: {guardrail_report.violation_reason}. The request was blocked to maintain zero-trust banking safety."
            ))
            trace.final_response = (
                f"⚠️ **Security Alert**: Your request was flagged by the NEXUS Banking AI Gateway for security policy violations:\n"
                f"> *{guardrail_report.violation_reason}*\n\n"
                f"Please rephrase your request according to standard banking inquiries."
            )
            trace.execution_time_ms = round((time.time() - start_time) * 1000, 2)
            return trace

        if guardrail_report.pii_detected:
            trace.steps.append(AgentThoughtStep(
                agent_name="AI Gateway / Control Plane",
                step_type=StepType.GUARDRAIL,
                title=f"Zero-Trust PII Masking Applied ({len(guardrail_report.pii_detected)} entities redacted)",
                content=f"Redacted sensitive items: {', '.join(guardrail_report.pii_detected)}. Downstream agents receive only sanitized tokens."
            ))

        # 2. Multi-Agent Orchestrator Execution
        trace = llm_manager.execute_multi_agent_workflow(
            trace,
            provider_override=llm_provider,
            api_key_override=api_key
        )

        # 3. FinOps & Observability Metrics
        elapsed_ms = round((time.time() - start_time) * 1000, 2)
        trace.execution_time_ms = elapsed_ms

        prompt_tokens = max(15, len(user_message) // 4 + len(trace.workflow_dag) * 30)
        completion_tokens = max(25, len(trace.final_response) // 4 + len(trace.steps) * 45)
        trace.token_usage = ai_gateway.calculate_cost(prompt_tokens, completion_tokens)

        return trace

supervisor = SupervisorAgent()
