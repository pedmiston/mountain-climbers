from invoke import task
import yaml
import peaks


@task
def simulate(ctx):
    teams = yaml.load(open('teams.yaml'))
    for team_name, player_attributes in teams.items():
        teams[team_name] = peaks.Team.from_player_attributes(*player_attributes)
    landscape = peaks.landscapes.SimpleHill()
    strategies = [peaks.strategies.synchronic, peaks.strategies.diachronic]
    peaks.run_experiment(landscape, teams, strategies,
                         labor_hours=50, n_seeds=100) 

@task
def report(ctx, open_after=False):
    Rscript = "rmarkdown::render('report.Rmd')"
    ctx.run('Rscript -e "{}"'.format(Rscript))
    if open_after:
        ctx.run('open report.html')
