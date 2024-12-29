import logging
from typing import Optional
from src.agents.base_agent import BaseAgent
import logging

_logger = logging.getLogger(__name__)


class TweeterAgent(BaseAgent):
    SYSTEM_PROMPT = """
    You are a professional social media expert specializing in NBA content.
    Your role is to evaluate the NBA information for relevance to the original question.
    If the NBA information is relevant, format it into an engaging tweet (max 280 characters)
    using the mock tweet tool. If not, use the mock_tweet tool with the response "This is not relevant to the original question."
    """

    def evaluate_and_tweet(
        self, original_query: str, nba_response: str
    ) -> Optional[str]:
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
            if not self.get_tool_schemas():
                _logger.error("Tool schemas are not initialized")
                return None

            response = self.claude_service.create_message(
                system_prompt=self.SYSTEM_PROMPT,
                messages=messages,
                tools=self.get_tool_schemas() or [],
                tool_choice={"type": "any"},
            )

            if response.stop_reason == "tool_use":
                tool_use = next(
                    block for block in response.content if block.type == "tool_use"
                )
                tool_result = self.execute_tool(tool_use.name, tool_use.input)

                return tool_result

        except Exception as e:
            _logger.error("Error processing tweet.", exc_info=True)
            return None
