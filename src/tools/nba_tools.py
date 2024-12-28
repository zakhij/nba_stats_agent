from typing import Optional, List, Dict, Any

from nba_api.stats.static import players
from nba_api.stats.endpoints import (
    playercareerstats,
    alltimeleadersgrids,
    leagueleaders,
    playergamelogs,
    commonteamroster,
    leaguestandingsv3,
    teamgamelogs,
    boxscoresummaryv2,
)


def generate_final_response(
    answer: str, confidence: str, data_sources: List[str]
) -> Dict[str, Any]:
    """Special tool that signals the end of the conversation and stores the final response."""
    final_response = {
        "answer": answer,
        "confidence": confidence,
        "data_sources": data_sources,
    }
    return final_response


def get_player_id(player_name: str) -> str:
    player = players.find_players_by_full_name(player_name)
    return str(player[0]["id"])


def get_player_stats(player_id: str) -> str:
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    return career.get_json()


def get_all_time_leaders(
    top_x: int,
    league_id: Optional[int] = None,
    per_mode_simple: Optional[str] = None,
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
    if per_mode_simple is not None:
        kwargs["per_mode_simple"] = per_mode_simple
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


def get_league_standings(
    league_id: str,
    season: str,
    season_type: str,
) -> str:
    """
    Gets current NBA standings including conference rankings and records.
    Returns the data in JSON format.
    """
    standings = leaguestandingsv3.LeagueStandingsV3(
        league_id=league_id,
        season=season,
        season_type=season_type,
    )
    return standings.get_json()


def get_team_game_logs(
    team_id: int,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    season_type: Optional[str] = None,
) -> str:
    """
    Fetches detailed game logs for a team including basic stats and rankings.
    Returns the data in JSON format.
    """
    kwargs: dict[str, int | str] = {
        "team_id_nullable": team_id,
    }
    if date_from is not None:
        kwargs["date_from_nullable"] = date_from
    if date_to is not None:
        kwargs["date_to_nullable"] = date_to
    if season_type is not None:
        kwargs["season_type_nullable"] = season_type

    logs = teamgamelogs.TeamGameLogs(**kwargs)
    return logs.get_json()


def get_box_score_summary(game_id: str) -> str:
    """
    Gets comprehensive game summary including line scores, team stats,
    officials, and game info.
    Returns the data in JSON format.
    """
    summary = boxscoresummaryv2.BoxScoreSummaryV2(game_id=game_id)
    return summary.get_json()
