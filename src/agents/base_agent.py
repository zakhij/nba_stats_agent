from src.services.claude_service import ClaudeService
from typing import List, Dict, Any, Callable, Optional
from abc import ABC
import logging
import json

_logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    def __init__(
        self,
        claude_service: ClaudeService,
        tool_schemas: Optional[List[Dict[str, Any]]] = None,
        tool_map: Optional[Dict[str, Callable]] = None,
    ):
        self.claude_service = claude_service
        self.tool_schemas = tool_schemas
        self.tool_map = tool_map

    def get_tool_schemas(self) -> Optional[List[Dict[str, Any]]]:
        return self.tool_schemas

    def execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> Optional[str]:
        try:
            _logger.debug(
                f"Calling tool - {tool_name}: {json.dumps(tool_input, indent=2)}"
            )
            if not self.tool_map:
                _logger.error("Tool map is not initialized")
                return None

            if tool_name not in self.tool_map:
                _logger.error(f"Unknown tool requested: {tool_name}")
                return None

            result = self.tool_map[tool_name](**tool_input)

            _logger.debug(
                f"Result from tool - {tool_name}: {str(result)[:100] if result else 'None'}"
            )
            return result

        except Exception as e:
            _logger.error(f"Tool execution failed - {tool_name}", exc_info=True)
            return None
