import os
from dotenv import load_dotenv
import logging
from typing import Dict, Callable, Tuple
import time

load_dotenv()

from src.services.claude_service import ClaudeService
from src.agents.nba_agent import NBAAgent
from src.agents.tweeter_agent import TweeterAgent
from src.tools.nba_tools import (
    get_player_id,
    get_player_stats,
    get_all_time_leaders,
    get_league_leaders,
    get_player_recent_games,
    get_team_roster,
    get_league_standings,
    get_team_game_logs,
    get_box_score_summary,
    generate_final_response,
)
from src.tools.tweeter_tools import mock_tweet
from src.tools.nba_tool_schema import nba_tools
from src.tools.tweeter_tool_schema import tweeter_tools
from src.services.twitter_service import TwitterService


def setup_logging():

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    noisy_loggers = [
        "httpx",
        "anthropic",
        "urllib3",
        "requests",
        "httpcore",
        "requests_oauthlib",
        "oauthlib",
        "tweepy",
    ]

    for logger_name in noisy_loggers:
        logging.getLogger(logger_name).propagate = False

    app_logger = logging.getLogger("src")
    app_logger.setLevel(logging.DEBUG)


def main() -> None:
    setup_logging()
    _logger = logging.getLogger(__name__)

    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY") or ""
    twitter_api_key = os.getenv("TWITTER_API_KEY") or ""
    twitter_api_secret = os.getenv("TWITTER_API_SECRET") or ""
    twitter_access_token = os.getenv("TWITTER_ACCESS_TOKEN") or ""
    twitter_access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET") or ""

    if not api_key:
        _logger.error("No API key found in environment variables")
        return

    claude_service = ClaudeService(api_key)

    if (
        not twitter_api_key
        or not twitter_api_secret
        or not twitter_access_token
        or not twitter_access_token_secret
    ):
        _logger.error(
            "No Twitter API key, secret, access token, or access token secret found in environment variables"
        )
        return

    twitter_service = TwitterService(
        api_key=twitter_api_key,
        api_secret=twitter_api_secret,
        access_token=twitter_access_token,
        access_token_secret=twitter_access_token_secret,
    )

    nba_agent = NBAAgent(
        claude_service=claude_service,
        tool_schemas=nba_tools,
        tool_module_path="src.tools.nba_tools",
    )

    tweeter_agent = TweeterAgent(
        claude_service=claude_service,
        tool_schemas=tweeter_tools,
        tool_module_path="src.tools.tweeter_tools",
        twitter_service=twitter_service,
    )

    _logger.info("Agents initialized successfully")

    while True:
        try:
            mentions = tweeter_agent.check_mentions()

            if mentions:
                for mention in mentions:
                    nba_response = nba_agent.get_nba_response(mention.text)
                    if nba_response:
                        tweeter_agent.evaluate_and_tweet(
                            mention.text, nba_response, mention_id=mention.id
                        )

            time.sleep(20)

        except Exception as e:
            _logger.error("Error in main loop", exc_info=True)
            time.sleep(20)


if __name__ == "__main__":
    main()
