import sys
from glob import glob

import yaml
from invoke import task
from unipath import Path

import peaks


PROJ = Path(__file__).ancestor(2).absolute()
R_PKG = Path(PROJ, 'data')
BOTS = Path(PROJ, 'bots')
EXPERIMENTS = Path(BOTS, 'experiments')


@task(help=dict(experiment='yaml file by path or stem name with no extension'))
def run(ctx, experiment):
    """Run an experiment in "experiments/" or from a config file.

    Run an experiment by passing in a path to a config file. Experiments will
    be searched for in the experiments directory. To list available
    experiments, pass 'list' as the first argument. Experiments
    in this directory can be run by the stem name of the file. To run all the
    available experiments, pass 'all'.

        $ inv run path/to/my/exp-1.yaml  # run a single experiment
        $ inv run list                   # list experiments in "experiments/"
        $ inv run exp-1                  # run "experiments/exp-1.yaml"
        $ inv run all                    # run all available experiments
    """
    if experiment == 'list':
        print('Experiments:')
        for experiment in EXPERIMENTS.listdir('*.yaml'):
            print(' - ' + experiment.stem)
        return
    elif experiment == 'all':
        experiments = EXPERIMENTS.listdir('*.yaml')
    elif Path(experiment).exists():
        experiments = [Path(experiment)]
    else:
        experiment = Path(EXPERIMENTS, experiment + '.yaml')
        assert experiment.exists(), 'experiment %s not found' % experiment
        experiments = [experiment]

    for experiment in experiments:
        output = Path(R_PKG, 'data-raw', experiment.stem+'.csv')
        print('Running experiment { %s }' % experiment.stem)
        peaks.run_experiment(experiment, output=output)

