import os

from dotenv import load_dotenv
import anthropic

load_dotenv()


def get_claude_response():
    client = anthropic.Anthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY"),
    )
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello, Claude"}],
    )
    print(message.content)


def main():
    get_claude_response()


if __name__ == "__main__":
    main()
