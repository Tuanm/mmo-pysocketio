from core.position import Position
from core.behavior import GameBehavior

from game.action import Action
from game.direction import Direction
from game.status import Status
from game.map import GameMap

from config.timer import DELTA_TIME
from config.physics import GRAVITY

class Movement(GameBehavior):

    speed: float
    move_step: float
    jump_speed: float
    jump_high: float
    map: GameMap
    position: Position
    action: Action
    status: Status
    direction: Direction

    def start(self):
        self.speed = 5
        self.move_step = 3
        self.jump_speed = 8
        self.jump_high = 10
        self.map = GameMap('1')
        self.position = Position.new()
        self.action = Action.STAND
        self.status = Status.STANDING
        self.direction = Direction.FACE_RIGHT

    def update(self):
        self.fall()
        if self.action == Action.MOVE_LEFT:
            self.move_left()
        elif self.action == Action.MOVE_RIGHT:
            self.move_right()
        elif self.action == Action.JUMP:
            self.jump()

    def move_left(self):
        if not self.map.left_blocked(self.position):
            self.position.x -= DELTA_TIME * self.speed * self.move_step
            self.status = Status.MOVING_LEFT

    def move_right(self):
        if not self.map.right_blocked(self.position):
            self.position.x += DELTA_TIME * self.speed * self.move_step
            self.status = Status.MOVING_RIGHT
    def jump(self):
        if not self.map.above_blocked(self.position):
            self.position.y += DELTA_TIME * self.jump_speed * self.jump_high
            self.status = Status.JUMPING
    def fall(self):
        if not self.map.bottom_blocked(self.position):
            self.position.y -= DELTA_TIME * GRAVITY
            self.status = Status.FALLING
