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
        omniscient = kwargs.pop('omniscient', False)
        players = [Player(omniscient=omniscient, **attributes)
                          for attributes in player_attributes]
        return cls(players, **kwargs)

    def new_pos(self, aggregate_fn='sum', landscape=None):
        """Generate a new position from current position and player deltas."""
        deltas = [player.delta(landscape, self.pos)
                  for player in self.active_players]
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

    def set_omniscience(self, omniscient=False):
        for player in self.players:
            player.omniscient = omniscient

    def __str__(self):
        return json.dumps(dict(
            name=self.name,
            players=[player.to_dict() for player in self.players]
        ))


class Player:
    def __init__(self, vision_x, vision_y, omniscient=False):
        self.vision_x = vision_x
        self.vision_y = vision_y
        self.sight_x = Player.vision_to_sight(vision_x)
        self.sight_y = Player.vision_to_sight(vision_y)
        self.omniscient = omniscient

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

    def delta(self, landscape=None, starting_pos=None):
        """Return a delta that this player can impact on a team's position.

        If this player is omniscient, then a landscape and a starting position
        need to be provided in order to sample the best delta within the players
        vision.
        """
        if self.omniscient:
            if landscape is None:
                raise OmniscientWithoutLandscape
            if starting_pos is None:
                raise OmniscientWithoutStartingPos
            return landscape.pick_best(starting_pos, self.vision_x, self.vision_y)

        return (self.pick_one(self.sight_x), self.pick_one(self.sight_y))

    def to_dict(self):
        return dict(vision_x=self.vision_x, vision_y=self.vision_y)

    def __str__(self):
        return json.dumps(self.to_dict())


class AggregateFunctionNotFound(Exception):
    """Probably due to a config error."""

class OmniscientWithoutLandscape(Exception):
    """Omniscient players need to know the landscape to be omnisicent."""

class OmniscientWithoutStartingPos(Exception):
    """Omniscient players need to know where they are to be omnisicent."""
