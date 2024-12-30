import tweepy
import logging
from typing import Optional, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Mention:
    id: str
    text: str
    author_id: str
    created_at: datetime


_logger = logging.getLogger(__name__)


class TwitterService:
    def __init__(
        self, api_key: str, api_secret: str, access_token: str, access_token_secret: str
    ):
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
        self.bot_user = self.api.verify_credentials()

    def get_mentions(self, since_id: Optional[str] = None) -> List[Mention]:
        try:
            mentions = self.api.mentions_timeline(
                since_id=since_id, tweet_mode="extended"
            )

            return [
                Mention(
                    id=str(mention.id),
                    text=mention.full_text,
                    author_id=str(mention.user.id),
                    created_at=mention.created_at,
                )
                for mention in mentions
            ]

        except Exception as e:
            _logger.error("Failed to fetch mentions", exc_info=True)
            return []

    def reply_to_tweet(self, tweet_id: str, content: str) -> Optional[str]:
        if not content or len(content) > 280:
            _logger.error(
                f"Invalid tweet content length: {len(content) if content else 0}"
            )
            return None

        reply = self.api.update_status(
            status=content,
            in_reply_to_status_id=tweet_id,
            auto_populate_reply_metadata=True,
        )

        _logger.info(f"Reply posted successfully: {reply.id}")
        return str(reply.id)
