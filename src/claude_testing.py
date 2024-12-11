import anthropic

from src.tools.tools import add_two_integers
from src.tools.tool_schema import tools


class ClaudeClient:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def process_tool_call(self, tool_name, tool_input):
        if tool_name == "add_two_integers":
            return add_two_integers(tool_input["integer1"], tool_input["integer2"])

    def chat_with_claude(self, user_message):
        print(f"\n{'='*50}\nUser Message: {user_message}\n{'='*50}")

        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            messages=[{"role": "user", "content": user_message}],
            tools=tools,
        )

        print(f"\nInitial Response:")
        print(f"Stop Reason: {message.stop_reason}")
        print(f"Content: {message.content}")

        if message.stop_reason == "tool_use":
            tool_use = next(
                block for block in message.content if block.type == "tool_use"
            )
            tool_name = tool_use.name
            tool_input = tool_use.input

            print(f"\nTool Used: {tool_name}")
            print(f"Tool Input: {tool_input}")

            tool_result = self.process_tool_call(tool_name, tool_input)

            print(f"Tool Result: {tool_result}")

            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": user_message},
                    {"role": "assistant", "content": message.content},
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
                ],
                tools=tools,
            )
        else:
            response = message

        final_response = next(
            (block.text for block in response.content if hasattr(block, "text")),
            None,
        )
        return final_response
