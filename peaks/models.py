from os import path
from functools import partial
import yaml
import numpy


class Simulation:
    def __init__(self, landscape, team):
        self.landscape = landscape
        self.team = team

    def run(self):
        fitness = self.landscape.evaluate(self.team.pos)
        for _ in xrange(100):
            new_pos = self.team.new_pos()
            new_fitness = self.landscape.evaluate(new_pos)
            if new_fitness > fitness:
                self.team.pos = new_pos
                fitness = new_fitness


class Team:
    def __init__(self, **players):
        self.players = players
        self.pos = (0, 0)

    @classmethod
    def from_yaml_config(cls, config):
        assert path(config).exists(), "config file %s not found" % config
        players = yaml.load(open(config))
        return cls.from_player_attributes(**players)

    @classmethod
    def from_player_attributes(cls, **players):
        for name, attributes in players.items():
            players[name] = Player(**attributes)
        return cls(**players)

    def new_pos(self):
        deviations = [player.new_deviation() for player in self.players]
        mean_deviation = numpy.array(deviations).mean(axis=0)
        new_pos = numpy.array([self.pos, mean_deviation]).sum(axis=0)
        return new_pos


class Player:
    def __init__(self, vision_x, vision_y, seed=None):
        self.options_x = Player.vision_to_options(vision_x)
        self.options_y = Player.vision_to_options(vision_y)
        self.pick_one = partial(numpy.random.RandomState(seed).choice, size=1)

    @staticmethod
    def vision_to_options(vision):
        return range(-vision, vision+1)

    def new_pos(self):
        return (self.pick_one(self.options_x), self.pick_one(self.options_y))


class Landscape:
    def __init__(self, fitness_fn):
        self.fitness_fn = fitness_fn

    def evaluate(self, pos):
        return self.fitness_fn(pos)
