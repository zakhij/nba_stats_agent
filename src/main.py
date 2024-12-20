import os
from dotenv import load_dotenv
import logging

from src.claude_testing import ClaudeClient
import nba_api

load_dotenv()


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Quiet down external libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("anthropic").setLevel(logging.WARNING)


def main() -> None:
    setup_logging()
    _logger = logging.getLogger(__name__)

    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY") or ""

    if not api_key:
        _logger.error("No API key found in environment variables")
        return

    claude_client = ClaudeClient(api_key)
    _logger.info("Claude client initialized successfully")

    while True:
        ask = input("Ask the LLM: ")
        if ask == "exit":
            _logger.info("Exiting application")
            break
        claude_client.chat_with_claude_any(ask)


if __name__ == "__main__":
    main()
