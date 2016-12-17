from functools import partial
import numpy


class Team:
    def __init__(self, players):
        self.players = players
        self.active_players = players
        self.pos = (0, 0)

    @classmethod
    def from_player_attributes(cls, *player_attributes):
        """Create players before adding them to a team."""
        players = [Player(**attributes) for attributes in player_attributes]
        return cls(players)

    def new_pos(self):
        """Generate a new position from current position and player deltas."""
        deltas = [player.delta() for player in self.active_players]
        mean_delta = numpy.array(deltas).mean(axis=0)
        new_pos = numpy.array([self.pos, mean_delta]).sum(axis=0)
        return new_pos

    def set_seed(self, seed):
        rand = numpy.random.RandomState(seed)
        player_seeds = rand.randint(100, size=len(self.players)).tolist()
        for ix, s in enumerate(player_seeds):
            self.players[ix].set_seed(s)


class Player:
    def __init__(self, vision_x, vision_y):
        self.sight_x = Player.vision_to_sight(vision_x)
        self.sight_y = Player.vision_to_sight(vision_y)
        self.set_seed()

    @staticmethod
    def vision_to_sight(vision):
        """Create a range of available options, e.g., the player's sight.

        If a player has vision == 2, then their available
        sight is [-2, -1, 0, 1, 2].
        """
        return range(-vision, vision+1)

    def set_seed(self, seed=None):
        self._pick_one = partial(numpy.random.RandomState(seed).choice, size=1)

    def pick_one(self, values):
        return self._pick_one(values)[0]

    def delta(self):
        """Return a delta that this player can impact on a team's position."""
        return (self.pick_one(self.sight_x), self.pick_one(self.sight_y))
