import os
from dotenv import load_dotenv
import logging

load_dotenv()

from src.services.claude_service import ClaudeService
from src.services.tool_manager import ToolManager
from src.agents.nba_agent import NBAAgent
from src.tools.tools import (
    get_player_id,
    get_player_stats,
    mock_tweet,
    get_all_time_leaders,
)
from src.tools.tool_schema import tools


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

    for tool in tools:
        if tool["name"] == "get_player_id":
            tool_manager.register_tool("get_player_id", get_player_id, tool)
        elif tool["name"] == "get_player_stats":
            tool_manager.register_tool("get_player_stats", get_player_stats, tool)
        elif tool["name"] == "mock_tweet":
            tool_manager.register_tool("mock_tweet", mock_tweet, tool)
        elif tool["name"] == "get_all_time_leaders":
            tool_manager.register_tool(
                "get_all_time_leaders", get_all_time_leaders, tool
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
