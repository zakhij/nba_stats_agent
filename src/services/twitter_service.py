import tweepy
import logging
from typing import Optional

_logger = logging.getLogger(__name__)


class TwitterService:
    def __init__(
        self, api_key: str, api_secret: str, access_token: str, access_token_secret: str
    ):
        try:
            auth = tweepy.OAuthHandler(api_key, api_secret)
            auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(auth)

            self.api.verify_credentials()
            _logger.info("Twitter authentication successful")

        except Exception as e:
            _logger.error("Twitter authentication failed", exc_info=True)
            raise

    def post_tweet(self, content: str) -> Optional[str]:
        try:
            if not content or len(content) > 280:
                _logger.error(
                    f"Invalid tweet content length: {len(content) if content else 0}"
                )
                return None

            tweet = self.api.update_status(content)
            _logger.info(f"Tweet posted successfully: {tweet.id}")
            return str(tweet.id)

        except Exception as e:
            _logger.error("Failed to post tweet", exc_info=True)
            return None
