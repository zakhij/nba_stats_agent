import anthropic

from src.tools.tools import (
    add_two_integers,
    get_scoreboard,
    get_player_id,
    get_player_stats,
    mock_tweet,
)
from src.tools.tool_schema import tools


class ClaudeClient:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def process_tool_call(self, tool_name, tool_input):
        if tool_name == "add_two_integers":
            return add_two_integers(tool_input["integer1"], tool_input["integer2"])
        elif tool_name == "get_scoreboard":
            return get_scoreboard()
        elif tool_name == "get_player_id":
            return get_player_id(tool_input["player_name"])
        elif tool_name == "get_player_stats":
            return get_player_stats(tool_input["player_id"])
        elif tool_name == "mock_tweet":
            return mock_tweet(tool_input["tweet_text"])

    def chat_with_claude(self, user_message):
        messages = [{"role": "user", "content": user_message}]
        print(f"\n{'='*50}\nUser Message: {user_message}\n{'='*50}")
        system_prompt = f"""
        You are a helpful assistant that answers questions about the NBA.
        Tweet out the answer to the user's NBA-related questions.
        """

        while True:
            response = self.client.messages.create(
                system=system_prompt,
                model="claude-3-5-sonnet-20241022",
                messages=messages,
                max_tokens=4096,
                tools=tools,
                tool_choice={"type": "auto"},
            )

            print("\nTURN")
            print(f"Content: {response.content}")
            print(f"Stop Reason: {response.stop_reason}")
            if response.stop_reason == "tool_use":

                tool_use = next(
                    block for block in response.content if block.type == "tool_use"
                )
                print(f"Tool Used: {tool_use.name}")
                print(f"Tool Input: {tool_use.input}")

                tool_result = self.process_tool_call(tool_use.name, tool_use.input)

                messages.extend(
                    [
                        {"role": "assistant", "content": response.content},
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "tool_result",
                                    "tool_use_id": tool_use.id,
                                    "content": tool_result,
                                }
                            ],
                        },
                    ]
                )
            else:
                break

        # Return final response
        final_response = next(
            (block.text for block in response.content if hasattr(block, "text")),
            None,
        )
        return final_response
