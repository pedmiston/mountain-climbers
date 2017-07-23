from collections import namedtuple

Simulation = namedtuple('Simulation', """\
team
landscape
strategy
aggregate_fn
p_feedback
labor_hours
starting_pos
seed
omniscient
""".splitlines())

Result = namedtuple('Result', """\
time
feedback
pos
fitness
""".splitlines())
