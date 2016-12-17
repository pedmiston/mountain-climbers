from . import landscapes
from . import strategies
from .models import Team, Player


def run_experiment(landscape, teams, strategies, labor_hours=100, n_seeds=10):
    """Run an experiment, which is a collection of simulations."""
    starting_pos = (-100, 100)
    print('team_name,strategy_name,seed,calendar_hour,pos_x,pos_y,fitness')
    for strategy in strategies:
        for name, team in teams.items():
            for seed in range(n_seeds):
                simulate(landscape, team, strategy, labor_hours, starting_pos,
                         seed, team_name=name)


def simulate(landscape, team, strategy, labor_hours, starting_pos, seed,
             team_name=None):
    """Run a single simulation: a mountain climbing excursion.

    Args:
        landscape (peaks.landscapes.Landscape): The landscape containing the
            mountain to climb.
        team (peaks.models.Team): The team attempting the climb.
        strategy (func): Method for using labor hours.
        labor_hours (int): Number of labor hours allowed per player.
        starting_pos (tuple): x, y coordinates for team starting position.
        seed (int): Random seed for reproducible climbs.
        team_name (str): Label for the team.
    """
    team.pos = starting_pos
    team.set_seed(seed)
    fitness = landscape.evaluate(team.pos)

    for calendar_hour in strategy(labor_hours, team):
        new_pos = team.new_pos()
        new_fitness = landscape.evaluate(new_pos)
        if new_fitness > fitness:
            team.pos = new_pos
            fitness = new_fitness
        print(('{team_name},{strategy_name},{seed},'
               '{calendar_hour},{pos_x},{pos_y},{fitness}')
               .format(team_name=team_name, strategy_name=strategy.__name__,
                       seed=seed, calendar_hour=calendar_hour,
                       pos_x=team.pos[0], pos_y=team.pos[1],
                       fitness=fitness))
