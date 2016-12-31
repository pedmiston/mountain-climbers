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
    elif experiment == 'all':
        experiments = Path('experiments').listdir('*.yaml')
    elif Path(experiment).exists():
        experiments = [Path(experiment)]
    else:
        experiment = Path('experiments', experiment + '.yaml')
        assert experiment.exists(), 'experiment %s not found' % experiment
        experiments = [experiment]

    for experiment in experiments:
        output = Path('experiments', experiment.stem + '.csv')
        print('Running experiment { %s }' % experiment.stem)
        peaks.run_experiment(experiment, output=output)


@task
def report(ctx, clear_cache=False, open_after=False, skip_prereqs=False):
    Rscript = "rmarkdown::render('report.Rmd')"

    if not skip_prereqs:
        ctx.run('Rscript -e "devtools::install_github(\'pedmiston/crotchet\')"')

    if clear_cache:
        ctx.run('rm -rf .cache/ figs/')

    ctx.run('Rscript -e "{}"'.format(Rscript))

    if open_after:
        ctx.run('open report.html')
