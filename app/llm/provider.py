import os
from typing import Optional
from app.core.models import WorkflowExecutionTrace
from app.llm.cognitive_engine import cognitive_engine
from app.config import config

class LLMProviderManager:
    """
    Manages model execution between the Built-in Cognitive Multi-Agent Engine,
    Google Gemini (via google-genai), and OpenAI.
    """
    def __init__(self):
        self.active_provider = config.DEFAULT_LLM_PROVIDER
        self.gemini_key = config.GEMINI_API_KEY
        self.openai_key = config.OPENAI_API_KEY

    def set_provider(self, provider: str, api_key: Optional[str] = None):
        self.active_provider = provider.lower()
        if api_key:
            if "gemini" in self.active_provider:
                self.gemini_key = api_key
            elif "openai" in self.active_provider:
                self.openai_key = api_key

    def execute_multi_agent_workflow(self, trace: WorkflowExecutionTrace, provider_override: Optional[str] = None, api_key_override: Optional[str] = None) -> WorkflowExecutionTrace:
        provider = (provider_override or self.active_provider).lower()
        key = api_key_override or (self.gemini_key if "gemini" in provider else self.openai_key)

        # If Gemini requested and key available, attempt live Gemini model call
        if provider == "gemini" and key:
            try:
                return self._execute_gemini_workflow(trace, key)
            except Exception as e:
                # Add a fallback note and smoothly execute via cognitive engine
                trace = cognitive_engine.process(trace)
                trace.final_response += f"\n\n*(Note: Executed via Cognitive Engine fallback. Gemini API call returned: {str(e)[:100]}...)*"
                return trace

        # Default: high-precision Built-in Cognitive Agent Engine
        return cognitive_engine.process(trace)

    def _execute_gemini_workflow(self, trace: WorkflowExecutionTrace, api_key: str) -> WorkflowExecutionTrace:
        from google import genai
        client = genai.Client(api_key=api_key)
        
        # First execute cognitive tools to populate real data and steps
        trace = cognitive_engine.process(trace)
        
        prompt = (
            f"You are the Supervisor Agent for NEXUS International Banking Corp.\n"
            f"Customer ID: {trace.customer_id}\n"
            f"User Query: {trace.sanitized_message}\n"
            f"Active Specialist Agents: {', '.join(trace.active_agents)}\n"
            f"Specialist Agent Findings and Tool Results:\n"
            + "\n".join([f"- [{s.agent_name}] {s.title}: {s.content}" for s in trace.steps])
            + "\n\nPlease generate a professional, authoritative, and helpful banking customer response in markdown formatting based on these agent findings."
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        if response.text:
            trace.final_response = response.text
        return trace

llm_manager = LLMProviderManager()
