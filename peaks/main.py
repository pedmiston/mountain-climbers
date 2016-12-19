from sys import stdout
import pandas

from .config import Experiment


SIM_VARS = 'team landscape strategy labor_hours starting_pos seed'.split()
DATA_COLS = SIM_VARS + 'time pos fitness'.split()


def run_experiment(experiment_yaml, output=None):
    """Run an experiment, which is a collection of simulations."""
    exp = Experiment.from_yaml(experiment_yaml)
    output = open(output, 'w') if output else stdout
    for i, run in enumerate(exp.simulations(SIM_VARS)):
        results = simulate(*run)
        results.to_csv(output, index=False, header=(i==0))
    output.close()


def simulate(team, landscape, strategy, labor_hours, starting_pos, seed):
    """Run a single simulation: a mountain climbing excursion.

    WARNING! simulate is expected to have the same call signature as SIM_VARS.
    """
    team.pos = starting_pos
    team.set_seed(seed)
    fitness = landscape.evaluate(team.pos)

    results = []

    for calendar_hour in strategy(labor_hours, team):
        new_pos = team.new_pos()
        new_fitness = landscape.evaluate(new_pos)
        if new_fitness > fitness:
            team.pos = new_pos
            fitness = new_fitness

        results.append(dict(
            team=str(team),
            landscape=str(landscape),
            strategy=strategy.__name__,
            labor_hours=labor_hours,
            starting_pos=starting_pos,
            seed=seed,
            time=calendar_hour,
            pos=team.pos,
            fitness=fitness,
        ))

    return pandas.DataFrame.from_records(results, columns=DATA_COLS)
