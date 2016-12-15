from .models import *

def create_team(team_config=None):
    if team_config:
        team = Team.from_config(team_config)
    else:
        team = Team.from_members_data()
    return team


def create_landscape(landscape_config=None):
    pass
