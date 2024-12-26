nba_tools = [
    {
        "name": "get_player_id",
        "description": "A tool that gets the player id for a given NBA player, which is used to get the player stats.",
        "input_schema": {
            "type": "object",
            "properties": {
                "player_name": {
                    "type": "string",
                    "description": "NBA.com player ID",
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
                    "description": "Number of top players to return",
                },
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
                "stat_category": {
                    "type": "string",
                    "description": "Statistical category (PTS, AST, REB, STL, BLK)",
                    "enum": ["PTS", "AST", "REB", "STL", "BLK"],
                },
                "season": {
                    "type": "string",
                    "description": "NBA season (e.g., '2024-25')",
                },
                "season_type_all_star": {
                    "type": "string",
                    "description": "Season type (Regular Season, Playoffs, All Star)",
                    "enum": ["Regular Season", "Playoffs", "All Star", "Pre Season"],
                    "default": "Regular Season",
                },
                "per_mode48": {
                    "type": "string",
                    "description": "How to display statistics (PerGame or Totals)",
                    "enum": ["PerGame", "Totals"],
                    "default": "Totals",
                },
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
                "player_id": {"type": "string", "description": "NBA.com player ID"},
                "last_n_games": {
                    "type": "integer",
                    "description": "Number of recent games to return",
                },
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
                "team_id": {"type": "string", "description": "NBA.com team ID"},
                "season": {
                    "type": "string",
                    "description": "NBA season (e.g., '2024-25')",
                },
            },
            "required": ["team_id"],
        },
    },
]
