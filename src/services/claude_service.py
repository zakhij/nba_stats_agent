import logging
from typing import List, Dict, Any, Optional
import anthropic
from anthropic.types import Message


_logger = logging.getLogger(__name__)


class ClaudeService:
    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def create_message(
        self,
        system_prompt: str,
        messages: List[Dict[str, Any]],
        tools: List[Dict[str, Any]],
        tool_choice: Dict[str, str],
    ) -> Message:
        try:
            return self.client.messages.create(
                system=system_prompt,
                model=self.model,
                messages=messages,
                max_tokens=4096,
                tools=tools,
                tool_choice=tool_choice,
            )
        except Exception as e:
            _logger.error("Failed to create message", exc_info=True)
            raise
