import re
from typing import Tuple, List, Dict
from app.core.models import GuardrailReport

class AIGateway:
    """
    Layer 3: AI Gateway / AI Control Plane
    Provides Zero-Trust PII Detection, Prompt Injection Guardrails, Content Safety,
    Token Budget enforcement, and Audit Policy tracking.
    """
    
    INJECTION_PATTERNS = [
        r"ignore (all )?previous instructions",
        r"disregard safety guidelines",
        r"jailbreak",
        r"prompt injection",
        r"drop database",
        r"bypass security",
        r"reveal system prompt",
        r"transfer all my money to .*hacker",
        r"override banking policy"
    ]

    SSN_PATTERN = r"\b\d{3}[- ]?\d{2}[- ]?(\d{4})\b"
    PAN_PATTERN = r"\b(?:\d{4}[ -]?){3}(\d{4})\b"
    CVV_PATTERN = r"\bcvv\s*[:=]?\s*(\d{3,4})\b"

    def __init__(self):
        self.total_tokens_processed = 0
        self.total_pii_entities_redacted = 0
        self.blocked_requests_count = 0

    def process_incoming_request(self, text: str) -> Tuple[str, GuardrailReport]:
        sanitized = text
        pii_found: List[str] = []
        is_safe = True
        violation_reason = None

        # 1. Prompt Injection & Jailbreak Guardrail Check
        for pattern in self.INJECTION_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                is_safe = False
                violation_reason = f"Security Policy Violation: High-risk prompt pattern detected ('{pattern}')"
                self.blocked_requests_count += 1
                break

        # 2. PII Detection & Zero-Trust Redaction
        # Mask SSN
        ssn_matches = list(re.finditer(self.SSN_PATTERN, sanitized))
        if ssn_matches:
            pii_found.append("SSN (Social Security Number)")
            sanitized = re.sub(self.SSN_PATTERN, r"[REDACTED-SSN-***-**-\1]", sanitized)
            self.total_pii_entities_redacted += len(ssn_matches)

        # Mask PAN (Credit Card Numbers)
        pan_matches = list(re.finditer(self.PAN_PATTERN, sanitized))
        if pan_matches:
            pii_found.append("PAN (Payment Card Account Number)")
            sanitized = re.sub(self.PAN_PATTERN, r"[REDACTED-PAN-****-****-****-\1]", sanitized)
            self.total_pii_entities_redacted += len(pan_matches)

        # Mask CVV
        cvv_matches = list(re.finditer(self.CVV_PATTERN, sanitized, re.IGNORECASE))
        if cvv_matches:
            pii_found.append("CVV Security Code")
            sanitized = re.sub(self.CVV_PATTERN, r"CVV:[REDACTED-CVV]", sanitized, flags=re.IGNORECASE)
            self.total_pii_entities_redacted += len(cvv_matches)

        # Token estimation (rule of thumb ~4 chars per token)
        estimated_tokens = max(1, len(text) // 4)
        self.total_tokens_processed += estimated_tokens

        report = GuardrailReport(
            prompt_safe=is_safe,
            violation_reason=violation_reason,
            pii_detected=pii_found,
            sanitized_input=sanitized,
            tokens_evaluated=estimated_tokens
        )

        return sanitized, report

    def calculate_cost(self, prompt_tokens: int, completion_tokens: int, model: str = "cognitive-agent") -> Dict[str, float]:
        # $0.15 per 1M input tokens, $0.60 per 1M output tokens (Gemini Flash standard pricing tier)
        cost_input = (prompt_tokens / 1_000_000) * 0.15
        cost_output = (completion_tokens / 1_000_000) * 0.60
        total_cost = round(cost_input + cost_output, 6)
        return {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
            "estimated_cost_usd": total_cost
        }

ai_gateway = AIGateway()
