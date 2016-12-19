# Mountain Climbers

## Setup

    git clone https://github.com/pedmiston/mountain-climbers
    cd mountain-climbers
    virtualenv --python=python3 ~/.venvs/peaks
    source ~/.venvs/peaks/bin/activate
    pip install -r requirements.txt

## Run experiment

    inv simulate experiment-1.yaml -o experiment-1.csv

## Analyze results

    inv report --open-after
