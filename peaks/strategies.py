
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


def solo(labor_hours, team):
    """Use the first player in the team."""
    team.active_players = [team.players[0]]  # using first player in team
    for calendar_hour in range(labor_hours * len(team.players)):
        yield calendar_hour


def diachronic_x(labor_hours, team, exchanges=1):
    total_hours = labor_hours * len(team.players)
    hours_per_session = int(total_hours/(exchanges + 1))
    exchange_hours = range(0, total_hours, hours_per_session)

    ix = 0  # start with first player in team
    for calendar_hour in range(total_hours):
        if calendar_hour in exchange_hours:
            next_player_ix = ix % len(team.players)
            team.active_players = [team.players[next_player_ix]]
            ix += 1
        yield calendar_hour


def diachronic_2(labor_hours, team):
    return diachronic_x(labor_hours, team, exchanges=2)


def diachronic_3(labor_hours, team):
    return diachronic_x(labor_hours, team, exchanges=3)


def diachronic_4(labor_hours, team):
    return diachronic_x(labor_hours, team, exchanges=4)


def diachronic_max(labor_hours, team):
    """Players take turns."""
    total_hours = labor_hours * len(team.players)
    for calendar_hour in range(total_hours):
        ix = calendar_hour % len(team.players)
        team.active_players = [team.players[ix]]
        yield calendar_hour
