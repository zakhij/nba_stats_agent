import os
from dotenv import load_dotenv
import logging
from src.claude_testing import ClaudeClient

load_dotenv()

_logger = logging.getLogger(__name__)


def main() -> None:
    # logging.basicConfig(level=logging.DEBUG)
    load_dotenv()

    api_key = os.getenv("ANTHROPIC_API_KEY") or ""

    claude_client = ClaudeClient(api_key)
    ex = claude_client.chat_with_claude("What bball games are on today?")
    print(f"\n FINAL RESPONSE: {ex}")


if __name__ == "__main__":
    main()
