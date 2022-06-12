from core.object import GameObject
from core.position import Position

class GameMap(GameObject):
    __id__: str

    def __init__(self, id: str):
        self.__id__ = id

    def left_blocked(self, position: Position):
        return False

    def right_blocked(self, position: Position):
        return False

    def above_blocked(self, position: Position):
        return False

    def bottom_blocked(self, position: Position):
        return position.y <= 0.5

    @property
    def id(self):
        return self.__id__
