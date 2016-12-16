import peaks


def test_create_team_from_player_attributes():
    players = [{'vision_x': 1, 'vision_y': 2},
               {'vision_x': 3, 'vision_y': 4}]
    team = peaks.Team.from_player_attributes(*players)
    player_0_sight_x = team.players[0].sight_x
    assert len(player_0_sight_x) == 3, \
           "expecting %s to be [-1, 0, 1]" % player_0_sight_x


def test_player_deltas_are_reproducibly_random():
    n_steps = 10
    player_attributes = dict(vision_x=10, vision_y=10, seed=1)
    player = peaks.Player(**player_attributes)
    orig_deltas = [player.delta() for _ in range(n_steps)]

    clone = peaks.Player(**player_attributes)
    clone_deltas = [clone.delta() for _ in range(n_steps)]
    assert orig_deltas == clone_deltas

    next_steps = [player.delta() for _ in range(n_steps)]
    assert next_steps != orig_deltas

