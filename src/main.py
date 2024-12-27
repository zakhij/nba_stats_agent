import os
from dotenv import load_dotenv
import logging

load_dotenv()

from src.services.claude_service import ClaudeService
from src.services.tool_manager import ToolManager
from src.agents.nba_agent import NBAAgent
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
)
from src.tools.other_tools import mock_tweet
from src.tools.nba_tool_schema import nba_tools
from src.tools.other_tool_schema import other_tools


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


def setup_tool_manager() -> ToolManager:
    tool_manager = ToolManager()

    tool_map = {
        "get_player_id": get_player_id,
        "get_player_stats": get_player_stats,
        "get_all_time_leaders": get_all_time_leaders,
        "get_league_leaders": get_league_leaders,
        "get_player_recent_games": get_player_recent_games,
        "get_team_roster": get_team_roster,
        "get_league_standings": get_league_standings,
        "get_team_game_logs": get_team_game_logs,
        "get_box_score_summary": get_box_score_summary,
        "mock_tweet": mock_tweet,
    }

    for nba_tool in nba_tools:
        if nba_tool["name"] in tool_map:
            tool_manager.register_tool(
                nba_tool["name"], tool_map[nba_tool["name"]], nba_tool
            )

    for other_tool in other_tools:
        if other_tool["name"] in tool_map:
            tool_manager.register_tool(
                other_tool["name"], tool_map[other_tool["name"]], other_tool
            )

    return tool_manager


def main() -> None:
    setup_logging()
    _logger = logging.getLogger(__name__)

    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY") or ""

    if not api_key:
        _logger.error("No API key found in environment variables")
        return

    claude_service = ClaudeService(api_key)
    tool_manager = setup_tool_manager()
    nba_agent = NBAAgent(claude_service, tool_manager)

    _logger.info("NBA agent initialized successfully")

    while True:
        ask = input("Ask the LLM: ")
        if ask == "exit":
            _logger.info("Exiting application")
            break
        nba_agent.chat(ask, tool_choice_type="any")


if __name__ == "__main__":
    main()
