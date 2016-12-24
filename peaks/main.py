from sys import stdout
from collections import namedtuple

import yaml

from .config import Simulation, Result


def run_experiment(experiment_yaml, output=None):
    """Run an experiment, which is a collection of simulations."""
    experiment = Experiment.from_yaml(experiment_yaml)
    output = open(output, 'w') if output else stdout
    for i, simulation in enumerate(experiment.simulations()):
        results = simulation.run()
        results.to_csv(output, index=False, header=(i==0), method='a')
    output.close()


class Experiment:
    """Object-oriented config parsing."""
    def __init__(self, data=None):
        """Experiments are created from config data."""
        self._data = data or dict()

    @classmethod
    def from_yaml(cls, experiment_yaml):
        data = yaml.load(open(experiment_yaml))
        return cls(data)

    def simulations(self):
        """Returns simulations for the product of all properties."""
        props = [getattr(self, prop) for prop in self.ordered_properties]
        for sim_vars in product(*props):
            yield Simulation(sim_vars)

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
        """Return a list of tuples containing (x, y) starting positions."""
        # get_as_list won't work since a single coord is a list
        starting_pos = self._data['starting_pos']
        if len(starting_pos) == 2 and isinstance(starting_pos[0], int):
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
    def __init__(self, sim_vars):
        self.vars = sim_vars

    def run(self):
        """Run a single simulation: a mountain climbing excursion."""
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
