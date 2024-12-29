import logging
from datetime import datetime
from typing import Optional
from src.agents.base_agent import BaseAgent

_logger = logging.getLogger(__name__)


class NBAAgent(BaseAgent):
    SYSTEM_PROMPT = f"""
    You are a helpful assistant that answers questions about the NBA.
    Tweet out the answer to the user's NBA-related questions. 
    Maintain a neutral, calm tone and avoid using emojis.
    If the user's query is not about the NBA, respond with a tweet saying "I'm sorry, I can only answer questions about the NBA."
    ALWAYS RESPOND WITH ONE SINGLE TWEET, EVEN IF THE USER ASKS MULTIPLE QUESTIONS (INCLUDING IRRELEVANT QUESTIONS).
    ALWAYS END THE CONVERSATION WITH A TWEET.
    SOME IMPORTANT INFORMATION:
    - Today's date is {datetime.now().strftime('%B %d, %Y')}
    """
    MAX_TURNS = 6

    def get_nba_response(
        self, user_message: str, tool_choice_type: str = "any"
    ) -> Optional[str]:
        messages = [{"role": "user", "content": user_message}]
        _logger.debug(f"Processing query: {user_message[:100]}...")

        turn_count = 0
        try:
            while True:
                turn_count += 1
                if turn_count > self.MAX_TURNS:
                    _logger.warning(
                        "Conversation exceeded max turns. Ending conversation."
                    )
                    return None

                if not self.get_tool_schemas():
                    _logger.error("Tool schemas are not initialized")
                    return None

                _logger.debug(f"Turn {turn_count}")
                response = self.claude_service.create_message(
                    system_prompt=self.SYSTEM_PROMPT,
                    messages=messages,
                    tools=self.get_tool_schemas() or [],
                    tool_choice={"type": tool_choice_type},
                )

                for block in response.content:
                    if block.type == "text":
                        _logger.info(f"Text: {block.text}")

                if response.stop_reason == "tool_use":
                    conversation_continuing = (
                        self._handle_multiple_tools(response, messages)
                        if tool_choice_type == "any"
                        else self._handle_single_tool(response, messages)
                    )

                    tool_uses = [
                        block for block in response.content if block.type == "tool_use"
                    ]
                    if any(
                        tool.name == "generate_final_response" for tool in tool_uses
                    ):
                        return conversation_continuing

        except Exception as e:
            _logger.error("Chat processing failed", exc_info=True)
            return None

    def _handle_multiple_tools(self, response, messages) -> Optional[str]:
        tool_uses = [block for block in response.content if block.type == "tool_use"]
        tool_results = []

        for tool_use in tool_uses:
            tool_result = self.execute_tool(tool_use.name, tool_use.input)
            if tool_use.name == "generate_final_response":
                return tool_result

            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": tool_result,
                }
            )

        messages.extend(
            [
                {
                    "role": "assistant",
                    "content": [block.dict() for block in response.content],
                },
                {"role": "user", "content": tool_results},
            ]
        )

    def _handle_single_tool(self, response, messages) -> Optional[str]:
        tool_use = next(block for block in response.content if block.type == "tool_use")
        tool_result = self.execute_tool(tool_use.name, tool_use.input)

        if tool_use.name == "generate_final_response":
            _logger.info("Conversation completed with final tweet.")
            return tool_result

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
