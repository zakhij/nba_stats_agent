from src.tools.nba_parameters import params

nba_tools = [
    {
        "name": "generate_final_response",
        "description": "A tool that generates the final response for the conversation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "answer": {
                    "type": "string",
                    "description": "Your comprehensive answer",
                },
                "confidence": {
                    "type": "string",
                    "enum": ["high", "medium", "low"],
                    "description": "Confidence level in the answer",
                },
                "data_sources": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of tools used to gather this information",
                },
            },
            "required": ["answer", "confidence", "data_sources"],
        },
    },
    {
        "name": "get_player_id",
        "description": "A tool that gets the player id for a given NBA player, which is used to get the player stats.",
        "input_schema": {
            "type": "object",
            "properties": {
                "player_name": params["player_name"],
            },
            "required": ["player_name"],
        },
    },
    {
        "name": "get_player_stats",
        "description": "A tool that gets the stats for a given NBA player.",
        "input_schema": {
            "type": "object",
            "properties": {"player_id": params["player_id"]},
            "required": ["player_id"],
        },
    },
    {
        "name": "get_all_time_leaders",
        "description": "Gets NBA all-time statistical leaders across multiple categories (points, assists, rebounds, etc). Returns top X players for each stat category.",
        "input_schema": {
            "type": "object",
            "properties": {
                "league_id": params["league_id"],
                "per_mode_simple": params["per_mode_simple"],
                "season_type": params["season_type"],
                "top_x": params["top_x"],
            },
            "required": ["top_x"],
        },
    },
    {
        "name": "get_league_leaders",
        "description": "Fetches NBA league leaders for a specific statistical category.",
        "input_schema": {
            "type": "object",
            "properties": {
                "stat_category": params["stat_category"],
                "season": params["season"],
                "season_type_all_star": params["season_type_all_star"],
                "per_mode48": params["per_mode48"],
            },
            "required": ["stat_category"],
        },
    },
    {
        "name": "get_player_recent_games",
        "description": "Fetches a player's recent game performances.",
        "input_schema": {
            "type": "object",
            "properties": {
                "player_id": params["player_id"],
                "last_n_games": params["last_n_games"],
            },
            "required": ["player_id", "last_n_games"],
        },
    },
    {
        "name": "get_team_roster",
        "description": "Fetches the current roster for an NBA team.",
        "input_schema": {
            "type": "object",
            "properties": {
                "team_id": params["team_id"],
                "season": params["season"],
            },
            "required": ["team_id"],
        },
    },
    {
        "name": "get_league_standings",
        "description": "Gets current NBA standings including conference rankings, win/loss records, and streaks.",
        "input_schema": {
            "type": "object",
            "properties": {
                "league_id": params["league_id"],
                "season": params["season"],
                "season_type": params["season_type"],
            },
            "required": ["league_id", "season", "season_type"],
        },
    },
    {
        "name": "get_team_game_logs",
        "description": "Fetches detailed game logs for a team including basic stats and rankings.",
        "input_schema": {
            "type": "object",
            "properties": {
                "team_id": params["team_id"],
                "date_from": params["date_from"],
                "date_to": params["date_to"],
                "season_type": params["season_type"],
            },
            "required": ["team_id"],
        },
    },
    {
        "name": "get_box_score_summary",
        "description": "Gets comprehensive game summary including line scores, team stats, officials, and game info.",
        "input_schema": {
            "type": "object",
            "properties": {
                "game_id": params["game_id"],
            },
            "required": ["game_id"],
        },
    },
]
