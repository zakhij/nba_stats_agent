from src.services.claude_service import ClaudeService
from typing import List, Dict, Any, Callable, Optional
from abc import ABC
import logging
import json
import importlib

_logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    def __init__(
        self,
        claude_service: ClaudeService,
        tool_schemas: Optional[List[Dict[str, Any]]] = None,
        tool_module_path: Optional[str] = None,  # e.g., "src.tools.nba_tools"
    ):
        self.claude_service = claude_service
        self.tool_schemas = tool_schemas
        self.tool_map = self._build_tool_map(tool_module_path)

    def _build_tool_map(self, module_path: Optional[str]) -> Dict[str, Callable]:
        if not module_path or not self.tool_schemas:
            return {}
        module = importlib.import_module(module_path)
        return {
            schema["name"]: getattr(module, schema["name"])
            for schema in self.tool_schemas
            if hasattr(module, schema["name"])
        }

    def get_tool_schemas(self) -> Optional[List[Dict[str, Any]]]:
        return self.tool_schemas

    def execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> Optional[str]:
        try:
            _logger.debug(
                f"Calling tool - {tool_name}: {json.dumps(tool_input, indent=2)}"
            )
            if not self.tool_map or tool_name not in self.tool_map:
                _logger.error(
                    f"Tool map is empty or missing requested tool: {tool_name}"
                )
                return None

            result = self.tool_map[tool_name](**tool_input)

            _logger.debug(
                f"Result from tool - {tool_name}: {str(result)[:100] if result else 'None'}"
            )
            return result

        except Exception as e:
            _logger.error(f"Tool execution failed - {tool_name}", exc_info=True)
            return None
