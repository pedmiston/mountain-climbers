from itertools import product
import yaml

from . import landscapes
from . import strategies
from .models import Team


class Experiment:
    """Object-oriented approach to config parsing."""
    def __init__(self, data=None):
        """Experiments are created from config data."""
        self._data = data or dict()

    @classmethod
    def from_yaml(cls, experiment_yaml):
        data = yaml.load(open(experiment_yaml))
        return cls(data)

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
        return [tuple(self._data['starting_pos'])]

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

    def simulations(self, ordered_properties):
        """Returns a simulation generator of the product of all properties."""
        props = [getattr(self, prop) for prop in ordered_properties]
        return product(*props)

    def get_as_list(self, key, default):
        data = self._data.get(key, default)
        if not isinstance(data, list):
            data = [data]
        return data
