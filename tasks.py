import sys

import yaml
from invoke import task
from unipath import Path

import peaks


@task(help=dict(experiment='yaml file by path or stem name with no extension'))
def run(ctx, experiment):
    """Run an experiment in "experiments/" or from a config file.

    Run an experiment by passing in a path to a config file. Experiments will
    be searched for in the experiments directory. To list available
    experiments, pass '?' (a question mark) as the first argument. Experiments
    in this directory can be run by the stem name of the file. To run all the
    available experiments, pass 'all'.  

        $ inv run path/to/my/exp-1.yaml  # run a single experiment
        $ inv run ?                      # list experiments in "experiments/"
        $ inv run exp-1                  # run "experiments/exp-1.yaml"
        $ inv run all                    # run all available experiments
    """
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


@task(help={'clear-cache': 'Clear knitr cache and figs before rendering.',
            'open-after': 'Open the report after creating it.',
            'skip-prereqs': 'Don\'t try to update custom prereqs.'})
def report(ctx, clear_cache=False, open_after=False, skip_prereqs=False):
    """Compile dynamic reports from the results of the experiments."""
    Rscript = "rmarkdown::render('report.Rmd')"

    if not skip_prereqs:
        ctx.run('Rscript -e "devtools::install_github(\'pedmiston/crotchet\')"')

    if clear_cache:
        ctx.run('rm -rf .cache/ figs/')

    ctx.run('Rscript -e "{}"'.format(Rscript))

    if open_after:
        ctx.run('open report.html')
