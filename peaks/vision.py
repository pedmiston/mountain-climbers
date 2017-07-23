from itertools import product
from . import models

def calculate_field_of_vision(starting_pos, vision_x, vision_y):
    sight_x = models.Player.vision_to_sight(vision_x)
    sight_y = models.Player.vision_to_sight(vision_y)
    visual_field = [(starting_pos[0]+delta[0], starting_pos[1]+delta[1])
                    for delta in product(sight_x, sight_y)]
    return visual_field
