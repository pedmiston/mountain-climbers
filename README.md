# Mountain climbers

## Reproducing

The first step is to clone the repo.

    # bash
    git clone https://github.com/pedmiston/mountain-climbers
    cd mountain-climbers

The simulations are run in python3. Install the required
packages in an isolated virtualenv.

    # bash
    virtualenv --python=python3 ~/.venvs/peaks
    source ~/.venvs/peaks/bin/activate
    pip install -r requirements.txt

Analyzing the results in R requires the tidyverse and a few
custom packages that can be installed from github with devtools.

    # R
    install.packages("tidyverse")  # Hadleyverse
    install.packages("magrittr")   # extra pipe functions
    library(devtools)
    install_github("pedmiston/crotchet")
    install_github("pedmiston/diachronic-teams", subdir = "evoteams")

## Run experiment

    # bash
    inv simulate ?    # view experiments
    inv simulate all  # run all experiments
    inv simulate identical-teams
    inv simulate path/to/custom-experiment.yaml

## Analyze results

    # bash
    inv report --open-after
