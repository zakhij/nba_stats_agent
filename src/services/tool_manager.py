import logging
from typing import Dict, Any, Optional, Callable, List
import json

_logger = logging.getLogger(__name__)


class ToolManager:
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self.tool_schemas: List[Dict[str, Any]] = []

    def register_tool(self, name: str, func: Callable, schema: Dict[str, Any]) -> None:
        self.tools[name] = func
        self.tool_schemas.append({"name": name, **schema})

    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        return self.tool_schemas

    def execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> Optional[str]:
        try:
            _logger.debug(
                f"Calling tool - {tool_name}: {json.dumps(tool_input, indent=2)}"
            )

            if tool_name not in self.tools:
                _logger.error(f"Unknown tool requested: {tool_name}")
                return None

            result = self.tools[tool_name](**tool_input)

            _logger.debug(
                f"Result from tool - {tool_name}: {str(result)[:100] if result else 'None'}"
            )
            return result

        except Exception as e:
            _logger.error(f"Tool execution failed - {tool_name}", exc_info=True)
            return None
