
class Landscape:
    def __init__(self, fitness_fn):
        self.fitness_fn = fitness_fn

    def evaluate(self, pos):
        return self.fitness_fn(pos)


class SimpleHill(Landscape):
    def __init__(self):
        fitness_fn = lambda xy: 100 - xy[0]**2 - xy[1]**2
        return super().__init__(fitness_fn)

    def __str__(self):
        return 'SimpleHill'

