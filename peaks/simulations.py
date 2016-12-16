
class Simulation:
    start_pos = (-100, -100)
    labor_hours = 100

    def __init__(self, landscape, teams):
        self.landscape = landscape
        self.teams = teams

    def run_team(self, name, condition, t0=0):
        team = self.teams[name]
        fitness = self.landscape.evaluate(team.pos)
        for t in range(t0, t0+self.labor_hours):
            new_pos = team.new_pos()
            new_fitness = self.landscape.evaluate(new_pos)
            if new_fitness > fitness:
                team.pos = new_pos
                fitness = new_fitness
            print('{},{},{},{}'.format(name, condition, t, fitness))


class Synchronic(Simulation):
    def run(self):
        for name in self.teams:
            # Run synchronic simulation by setting all players to active.
            team = self.teams[name]
            team.pos = self.start_pos
            team.active_players = team.players
            self.run_synchronic_team(name)

    def run_synchronic_team(self, name):
        self.run_team(name, 'synchronic')


class Diachronic(Simulation):
    def run(self):
        for name in self.teams:
            team = self.teams[name]
            team.pos = self.start_pos
            self.run_diachronic_team(name)

    def run_diachronic_team(self, name):
        team = self.teams[name]
        for order, player in enumerate(team.players):
            team.active_players = [player]
            self.run_team(name, 'diachronic', t0=order*self.labor_hours)
