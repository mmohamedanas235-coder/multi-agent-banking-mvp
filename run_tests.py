import sys
import os

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from tests.test_agents import (
    test_database_initialization,
    test_ai_gateway_pii_and_guardrails,
    test_tools_execution,
    test_use_case_1_fraud_and_card_freeze,
    test_use_case_2_loan_pre_approval,
    test_use_case_3_wire_transfer_hitl,
    test_chat_api_endpoint
)

if __name__ == "__main__":
    print("==================================================")
    print(" RUNNING NEXUS MULTI-AGENT BANKING TEST SUITE     ")
    print("==================================================")
    test_database_initialization()
    print(" [PASS] 1. Core Banking Database initialization & seed integrity")
    test_ai_gateway_pii_and_guardrails()
    print(" [PASS] 2. Layer 3 AI Gateway (PII Redaction & Security Guardrails)")
    test_tools_execution()
    print(" [PASS] 3. Layer 5 MCP Tool Registry & Banking APIs")
    test_use_case_1_fraud_and_card_freeze()
    print(" [PASS] 4. Use Case 1: Fraud Anomaly Detection & Autonomous Card Lock")
    test_use_case_2_loan_pre_approval()
    print(" [PASS] 5. Use Case 2: Credit Underwriting & Instant Loan Offer")
    test_use_case_3_wire_transfer_hitl()
    print(" [PASS] 6. Use Case 3: High-Value Wire & AML/CTR Human-in-the-Loop")
    test_chat_api_endpoint()
    print(" [PASS] 7. Full REST API & Chat Orchestration Endpoint")
    print("==================================================")
    print(" SUCCESS: ALL 7 TESTS PASSED WITH 100% ACCURACY! ")
    print("==================================================")
