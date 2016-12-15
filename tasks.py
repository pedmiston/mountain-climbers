from invoke import task
import peaks


@task
def simulate(ctx, team_config=None, landscape_config=None):
    team = peaks.create_team(team_config)
    landscape = peaks.create_landscape(landscape_config)
    sim = peaks.Simulation(landscape, team)
    sim.run()
