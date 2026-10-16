from typing import Dict, Any, Optional
from app.core.models import AgentRole, AgentThoughtStep, StepType
from app.tools.banking_tools import tools

class BaseAgent:
    def __init__(self, role: AgentRole, description: str):
        self.role = role
        self.description = description

    def execute_tool(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        return tools.execute_tool(tool_name, self.role.value, args)

    def log_thought(self, title: str, thought: str) -> AgentThoughtStep:
        return AgentThoughtStep(
            agent_name=self.role.value,
            step_type=StepType.THOUGHT,
            title=title,
            content=thought
        )

    def log_tool_call(self, tool_name: str, args: Dict[str, Any], result: Dict[str, Any]) -> AgentThoughtStep:
        return AgentThoughtStep(
            agent_name=self.role.value,
            step_type=StepType.TOOL_CALL,
            title=f"Invoking MCP Tool: {tool_name}",
            content=f"Calling {tool_name} with parameters: {args}",
            tool_name=tool_name,
            tool_args=args,
            tool_result=result
        )
