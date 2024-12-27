from src.tools.nba_parameters import params

nba_tools = [
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
                "per_mode": params["per_mode"],
                "season_type": params["season_type"],
                "top_x": params["top_x"],
            },
            "required": ["league_id", "per_mode", "season_type", "top_x"],
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
]
