params = {
    "player_id": {
        "type": "integer",
        "description": "NBA.com player ID",
    },
    "team_id": {
        "type": "integer",
        "description": "NBA.com team ID",
    },
    "league_id": {
        "type": "string",
        "description": "NBA League ID (00 for NBA)",
        "default": "00",
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
    "player_name": {
        "type": "string",
        "description": "NBA player name",
    },
    "season_type": {
        "type": "string",
        "description": "Type of season stats to retrieve",
        "enum": ["Regular Season", "Playoffs", "All Star"],
        "default": "Regular Season",
    },
    "per_mode_simple": {
        "type": "string",
        "description": "How stats are represented (Totals or PerGame)",
        "enum": ["Totals", "PerGame"],
        "default": "Totals",
    },
    "top_x": {
        "type": "integer",
        "description": "Number of top players to return",
    },
    "stat_category": {
        "type": "string",
        "description": "Statistical category (PTS, AST, REB, STL, BLK)",
        "enum": ["PTS", "AST", "REB", "STL", "BLK"],
    },
    "per_mode48": {
        "type": "string",
        "description": "How to display statistics (PerGame or Totals)",
        "enum": ["PerGame", "Totals"],
        "default": "Totals",
    },
    "last_n_games": {
        "type": "integer",
        "description": "Number of recent games to return",
    },
    "date_from": {
        "type": "string",
        "description": "Start date in format YYYY-MM-DD",
    },
    "date_to": {
        "type": "string",
        "description": "End date in format YYYY-MM-DD",
    },
    "game_id": {
        "type": "string",
        "description": "NBA.com game ID (10 digits)",
        "pattern": "^\\d{10}$",
    },
}
