from functools import partial
import numpy
import json


class Team:
    def __init__(self, players, name='anonymous', seed=None):
        self.name = name
        self.players = players
        self.active_players = players
        self.pos = (0, 0)
        self.set_seed(seed)

    @classmethod
    def from_player_attributes(cls, *player_attributes, **kwargs):
        """Create players before adding them to a team."""
        players = [Player(**attributes) for attributes in player_attributes]
        return cls(players, **kwargs)

    def new_pos(self, aggregate_fn='sum'):
        """Generate a new position from current position and player deltas."""
        deltas = [player.delta() for player in self.active_players]
        try:
            agg_delta = getattr(numpy.array(deltas), aggregate_fn)(axis=0)
        except Exception as err:
            raise AggregateFunctionNotFound(err)
        new_pos = numpy.array([self.pos, agg_delta]).sum(axis=0)
        return new_pos.tolist()

    def set_seed(self, seed=None):
        rand = numpy.random.RandomState(seed)
        for player in self.players:
            player.set_seed(rand)

    def __str__(self):
        return json.dumps(dict(
            name=self.name,
            players=[player.to_dict() for player in self.players]
        ))


class Player:
    def __init__(self, vision_x, vision_y):
        self.vision_x = vision_x
        self.vision_y = vision_y
        self.sight_x = Player.vision_to_sight(vision_x)
        self.sight_y = Player.vision_to_sight(vision_y)

    @staticmethod
    def vision_to_sight(vision):
        """Create a range of available options, e.g., the player's sight.

        If a player has vision == 2, then their available
        sight is [-2, -1, 0, 1, 2].
        """
        return range(-vision, vision+1)

    def set_seed(self, seed=None):
        if seed and isinstance(seed, numpy.random.RandomState):
            rand = seed
        else:
            rand = numpy.random.RandomState(seed)
        self._pick_one = partial(rand.choice, size=1)

    def pick_one(self, values):
        return self._pick_one(values)[0]

    def delta(self):
        """Return a delta that this player can impact on a team's position."""
        return (self.pick_one(self.sight_x), self.pick_one(self.sight_y))

    def to_dict(self):
        return dict(vision_x=self.vision_x, vision_y=self.vision_y)

    def __str__(self):
        return json.dumps(self.to_dict())


class AggregateFunctionNotFound(Exception):
    """Probably due to a config error."""
