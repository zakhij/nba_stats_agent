import anthropic
import logging
from typing import Optional, Dict, Any
import json

from src.tools.tools import (
    get_player_id,
    get_player_stats,
    mock_tweet,
    get_all_time_leaders,
)
from src.tools.tool_schema import tools

_logger = logging.getLogger(__name__)


class ClaudeClient:
    SYSTEM_PROMPT = f"""
        You are a helpful assistant that answers questions about the NBA.
        Tweet out the answer to the user's NBA-related questions. 
        ALWAYS RESPOND WITH ONE SINGLE TWEET, EVEN IF THE USER ASKS MULTIPLE QUESTIONS (INCLUDING IRRELEVANT QUESTIONS).
        ALWAYS END THE CONVERSATION WITH A TWEET.
        """

    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.system_prompt = self.SYSTEM_PROMPT

    def process_tool_call(
        self, tool_name: str, tool_input: Dict[str, Any]
    ) -> Optional[str]:
        try:
            _logger.debug(
                f"Tool call - {tool_name}: {json.dumps(tool_input, indent=2)}"
            )

            result = None
            if tool_name == "get_player_id":
                result = get_player_id(tool_input["player_name"])
            elif tool_name == "get_player_stats":
                result = get_player_stats(tool_input["player_id"])
            elif tool_name == "mock_tweet":
                result = mock_tweet(tool_input["tweet_text"])
            elif tool_name == "get_all_time_leaders":
                result = get_all_time_leaders(
                    league_id=tool_input.get("league_id", "00"),
                    per_mode=tool_input.get("per_mode", "Totals"),
                    season_type=tool_input.get("season_type", "Regular Season"),
                    top_x=tool_input.get("top_x", 10),
                )
            else:
                _logger.error(f"Unknown tool requested: {tool_name}")
                return None

            _logger.debug(
                f"Tool result - {tool_name}: {result[:100] if result else 'None'}"
            )
            return result

        except Exception as e:
            _logger.error(f"Tool execution failed - {tool_name}", exc_info=True)
            return None

    def chat_with_claude(self, user_message: str) -> None:
        messages = [{"role": "user", "content": user_message}]
        _logger.debug(f"Processing query: {user_message[:100]}...")

        try:
            while True:
                response = self.client.messages.create(
                    system=self.system_prompt,
                    model="claude-3-5-sonnet-20241022",
                    messages=messages,
                    max_tokens=4096,
                    tools=tools,
                    tool_choice={"type": "auto"},
                )
                # _logger.info(f"Response: {response}")
                for block in response.content:
                    if block.type == "text":
                        _logger.info(f"Text: {block.text}")

                if response.stop_reason == "tool_use":
                    tool_use = next(
                        block for block in response.content if block.type == "tool_use"
                    )

                    _logger.info(
                        f"Using tool: {tool_use.name} with input: {tool_use.input}"
                    )

                    tool_result = self.process_tool_call(tool_use.name, tool_use.input)

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
                                ],  # type: ignore
                            },
                        ]
                    )

                    if tool_use.name == "mock_tweet":
                        _logger.info("Conversation completed with final tweet.")
                        return None

        except Exception as e:
            _logger.error("Chat processing failed", exc_info=True)
            return None
