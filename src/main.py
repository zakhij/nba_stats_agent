import os
from dotenv import load_dotenv
import logging
from typing import Dict, Callable, Tuple

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


def setup_logging():

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    noisy_loggers = ["httpx", "anthropic", "urllib3", "requests", "httpcore"]

    for logger_name in noisy_loggers:
        logging.getLogger(logger_name).propagate = False

    app_logger = logging.getLogger("src")
    app_logger.setLevel(logging.DEBUG)


def main() -> None:
    setup_logging()
    _logger = logging.getLogger(__name__)

    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY") or ""

    if not api_key:
        _logger.error("No API key found in environment variables")
        return

    claude_service = ClaudeService(api_key)

    nba_agent = NBAAgent(
        claude_service=claude_service,
        tool_schemas=nba_tools,
        tool_module_path="src.tools.nba_tools",
    )

    tweeter_agent = TweeterAgent(
        claude_service=claude_service,
        tool_schemas=tweeter_tools,
        tool_module_path="src.tools.tweeter_tools",
    )

    _logger.info("Agents initialized successfully")

    while True:
        ask = input("Ask the LLM: ")
        if ask == "exit":
            _logger.info("Exiting application")
            break
        answer = nba_agent.chat(ask, tool_choice_type="any")
        if answer:
            tweeter_agent.evaluate_and_tweet(ask, answer)


if __name__ == "__main__":
    main()
