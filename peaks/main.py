from sys import stdout
import json
import pandas
import numpy

from .config import Experiment


SIM_VARS = 'team landscape strategy aggregate_fn p_feedback labor_hours starting_pos seed'.split()
DATA_COLS = SIM_VARS + 'time feedback pos fitness'.split()


def run_experiment(experiment_yaml, output=None):
    """Run an experiment, which is a collection of simulations."""
    exp = Experiment.from_yaml(experiment_yaml)
    output = open(output, 'w') if output else stdout
    for i, run in enumerate(exp.simulations(SIM_VARS)):
        results = simulate(*run)
        results.insert(0, 'sim_id', i)
        results.to_csv(output, index=False, header=(i==0))
    output.close()


def simulate(team, landscape, strategy, aggregate_fn, p_feedback, labor_hours, starting_pos, seed):
    """Run a single simulation: a mountain climbing excursion.

    WARNING! simulate is expected to have the same call signature as SIM_VARS.
    """
    rand = numpy.random.RandomState(seed)

    team.pos = list(starting_pos)
    team.set_seed(seed)
    fitness = landscape.evaluate(team.pos)

    results = []

    for calendar_hour in strategy(labor_hours, team):
        new_pos = team.new_pos(aggregate_fn)
        new_fitness = landscape.evaluate(new_pos)

        feedback_trial = rand.choice([1, 0], p=[p_feedback, 1-p_feedback])
        if not feedback_trial:
            team.pos = new_pos
            fitness = new_fitness
        else:
            # For feedback trials, only change position if
            # it improves fitness.
            if new_fitness > fitness:
                team.pos = new_pos
                fitness = new_fitness
            # else don't change team pos

        results.append(dict(
            team=str(team),
            landscape=str(landscape),
            strategy=strategy.__name__,
            aggregate_fn=aggregate_fn,
            p_feedback=p_feedback,
            labor_hours=labor_hours,
            starting_pos=starting_pos,
            seed=seed,
            time=calendar_hour,
            feedback=int(feedback_trial),
            pos=json.dumps(team.pos),
            fitness=float(fitness),
        ))

    return pandas.DataFrame.from_records(results, columns=DATA_COLS)
