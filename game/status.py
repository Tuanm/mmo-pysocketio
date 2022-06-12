from enum import Enum

class Status(str, Enum):
    FALLING = 'falling'
    MOVING_LEFT = 'moving_left'
    MOVING_RIGHT = 'moving_right'
    JUMPING = 'jumping'
    STANDING = 'standing'