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
    {
        "name": "get_all_time_leaders",
        "description": "Gets NBA all-time statistical leaders across multiple categories (points, assists, rebounds, etc). Returns top X players for each stat category.",
        "input_schema": {
            "type": "object",
            "properties": {
                "league_id": {
                    "type": "string",
                    "description": "NBA League ID (00 for NBA)",
                    "default": "00",
                },
                "per_mode": {
                    "type": "string",
                    "description": "How stats are represented (Totals or PerGame)",
                    "enum": ["Totals", "PerGame"],
                    "default": "Totals",
                },
                "season_type": {
                    "type": "string",
                    "description": "Type of season stats to retrieve",
                    "enum": ["Regular Season", "Playoffs", "All Star"],
                    "default": "Regular Season",
                },
                "top_x": {
                    "type": "integer",
                    "description": "Number of top players to return (e.g., top 10)",
                    "default": 10,
                },
            },
            "required": ["league_id", "per_mode", "season_type", "top_x"],
        },
    },
]
