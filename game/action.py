from enum import Enum

class Action(Enum):
    MOVE_LEFT = 'move_left'
    MOVE_RIGHT = 'move_right'
    JUMP = 'jump'
    STAND = 'stand'