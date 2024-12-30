import logging
from typing import List, Dict, Any
import anthropic
from anthropic.types import Message


_logger = logging.getLogger(__name__)


class ClaudeService:
    MAX_TOKENS = 4096
    MODEL = "claude-3-5-sonnet-20241022"

    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def create_message(
        self,
        system_prompt: str,
        messages: List[Dict[str, Any]],
        tools: List[Dict[str, Any]],
        tool_choice: Dict[str, str],
    ) -> Message:
        return self.client.messages.create(
            system=system_prompt,
            model=self.MODEL,
            messages=messages,
            max_tokens=self.MAX_TOKENS,
            tools=tools,
            tool_choice=tool_choice,
        )
