from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats


def get_player_id(player_name: str) -> str:
    player = players.find_players_by_full_name(player_name)
    return str(player[0]["id"])


def get_player_stats(player_id: str) -> str:
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    return career.get_json()


def mock_tweet(tweet_text: str) -> None:
    print(f"MOCK TWEET: {tweet_text}")
