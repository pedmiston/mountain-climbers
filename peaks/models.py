import numpy

class Simulation:
    def __init__(self, landscape, team):
        self.landscape = landscape
        self.team = team

    def run(self):
        guess = self.team.generate_coords()
        fitness = self.landscape.evaluate(guess)
        for _ in xrange(100):
            guess = self.team.generate_coords()
            new_fitness = self.landscape.evaluate(guess)
            if new_fitness > fitness:
                self.team.update_pos(guess)
                fitness = new_fitness


class Team:
    def __init__(self, **members):
        self.members = members
        self.coords = (0, 0)

    @classmethod
    def from_config(cls, config):
        assert path(config).exists(), "config file %s not found" % config

        try:
            data = yaml.load(open(config))
        except Exception as e:
            raise AssertionError("config file not in proper yaml; %s" % e)

        return cls.from_members_data(**data)

    @classmethod
    def from_members_data(cls, **persons):
        for name, attributes in persons.items():
            persons[name] = Person(**attributes)
        return cls(**persons)

    def generate_coords(self):
        mean = lambda x: np.array(x).mean()
        x = mean([person.sample_x(self.coords[0]) for person in self.members])
        y = mean([person.sample_y(self.coords[1]) for person in self.members])

    def update_pos(self, coords):
        self.coords = coords


class Person:
    def __init__(self, vision_x, vision_y):
        self.vision_x = vision_x
        self.vision_y = vision_y
        self.rand = numpy.random.RandomState()

    def sample_x(self, start):
        return start + self.sample(self.vision_x)

    def sample_y(self, start):
        return start + self.sample(self.vision_y)

    def sample(self, values):
        return self.rand.sample(values)


class Landscape:
    def __init__(self, fitness_fn):
        self.fitness_fn = fitness_fn

    def evaluate(self, coords):
        return self.fitness_fn(coords)
