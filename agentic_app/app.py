from typing import Any, Optional
import logging
from .agent import Agent
from .tools import ToolRegistry, Tool

logger = logging.getLogger(__name__)


class AgenticApp:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.agent = Agent(verbose=verbose)
        self.tool_registry = self.agent.tool_registry

    def query(self, query_string: str) -> Any:
        if not query_string or not query_string.strip():
            raise ValueError("Query cannot be empty")
        
        try:
            result = self.agent.execute(query_string)
            return result
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise

    def register_tool(self, tool: Tool) -> None:
        try:
            self.tool_registry.register(tool)
            logger.info(f"Registered tool: {tool.name}")
        except ValueError as e:
            logger.error(f"Failed to register tool: {e}")
            raise

    def list_tools(self) -> list:
        return self.tool_registry.list_all()

    def get_tool_info(self, tool_name: str) -> Optional[dict]:
        tool = self.tool_registry.get(tool_name)
        if not tool:
            return None
        
        return {
            "name": tool.name,
            "description": tool.description,
            "type": tool.tool_type.value,
            "parameters": [
                {
                    "name": p.name,
                    "type": p.param_type,
                    "required": p.required,
                    "description": p.description,
                    "default": p.default,
                }
                for p in tool.parameters
            ]
        }

    def get_execution_summary(self) -> str:
        return self.agent.get_execution_summary()


def create_app(verbose: bool = False) -> AgenticApp:
    return AgenticApp(verbose=verbose)
