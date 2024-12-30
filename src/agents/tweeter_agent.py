import logging
from typing import Optional, List
from src.agents.base_agent import BaseAgent
from src.services.twitter_service import TwitterService, Mention

_logger = logging.getLogger(__name__)


class TweeterAgent(BaseAgent):
    SYSTEM_PROMPT = """
    You are a professional social media expert specializing in NBA content.
    Your role is to evaluate the NBA information for relevance to the original question.
    If the NBA information is relevant, format it into an engaging tweet (max 280 characters)
    using the mock tweet tool. If not, use the mock_tweet tool with the response "This is not relevant to the original question."
    """

    def __init__(
        self,
        claude_service,
        tool_schemas,
        tool_module_path,
        twitter_service: TwitterService,
    ):
        super().__init__(claude_service, tool_schemas, tool_module_path)
        self.twitter_service = twitter_service
        self.last_mention_id = None

    def check_mentions(self) -> Optional[List[Mention]]:
        """Check for new mentions and process them."""
        mentions = self.twitter_service.get_mentions(since_id=self.last_mention_id)

        if mentions:
            self.last_mention_id = mentions[0].id
            return mentions

        return []

    def reply_to_mention(self, mention_id: str, content: str) -> Optional[str]:
        """Reply to a specific mention."""
        return self.twitter_service.reply_to_tweet(mention_id, content)

    def evaluate_and_tweet(
        self, original_query: str, nba_response: str, mention_id: Optional[str] = None
    ) -> Optional[str]:
        """Evaluate NBA response and post tweet."""
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
            tweet_content = self.execute_tool(tool_use.name, tool_use.input)

            if mention_id:
                return self.reply_to_mention(mention_id, tweet_content or "")
            return tweet_content
