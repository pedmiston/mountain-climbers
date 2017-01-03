"""Strategies are ways of allotting labor hours.

Strategies are functions with the following signature:

    def strategy(labor_hours, team):
        # ...
        yield calendar_hour

Args:
    labor_hours: Total number of labor hours available.
    team (peaks.models.Team): The team using the strategy.

Teams are *modified* by the strategy. The first thing a strategy
must do is modify the team by setting the active players to
use.
"""


def synchronic(labor_hours, team):
    """Activate all of the team's players.

    Spends labor hours in the fastest way possible.
    """
    team.active_players = team.players
    calendar_hours = int(labor_hours/len(team.players))
    for calendar_hour in range(calendar_hours):
        yield calendar_hour


def diachronic(labor_hours, team):
    """Activate one of the team's players at a time.

    Spend calendar hours in the slowest way possible.
    """
    hours_per_player = int(labor_hours/len(team.players))
    ix = 0  # start with first player in the team
    for calendar_hour in range(labor_hours):
        if calendar_hour % hours_per_player == 0:
            team.active_players = [team.players[ix]]
            ix = (ix + 1) % len(team.players)
        yield calendar_hour


def solo(labor_hours, team):
    """Use the first player in the team.

    TODO: Remove the solo strategy and replace it with multiple
          experiments in the same yaml file.
    """
    team.active_players = [team.players[0]]  # using first player in team
    for calendar_hour in range(labor_hours):
        yield calendar_hour


def diachronic_x(labor_hours, team, exchanges=1):
    """Diachronic strategy with modified exchange rate."""
    hours_per_session = int(labor_hours/(exchanges + 1))
    exchange_hours = range(0, labor_hours, hours_per_session)

    ix = 0  # start with first player in the team
    for calendar_hour in range(labor_hours):
        if calendar_hour in exchange_hours:
            team.active_players = [team.players[ix]]
            ix = (ix + 1) % len(team.players)
        yield calendar_hour


def diachronic_2(labor_hours, team):
    return diachronic_x(labor_hours, team, exchanges=2)


def diachronic_3(labor_hours, team):
    return diachronic_x(labor_hours, team, exchanges=3)


def diachronic_4(labor_hours, team):
    return diachronic_x(labor_hours, team, exchanges=4)


def diachronic_max(labor_hours, team):
    """Players take turns."""
    for calendar_hour in range(labor_hours):
        ix = calendar_hour % len(team.players)
        team.active_players = [team.players[ix]]
        yield calendar_hour
