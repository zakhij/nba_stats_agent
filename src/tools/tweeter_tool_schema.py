tweeter_tools = [
    {
        "name": "mock_tweet",
        "description": "A tool that mocks tweets a given text.",
        "input_schema": {
            "type": "object",
            "properties": {
                "tweet_text": {
                    "type": "string",
                    "description": "The text to mock tweet.",
                }
            },
            "required": ["tweet_text"],
        },
    },
]
