from nba_api.stats.static import players
from nba_api.stats.endpoints import (
    playercareerstats,
    alltimeleadersgrids,
    leagueleaders,
    playergamelogs,
    commonteamroster,
)
import logging

_logger = logging.getLogger(__name__)


def get_player_id(player_name: str) -> str:
    player = players.find_players_by_full_name(player_name)
    return str(player[0]["id"])


def get_player_stats(player_id: str) -> str:
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    return career.get_json()


def mock_tweet(tweet_text: str) -> None:
    print(f"MOCK TWEET: {tweet_text}")


def get_all_time_leaders(
    league_id: str,
    per_mode: str,
    season_type: str,
    top_x: int,
) -> str:
    """
    Fetches NBA all-time statistical leaders across multiple categories.
    Returns the data in JSON format.
    """
    leaders = alltimeleadersgrids.AllTimeLeadersGrids(
        league_id=league_id,
        per_mode_simple=per_mode,
        season_type=season_type,
        topx=top_x,
    )
    return leaders.get_json()


def get_league_leaders(
    stat_category: str,
    season: str,
    per_mode: str,
    season_type_all_star: str,
) -> str:
    """
    Fetches NBA league leaders for a specific statistical category.
    Returns the data in JSON format.
    """
    leaders = leagueleaders.LeagueLeaders(
        season=season,
        per_mode48=per_mode,
        season_type_all_star=season_type_all_star,
        stat_category_abbreviation=stat_category,
    )
    return leaders.get_json()


def get_player_recent_games(player_id: str, last_n_games: int) -> str:
    """
    Fetches a player's recent game performances.
    Returns the data in JSON format.
    """
    game_logs = playergamelogs.PlayerGameLogs(
        player_id_nullable=player_id, last_n_games_nullable=last_n_games
    )
    return game_logs.get_json()


def get_team_roster(team_id: str, season: str) -> str:
    """
    Fetches the current roster for an NBA team.
    Returns the data in JSON format.
    """
    roster = commonteamroster.CommonTeamRoster(team_id=team_id, season=season)
    return roster.get_json()
