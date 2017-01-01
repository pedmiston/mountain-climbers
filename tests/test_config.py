from unipath import Path
import peaks

tests_dir = Path(__file__).parent.absolute()
fixtures_dir = Path(tests_dir, 'fixtures')


def test_default_config_vars():
    exp = peaks.Experiment()
    assert exp.aggregate_fn == ['sum']
    assert exp.p_feedback == [1.0]

def test_different_agg_functions(team):
    team.new_pos()
    team.new_pos('mean')
    team.new_pos('max')
    team.new_pos('prod')

def test_multiple_experiments():
    multiple_experiments_yaml = Path(fixtures_dir, 'multiple-experiments.yaml')
    exp = peaks.Experiment.from_yaml(multiple_experiments_yaml)
    assert len(list(exp)) == 2

def test_specific_starting_positions():

    def make_exp(arg):
        return peaks.Experiment(data=dict(starting_pos=arg))

    single_pos_exp = make_exp([100, 100]).starting_pos
    assert len(single_pos_exp) == 1
    assert single_pos_exp[0] == [100, 100]

    multiple_pos_exp = make_exp([[100, 100], [200, 200]]).starting_pos
    assert len(multiple_pos_exp) == 2
    assert multiple_pos_exp[1] == [200, 200]
