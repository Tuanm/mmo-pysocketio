from typing import Generic, List, TypeVar
from core.behavior import GameBehavior

class GameObject:
    name: str
    behaviors: List[GameBehavior]

    def __init__(self):
        self.behaviors = []
        self.on_disposed = [GameObject.do_nothing]

    def attach(self, behavior: GameBehavior):
        if self.get(behavior.id) == None:
            self.behaviors.append(behavior.attach(self))

    def deattach(self, behavior_id: str):
        behavior = self.get(behavior_id)
        self.behaviors.remove(behavior)
        if behavior != None: behavior.destroy()

    def dispose(self):
        for task in self.on_disposed:
            task()

    def get(self, behavior_id: str):
        for behavior in self.behaviors:
            if behavior.id == behavior_id: return behavior
        return None

    @staticmethod
    def do_nothing():
        return

T = TypeVar('T')

class GameObjectDict(Generic[T]):

    class Entry:
        __key__: GameObject
        __value__: T

        def __init__(self, key: GameObject, value: T):
            self.__key__ = key
            self.__value__ = value

        @property
        def key(self):
            return self.__key__

        @property
        def value(self):
            return self.__value__

    __entries__: List[Entry]

    def __init__(self):
        super().__init__()
        self.__entries__ = []

    def put(self, key: GameObject, value: T):
        for entry in self.__entries__:
            if entry.key == key:
                entry.value = value
                return
        self.__entries__.append(GameObjectDict.Entry(key, value))

    def remove(self, key: GameObject):
        for entry in self.__entries__:
            if entry.key == key:
                self.__entries__.remove(entry)
                return True
        return False

    def get(self, key: GameObject):
        for entry in self.__entries__:
            if entry.key == key:
                return entry.value
        return None
