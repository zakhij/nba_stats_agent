def add_two_integers(integer1: int, integer2: int) -> str:
    return f"{integer1 + integer2}"


from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats


def get_scoreboard() -> str:
    # Today's Score Board
    games = scoreboard.ScoreBoard()

    return games.get_json()


def get_player_id(player_name: str) -> str:
    player = players.find_players_by_full_name(player_name)
    return str(player[0]["id"])


def get_player_stats(player_id: str) -> str:
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    return career.get_json()
