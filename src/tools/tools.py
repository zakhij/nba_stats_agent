from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats, alltimeleadersgrids


def get_player_id(player_name: str) -> str:
    player = players.find_players_by_full_name(player_name)
    return str(player[0]["id"])


def get_player_stats(player_id: str) -> str:
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    return career.get_json()


def mock_tweet(tweet_text: str) -> None:
    print(f"MOCK TWEET: {tweet_text}")


def get_all_time_leaders(
    league_id: str = "00",
    per_mode: str = "Totals",
    season_type: str = "Regular Season",
    top_x: int = 10,
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
