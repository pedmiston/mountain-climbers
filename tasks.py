from invoke import task
import yaml
import peaks


@task
def simulate(ctx):
    teams = yaml.load(open('teams.yaml'))
    for team_name, player_attributes in teams.items():
        teams[team_name] = peaks.Team.from_player_attributes(*player_attributes)
    landscape = peaks.landscapes.SimpleHill()
    print('team_name,condition,time,fitness')  # csv header
    peaks.Simulation(landscape, teams, strategies).run()

@task
def report(ctx):
    Rscript = "rmarkdown::render('report.Rmd')"
    ctx.run('Rscript -e "{}"'.format(Rscript))
