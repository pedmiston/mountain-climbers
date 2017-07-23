import numpy

from .vision import calculate_field_of_vision


class Landscape:
    def __init__(self, fitness_fn):
        self.fitness_fn = fitness_fn

    def evaluate(self, pos):
        return self.fitness_fn(pos)

    def pick_best(self, starting_pos, vision_x, vision_y):
        """Pick the highest point within a window."""
        # Create a window of positions around the starting positions
        field_of_vision = calculate_field_of_vision(starting_pos,
                                                    vision_x, vision_y)

        top_pos = starting_pos
        top_fitness = self.evaluate(starting_pos)

        for new_pos in field_of_vision:
            new_fitness = self.evaluate(new_pos)
            if new_fitness > top_fitness:
                top_pos = new_pos
                top_fitness = new_fitness

        return new_pos

class SimpleHill(Landscape):
    def __init__(self, center = (0, 0)):
        fitness_fn = lambda xy: -xy[0]**2 - xy[1]**2 + center[0] + center[1]
        return super().__init__(fitness_fn)

    def __str__(self):
        return 'SimpleHill'
