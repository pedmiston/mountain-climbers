import peaks


def test_create_team_from_player_attributes(team):
    assert len(team.players) == 2

def test_player_sight(team):
    assert team.players[0].sight_x == range(-1, 2)

def test_strategy_modifies_team(team):
    team.active_players = []
    next(peaks.strategies.synchronic(2, team))
    assert len(team.active_players) == 2

    next(peaks.strategies.diachronic(2, team))
    assert len(team.active_players) == 1

def test_player_deltas_are_reproducibly_random():
    n_steps = 10
    player_attributes = dict(vision_x=10, vision_y=10)
    player = peaks.Player(**player_attributes)
    player.set_seed(1)
    orig_deltas = [player.delta() for _ in range(n_steps)]

    clone = peaks.Player(**player_attributes)
    clone.set_seed(1)
    clone_deltas = [clone.delta() for _ in range(n_steps)]
    assert orig_deltas == clone_deltas

    next_steps = [player.delta() for _ in range(n_steps)]
    assert next_steps != orig_deltas

def test_team_deltas_are_reproducibly_random():
    n_steps = 10
    players = [{'vision_x': 1, 'vision_y': 2},
               {'vision_x': 3, 'vision_y': 4}]
    team = peaks.Team.from_player_attributes(*players)
    team.active_players = team.players
    team.set_seed(1)
    orig_deltas = [team.new_pos() for _ in range(n_steps)]

    clone = peaks.Team.from_player_attributes(*players)
    clone.active_players = clone.players
    clone.set_seed(1)
    clone_deltas = [clone.new_pos() for _ in range(n_steps)]

    assert orig_deltas == clone_deltas

    next_steps = [team.new_pos() for _ in range(n_steps)]
    assert next_steps != orig_deltas
