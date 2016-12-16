from invoke import task
import yaml
import peaks


@task
def simulate(ctx):
    teams = yaml.load(open('teams.yaml'))
    for team_name, player_attributes in teams.items():
        teams[team_name] = peaks.Team.from_player_attributes(*player_attributes)
    landscape = peaks.landscapes.SimpleHill()
    print('team_name,condition,time,fitness')
    peaks.simulations.Synchronic(landscape, teams).run()
    peaks.simulations.Diachronic(landscape, teams).run()
