import logging
from typing import Dict, Any, List, Optional
from src.services.claude_service import ClaudeService
from src.services.tool_manager import ToolManager
import json

_logger = logging.getLogger(__name__)


class NBAAgent:
    SYSTEM_PROMPT = """
    You are a helpful assistant that answers questions about the NBA.
    Tweet out the answer to the user's NBA-related questions. 
    If the user's query is not about the NBA, respond with a tweet saying "I'm sorry, I can only answer questions about the NBA."
    ALWAYS RESPOND WITH ONE SINGLE TWEET, EVEN IF THE USER ASKS MULTIPLE QUESTIONS (INCLUDING IRRELEVANT QUESTIONS).
    ALWAYS END THE CONVERSATION WITH A TWEET.
    """

    def __init__(self, claude_service: ClaudeService, tool_manager: ToolManager):
        self.claude_service = claude_service
        self.tool_manager = tool_manager
        self.system_prompt = self.SYSTEM_PROMPT

    def chat(self, user_message: str, tool_choice_type: str = "any") -> None:
        messages = [{"role": "user", "content": user_message}]
        _logger.debug(f"Processing query: {user_message[:100]}...")

        try:
            while True:
                response = self.claude_service.create_message(
                    system_prompt=self.system_prompt,
                    messages=messages,
                    tools=self.tool_manager.get_tool_schemas(),
                    tool_choice={"type": tool_choice_type},
                )

                for block in response.content:
                    if block.type == "text":
                        _logger.info(f"Text: {block.text}")

                if response.stop_reason == "tool_use":
                    conversation_complete = False
                    if tool_choice_type == "any":
                        conversation_complete = self._handle_multiple_tools(
                            response, messages
                        )
                    else:
                        conversation_complete = self._handle_single_tool(
                            response, messages
                        )

                    if conversation_complete:
                        return

        except Exception as e:
            _logger.error("Chat processing failed", exc_info=True)

    def _handle_multiple_tools(self, response, messages) -> bool:
        tool_uses = [block for block in response.content if block.type == "tool_use"]
        tool_results = []

        for tool_use in tool_uses:
            tool_result = self.tool_manager.execute_tool(tool_use.name, tool_use.input)
            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": tool_result,
                }
            )

            if tool_use.name == "mock_tweet":
                _logger.info("Conversation completed with final tweet.")
                return True

        messages.extend(
            [
                {
                    "role": "assistant",
                    "content": json.dumps([block.dict() for block in response.content]),
                },
                {"role": "user", "content": json.dumps(tool_results)},
            ]
        )
        return False

    def _handle_single_tool(self, response, messages) -> bool:
        tool_use = next(block for block in response.content if block.type == "tool_use")
        tool_result = self.tool_manager.execute_tool(tool_use.name, tool_use.input)

        messages.extend(
            [
                {"role": "assistant", "content": response.content},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_use.id,
                            "content": tool_result,
                        }
                    ],
                },
            ]
        )

        if tool_use.name == "mock_tweet":
            _logger.info("Conversation completed with final tweet.")
            return True
        return False
