import logging
from typing import Optional, Dict, Any
from src.services.claude_service import ClaudeService
from src.services.tool_manager import ToolManager

_logger = logging.getLogger(__name__)


class TweeterAgent:
    SYSTEM_PROMPT = """
    You are a professional social media expert specializing in NBA content.
    Your role is to evaluate the NBA information for relevance to the original question.
    If the NBA information is relevant, format it into an engaging tweet (max 280 characters)
    using the mock tweet tool. If not, use the mock_tweet tool with the response "This is not relevant to the original question."
    
    """

    def __init__(self, claude_service: ClaudeService, tool_manager: ToolManager):
        self.claude_service = claude_service
        self.tool_manager = tool_manager
        self.system_prompt = self.SYSTEM_PROMPT

    def evaluate_and_tweet(self, original_query: str, nba_response: str) -> None:
        _logger.debug(f"Processing NBA response for query: {original_query[:100]}...")

        messages = [
            {
                "role": "user",
                "content": f"""
                Original Question: {original_query}
                NBA Response: {nba_response}
                """,
            }
        ]

        try:
            response = self.claude_service.create_message(
                system_prompt=self.system_prompt,
                messages=messages,
                tools=self.tool_manager.get_tool_schemas(),
                tool_choice={"type": "any"},
            )

            if response.stop_reason == "tool_use":
                tool_use = next(
                    block for block in response.content if block.type == "tool_use"
                )
                tool_result = self.tool_manager.execute_tool(
                    tool_use.name, tool_use.input
                )

                return None

        except Exception as e:
            _logger.error(f"Error processing tweet.")
            return None