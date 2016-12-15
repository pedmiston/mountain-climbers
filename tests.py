import peaks


def test_create_default_team():
    team = peaks.create_team()  # should not raise


def test_create_team_from_config():
    config = {
        'person_1': {'vision_x': 2, 'vision_y': 10},
        'person_2': {'vision_x': 10, 'vision_y': 2},
    }
    team = peaks.Team.from_members_data(**config)
    assert team.members['person_1'].vision_x == 2
