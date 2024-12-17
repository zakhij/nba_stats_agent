tools = [
    {
        "name": "get_player_id",
        "description": "A tool that gets the player id for a given NBA player, which is used to get the player stats.",
        "input_schema": {
            "type": "object",
            "properties": {
                "player_name": {
                    "type": "string",
                    "description": "The name of the NBA player to get the id for.",
                }
            },
            "required": ["player_name"],
        },
    },
    {
        "name": "get_player_stats",
        "description": "A tool that gets the stats for a given NBA player.",
        "input_schema": {
            "type": "object",
            "properties": {
                "player_id": {
                    "type": "string",
                    "description": "The id of the NBA player to get stats for.",
                }
            },
            "required": ["player_id"],
        },
    },
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
