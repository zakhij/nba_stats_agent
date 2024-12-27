from typing import Optional

from nba_api.stats.static import players
from nba_api.stats.endpoints import (
    playercareerstats,
    alltimeleadersgrids,
    leagueleaders,
    playergamelogs,
    commonteamroster,
)


def get_player_id(player_name: str) -> str:
    player = players.find_players_by_full_name(player_name)
    return str(player[0]["id"])


def get_player_stats(player_id: str) -> str:
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    return career.get_json()


def get_all_time_leaders(
    top_x: int,
    league_id: Optional[int] = None,
    per_mode: Optional[str] = None,
    season_type: Optional[str] = None,
) -> str:
    """
    Fetches NBA all-time statistical leaders across multiple categories.
    Returns the data in JSON format.
    """

    kwargs: dict[str, int | str] = {
        "topx": top_x,
    }
    if league_id is not None:
        kwargs["league_id"] = league_id
    if per_mode is not None:
        kwargs["per_mode"] = per_mode
    if season_type is not None:
        kwargs["season_type"] = season_type

    leaders = alltimeleadersgrids.AllTimeLeadersGrids(**kwargs)
    return leaders.get_json()


def get_league_leaders(
    stat_category: str,
    season: str,
    per_mode48: Optional[str] = None,
    season_type_all_star: Optional[str] = None,
) -> str:
    """
    Fetches NBA league leaders for a specific statistical category.
    Returns the data in JSON format.
    """
    kwargs: dict[str, str] = {
        "season": season,
        "stat_category_abbreviation": stat_category,
    }
    if per_mode48 is not None:
        kwargs["per_mode48"] = per_mode48
    if season_type_all_star is not None:
        kwargs["season_type_all_star"] = season_type_all_star

    leaders = leagueleaders.LeagueLeaders(**kwargs)
    return leaders.get_json()


def get_player_recent_games(player_id: int, last_n_games: int) -> str:
    """
    Fetches a player's recent game performances.
    Returns the data in JSON format.
    """
    kwargs: dict[str, int] = {
        "player_id_nullable": player_id,
        "last_n_games_nullable": last_n_games,
    }
    game_logs = playergamelogs.PlayerGameLogs(**kwargs)
    return game_logs.get_json()


def get_team_roster(team_id: int, season: Optional[str] = None) -> str:
    """
    Fetches the current roster for an NBA team.
    Returns the data in JSON format.
    """
    kwargs: dict[str, int | str] = {
        "team_id": team_id,
    }
    if season is not None:
        kwargs["season"] = season
    roster = commonteamroster.CommonTeamRoster(**kwargs)
    return roster.get_json()
