import peaks


def test_default_config_vars():
    exp = peaks.Experiment()
    assert exp.aggregate_fn == ['sum']
    assert exp.p_feedback == [1.0]


def test_different_agg_functions(team):
    team.new_pos()
    team.new_pos('mean')
    team.new_pos('max')
    team.new_pos('prod')
