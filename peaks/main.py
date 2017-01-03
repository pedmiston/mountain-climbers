from sys import stdout
from collections import namedtuple
from itertools import product
import json
import math

import yaml
import numpy
import pandas

from . import landscapes
from . import strategies
from .models import Team
from .config import Simulation, Result


def run_experiment(experiment_yaml, output=None):
    """Run an experiment, which is a collection of simulations."""
    experiments = Experiment.from_yaml(experiment_yaml)
    output = open(output, 'w') if output else stdout
    for exp_id, experiment in enumerate(experiments):
        for sim_id, simulation in enumerate(experiment.simulations()):
            results = simulation.run()
            results.insert(0, 'sim_id', sim_id)
            results.insert(0, 'exp_id', exp_id)

            first_write = (exp_id == sim_id == 0)
            results.to_csv(output, index=False, header=first_write, mode='a')
    output.close()


class Experiment:
    """Object-oriented config parsing.

    An experiment is a friendly wrapper around a dict of experiment data.
    This data is easiest to obtain from a yaml file. Variables in the
    experiment are accessible as properties.

    **Experiment variables are not parsed until they are needed.**

    This makes it easy to test individual properties of experiments,
    but I'm sure it will bite me eventually.
    """
    def __init__(self, data=None):
        """Experiments are created from config data."""
        self._data = data or dict()

    @classmethod
    def from_yaml(cls, experiment_yaml):
        """Yields experiments contained in a yaml file."""
        defaults = dict()
        for config in yaml.load_all(open(experiment_yaml)):
            if 'type' in config:
                config_type = config.pop('type')
                if config_type == 'default':
                    defaults.update(config)
                    continue

            data = defaults.copy()
            data.update(config)
            yield cls(data)

    def simulations(self):
        """Returns simulations for the product of all properties."""
        props = [getattr(self, prop) for prop in Simulation._fields]
        for sim_vars in product(*props):
            config = Simulation(*sim_vars)
            yield Simulator(config)

    @property
    def landscape(self):
        """Return a list of landscape objects found in peaks.landscapes."""
        names = self.get_as_list('landscapes')
        return [getattr(landscapes, name)() for name in names]

    @property
    def strategy(self):
        """Return a list of strategy functions found in peaks.strategies."""
        names = self.get_as_list('strategies')
        return [getattr(strategies, name) for name in names]

    @property
    def labor_hours(self):
        """Return a list of labor hours alloted to each team."""
        return self.get_as_list('labor_hours')

    @property
    def starting_pos(self):
        """Return a list of tuples containing (x, y) starting positions.

        Examples of inputs:
            [100, 100]                            # single position
            [[100, 100], [-100, -100]]            # multiple positions
            {'radius': 10, 'size': 10}            # radius and n points
            {'radius': 10, 'degrees': 45}         # radius and degree (single)
            {'radius': 10, 'degrees': [45, 135]}  # radius and degrees
        """
        # get_as_list won't work since a single coord is a list
        starting_pos = self._data['starting_pos']
        if isinstance(starting_pos, dict):
            if 'degrees' in starting_pos:
                assert 'radius' in starting_pos
                rho = starting_pos.get('radius', 0)
                phis = starting_pos['degrees']
                if not isinstance(phis, list):
                    phis = [phis]
                starting_pos = [pol2cart(rho, to_radian(phi)) for phi in phis]
            else:
                # given a radius and number of points to sample
                starting_pos = sample_equidistant_positions(**starting_pos)
        elif len(starting_pos) == 2 and isinstance(starting_pos[0], int):
            # given a single coord
            starting_pos = [starting_pos]
        return starting_pos

    @property
    def seed(self):
        """Return a list of seeds to use when initializing the teams."""
        return range(self._data['n_seeds'])

    @property
    def team(self):
        """Return a list of Teams created from Player attributes."""
        teams = []
        for name, player_attributes in self._data['teams'].items():
            teams.append(Team.from_player_attributes(*player_attributes,
                                                     name=name))
        return teams

    @property
    def aggregate_fn(self):
        return self.get_as_list('aggregate_fn', 'sum')

    @property
    def p_feedback(self):
        return self.get_as_list('prob_feedback', 1.0)

    def get_as_list(self, key, default=None):
        data = self._data.get(key, default)
        if not isinstance(data, list):
            data = [data]
        return data


class Simulator:
    def __init__(self, sim):
        self._sim = sim
        self.data_cols = Simulation._fields + Result._fields

    def run(self):
        """Run a single simulation: a mountain climbing excursion."""
        s = self._sim
        rand = numpy.random.RandomState(s.seed)

        s.team.pos = list(s.starting_pos)
        s.team.set_seed(s.seed)
        fitness = s.landscape.evaluate(s.team.pos)

        results = []

        for calendar_hour in s.strategy(s.labor_hours, s.team):
            new_pos = s.team.new_pos(s.aggregate_fn)
            new_fitness = s.landscape.evaluate(new_pos)

            feedback_trial = rand.choice([1, 0], p=[s.p_feedback, 1-s.p_feedback])
            if not feedback_trial:
                s.team.pos = new_pos
                fitness = new_fitness
            else:
                # For feedback trials, only change position if
                # it improves fitness.
                if new_fitness > fitness:
                    s.team.pos = new_pos
                    fitness = new_fitness
                # else don't change team pos

            results.append(dict(
                team=str(s.team),
                landscape=str(s.landscape),
                strategy=s.strategy.__name__,
                aggregate_fn=s.aggregate_fn,
                p_feedback=s.p_feedback,
                labor_hours=s.labor_hours,
                starting_pos=s.starting_pos,
                seed=s.seed,
                time=calendar_hour,
                feedback=int(feedback_trial),
                pos=json.dumps(s.team.pos),
                fitness=float(fitness),
            ))

        return pandas.DataFrame.from_records(results, columns=self.data_cols)


def sample_equidistant_positions(radius, size, seed=None):
    rand = numpy.random.RandomState(seed)
    phis = rand.uniform(0, 2 * math.pi, size=size)
    return [pol2cart(radius, phi) for phi in phis]


def pol2cart(rho, phi):
    x = rho * numpy.cos(phi)
    y = rho * numpy.sin(phi)
    return (x, y)

def to_radian(degree):
    return degree*(math.pi/180)
