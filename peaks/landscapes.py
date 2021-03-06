import numpy
from functools import lru_cache

from .vision import calculate_field_of_vision


class Landscape:
    def __init__(self, fitness_fn):
        self.fitness_fn = fitness_fn

    @lru_cache(maxsize=1000)
    def evaluate(self, x, y):
        return self.fitness_fn(x, y)

    def pick_best_delta(self, starting_pos, vision_x, vision_y):
        """Pick the delta that gets to the highest point in the window."""
        # Create a list of all positions around the starting position
        field_of_vision = calculate_field_of_vision(starting_pos,
                                                    vision_x, vision_y)

        top_pos = starting_pos
        top_fitness = self.evaluate(*starting_pos)

        for new_pos in field_of_vision:
            new_fitness = self.evaluate(*new_pos)
            if new_fitness > top_fitness:
                top_pos = new_pos
                top_fitness = new_fitness

        delta = new_pos[0] - starting_pos[0], new_pos[1] - starting_pos[1]
        assert abs(delta[0]) <= vision_x and abs(delta[1]) <= vision_y
        return delta


class SimpleHill(Landscape):
    def __init__(self, center = (0, 0)):
        fitness_fn = lambda x, y: -x**2 - y**2 + center[0] + center[1]
        return super().__init__(fitness_fn)

    def __str__(self):
        return 'SimpleHill'
