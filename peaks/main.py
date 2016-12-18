from sys import stdout
from itertools import product
from collections import namedtuple
import yaml
import json
import pandas

from . import landscapes
from . import strategies
from .models import Team


SIM_VARS = 'team landscape strategy labor_hours starting_pos seed'.split()
DATA_COLS = SIM_VARS + 'time pos fitness'.split()


def run_experiment(experiment_yaml, output=None):
    """Run an experiment, which is a collection of simulations."""
    exp = Experiment.from_yaml(experiment_yaml)
    if output is None:
        output = stdout

    header = True
    mode = 'w'
    for i, run in enumerate(exp.simulations()):
        results = simulate(*run)
        results.to_csv(output, index=False, header=header, mode=mode)

        header = False
        mode = 'a'


def simulate(team, landscape, strategy, labor_hours, starting_pos, seed):
    """Run a single simulation: a mountain climbing excursion."""
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

    frame = pandas.DataFrame.from_records(results, columns=DATA_COLS)
    return frame


class Experiment:
    def __init__(self, data):
        self._data = data

    @classmethod
    def from_yaml(cls, experiment_yaml):
        data = yaml.load(open(experiment_yaml))
        return cls(data)

    def get_list(self, key):
        data = self._data[key]
        if not isinstance(data, list):
            data = [data]
        return data

    @property
    def landscapes(self):
        names = self.get_list('landscapes')
        return [getattr(landscapes, name)() for name in names]

    @property
    def strategies(self):
        names = self.get_list('strategies')
        return [getattr(strategies, name) for name in names]

    @property
    def labor_hours(self):
        return self.get_list('labor_hours')

    @property
    def starting_pos(self):
        return [tuple(self._data['starting_pos'])]

    @property
    def seeds(self):
        return range(self._data['n_seeds'])

    @property
    def teams(self):
        teams = []
        for name, player_attributes in self._data['teams'].items():
            teams.append(Team.from_player_attributes(*player_attributes))
        return teams

    def simulations(self):
        return product(
            self.teams,
            self.landscapes,
            self.strategies,
            self.labor_hours,
            self.starting_pos,
            self.seeds,
        )
