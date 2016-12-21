import pytest
import peaks


@pytest.fixture
def team():
    players = [{'vision_x': 1, 'vision_y': 2},
               {'vision_x': 3, 'vision_y': 4}]
    return peaks.Team.from_player_attributes(*players)


def test_create_team_from_player_attributes(team):
    player_0_sight_x = team.players[0].sight_x
    assert len(player_0_sight_x) == 3, \
           "expecting %s to be [-1, 0, 1]" % player_0_sight_x


def test_strategy_modifies_team(team):
    team.active_players = []
    next(peaks.strategies.synchronic(1, team))
    assert len(team.active_players) == 2

    next(peaks.strategies.diachronic(1, team))
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


def test_default_agg_function():
    exp = peaks.Experiment()
    assert exp.aggregate_fn == ['sum']


def test_different_agg_functions(team):
    team.new_pos()
    team.new_pos('mean')
    team.new_pos('max')
    team.new_pos('prod')
