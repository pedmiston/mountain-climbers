import sys
from invoke import task
import yaml
import peaks


@task
def simulate(ctx, experiment_yaml, output=None):
    peaks.run_experiment(experiment_yaml, output=output)


@task
def report(ctx, open_after=False):
    Rscript = "rmarkdown::render('report.Rmd')"
    ctx.run('Rscript -e "{}"'.format(Rscript))
    if open_after:
        ctx.run('open report.html')
