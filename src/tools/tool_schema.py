tools = [
    {
        "name": "add_two_integers",
        "description": "A simple tool that adds two integers.",
        "input_schema": {
            "type": "object",
            "properties": {
                "integer1": {
                    "type": "integer",
                    "description": "The first integer to add.",
                },
                "integer2": {
                    "type": "integer",
                    "description": "The second integer to add.",
                },
            },
            "required": ["integer1", "integer2"],
        },
    },
    {
        "name": "get_scoreboard",
        "description": "A tool that gets the scoreboard for today's NBA games.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
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
]
