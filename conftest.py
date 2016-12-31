import pytest
import peaks


@pytest.fixture
def team():
    players = [{'vision_x': 1, 'vision_y': 2},
               {'vision_x': 3, 'vision_y': 4}]
    return peaks.Team.from_player_attributes(*players)
