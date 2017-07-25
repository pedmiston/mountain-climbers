from unipath import Path
import peaks

import pytest

tests_dir = Path(__file__).parent.absolute()
fixtures_dir = Path(tests_dir, 'fixtures')


def test_run_simulation():
    test_experiment = Path(fixtures_dir, 'single-experiment.yaml')
    experiments = peaks.Experiment.from_yaml(test_experiment)
    experiment = next(experiments)
    simulator = next(experiment.simulations())
    simulator._prepare_team()
    starting_pos = simulator._sim.team.pos
    assert ((starting_pos[0] == simulator._sim.starting_pos[0]) and
            (starting_pos[1] == simulator._sim.starting_pos[1]))
    simulator.run()
    assert ((starting_pos[0] != simulator._sim.starting_pos[0]) and
            (starting_pos[1] != simulator._sim.starting_pos[1]))
