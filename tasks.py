import sys

import yaml
from invoke import task
from unipath import Path

import peaks


@task
def simulate(ctx, experiment):
    if experiment == '?':
        print('Experiments:')
        for experiment in Path('experiments').listdir('*.yaml'):
            print(' - ' + experiment.stem)
        return
    elif experiment == '*':
        experiments = Path('experiments').listdir('*.yaml')
    elif Path(experiment).exists():
        experiments = [Path(experiment)]
    else:
        experiment = Path('experiments', experiment + '.yaml')
        assert experiment.exists(), 'experiment %s not found' % experiment
        experiments = [experiment]

    for experiment in experiments:
        output = Path('experiments', experiment.stem + '.csv')
        print('Running experiment %s' % experiment.stem)
        peaks.run_experiment(experiment, output=output)


@task
def report(ctx, open_after=False):
    Rscript = "rmarkdown::render('report.Rmd')"
    ctx.run('Rscript -e "{}"'.format(Rscript))
    if open_after:
        ctx.run('open report.html')
