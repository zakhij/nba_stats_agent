import os
from dotenv import load_dotenv
import logging

from src.claude_testing import ClaudeClient
import nba_api

load_dotenv()

_logger = logging.getLogger(__name__)


def main() -> None:
    # logging.basicConfig(level=logging.DEBUG)
    load_dotenv()

    api_key = os.getenv("ANTHROPIC_API_KEY") or ""

    claude_client = ClaudeClient(api_key)

    while True:
        ask = input("Ask the LLM: ")
        if ask == "exit":
            break
        ex = claude_client.chat_with_claude(ask)
        print(f"\n FINAL RESPONSE: {ex}\n")


if __name__ == "__main__":
    main()
