import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables
load_dotenv()


def get_claude_response(prompt: str, model: str = "claude-3-sonnet-20240229") -> str:
    """
    Get a response from Claude using the Anthropic API.

    Args:
        prompt (str): The input prompt for Claude
        model (str): The model to use (defaults to Claude 3 Sonnet)

    Returns:
        str: Claude's response
    """
    try:
        # Initialize Anthropic client with API key from .env
        client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

        # Create message and get response
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )

        return message.content[0].text

    except Exception as e:
        return f"Error: {str(e)}"


# Example usage
if __name__ == "__main__":
    test_prompt = (
        "Are you familiar with DX, software engineering intelligence? The company"
    )
    response = get_claude_response(test_prompt)
    print(f"Prompt: {test_prompt}")
    print(f"Response: {response}")
