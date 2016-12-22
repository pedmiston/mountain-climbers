
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


def alternating(labor_hours, team):
    """Have players take turns."""
    total_hours = labor_hours * len(team.players)
    for calendar_hour in range(total_hours):
        ix = calendar_hour % len(team.players)
        team.active_players = [team.players[ix]]
        yield calendar_hour


def solo(labor_hours, team):
    """Use the first player in the team."""
    team.active_players = [team.players[0]]  # using first player in team
    for calendar_hour in range(labor_hours * len(team.players)):
        yield calendar_hour
