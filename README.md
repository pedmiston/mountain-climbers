# Mountain Climbers

## Setup

    git clone https://github.com/pedmiston/mountain-climbers
    cd mountain-climbers
    virtualenv --python=python3 ~/.venvs/peaks
    source ~/.venvs/peaks/bin/activate
    pip install -r requirements.txt

## Run experiment

    inv simulate ?    # view experiments
    inv simulate all  # run all experiments
    inv simulate identical-teams
    inv simulate path/to/custom-experiment.yaml

## Analyze results

    inv report --open-after
