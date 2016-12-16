from .models import *

def create_team(team_config=None):
    if team_config:
        team = Team.from_yaml_config(team_config)
    else:
        # Create a default team
        team = Team.from_player_attributes(
            sam=dict(vision_x=2, vision_y=10),
            bill=dict(vision_x=10, vision_y=2),
        )
    return team


def create_landscape(landscape_config=None):
    pass
