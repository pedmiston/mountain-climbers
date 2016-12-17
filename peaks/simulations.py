
def simulations(landscape, teams, strategies, labor_hours=100, n_seeds=100):
    for strategy in strategies:
        for name, team in teams:
            for seed in range(n_seeds):
                simulate(landscape, team, strategy, seed, labor_hours, n_seeds)


def simulate(landscape, team, strategy, seed,
             labor_hours, n_seeds, starting_pos):
    team.pos = starting_pos
    team.set_seed(seed)
    fitness = landscape.evaluate(team.pos)
    
    for calendar_hour in strategy.spend_labor_hours(labor_hours):
        new_pos = team.new_pos()
        new_fitness = landscape.evaluate(new_pos)
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
