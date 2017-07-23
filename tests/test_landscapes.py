from itertools import product

import peaks


def test_pick_best_location():
    landscape = peaks.landscapes.SimpleHill(center = (10, 10))
    starting_pos = (0, 0)
    vision_x = 5
    vision_y = 5
    best_pos = landscape.pick_best(starting_pos, vision_x, vision_y)
    assert best_pos == (5, 5)


def test_creating_field_of_vision():
    starting_pos = (0, 0)
    vision_x = 1
    vision_y = 1
    visual_field = peaks.vision.calculate_field_of_vision(starting_pos,
                                                          vision_x, vision_y)
    possible_deltas = product([-1, 0, 1], [-1, 0, 1])
    possible_positions = [(starting_pos[0]+delta[0], starting_pos[1]+delta[1])
                          for delta in possible_deltas]

    assert len(visual_field) == len(possible_positions)
    assert set(visual_field) == set(possible_positions)
