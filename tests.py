import peaks


def test_create_default_team():
    team = peaks.create_team()  # should not raise

def test_create_team_from_config():
    players = {
        'sam': {'vision_x': 2, 'vision_y': 10},
        'bill': {'vision_x': 10, 'vision_y': 2},
    }
    team = peaks.Team.from_player_attributes(**players)
    assert len(team.players['sam'].options_x) == 5

