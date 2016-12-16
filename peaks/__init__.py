from os import path
from functools import partial
import yaml
import numpy

from . import landscapes


class Simulation:
    start_pos = (-100, -100)

    def __init__(self, landscape, teams):
        self.landscape = landscape
        for team in teams.values():
            team.pos = self.start_pos
        self.teams = teams

    def run(self):
        print('team_name,time,fitness')
        for name in self.teams:
            self.run_team(name)

    def run_team(self, name):
        team = self.teams[name]
        fitness = self.landscape.evaluate(team.pos)
        for t in range(100):
            new_pos = team.new_pos()
            new_fitness = self.landscape.evaluate(new_pos)
            if new_fitness > fitness:
                team.pos = new_pos
                fitness = new_fitness
            print('{},{},{}'.format(name, t, fitness))


class Team:
    def __init__(self, players):
        self.players = players
        self.pos = (0, 0)

    @classmethod
    def from_player_attributes(cls, *player_attributes):
        """Create players before adding them to a team."""
        players = [Player(**attributes) for attributes in player_attributes]
        return cls(players)

    def new_pos(self):
        """Generate a new position from current position and player deltas."""
        deltas = [player.delta() for player in self.players]
        mean_delta = numpy.array(deltas).mean(axis=0)
        new_pos = numpy.array([self.pos, mean_delta]).sum(axis=0)
        return new_pos


class Player:
    def __init__(self, vision_x, vision_y, seed=None):
        self.sight_x = Player.vision_to_sight(vision_x)
        self.sight_y = Player.vision_to_sight(vision_y)
        self._pick_one = partial(numpy.random.RandomState(seed).choice, size=1)

    @staticmethod
    def vision_to_sight(vision):
        """Create a range of available options, e.g., the player's sight.

        If a player has vision == 2, then their available
        sight is [-2, -1, 0, 1, 2].
        """
        return range(-vision, vision+1)

    def pick_one(self, values):
        return self._pick_one(values)[0]

    def delta(self):
        """Return a delta that this player can impact on a team's position."""
        return (self.pick_one(self.sight_x), self.pick_one(self.sight_y))
