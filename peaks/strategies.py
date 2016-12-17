
def synchronic(labor_hours, team):
    """Activate all of the team's players."""
    team.active_players = team.players
    for calendar_hour in range(labor_hours):
        yield calendar_hour


def diachronic(labor_hours, team):
    """Activate one of the team's players at a time."""
    for i, player in enumerate(team.players):
        team.active_players = [player]
        # Calculate calendar hours based on current player index
        for calendar_hour in range(i*labor_hours, i*labor_hours+labor_hours):
            yield calendar_hour
