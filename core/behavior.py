class GameBehavior:
    __id__: str
    __object__: any

    def __init__(self, id: str):
        self.__id__ = id
        self.on_started = [GameBehavior.do_nothing]
        self.on_updated = [GameBehavior.do_nothing]
        self.on_destroyed = [GameBehavior.do_nothing]
        self.scheduler = None

    def start(self):
        pass

    def update(self):
        pass

    def destroy(self):
        pass

    def attach(self, obj: any):
        self.__object__ = obj
        return self

    @property
    def id(self):
        return self.__id__

    @property
    def game_object(self):
        return self.__object__

    @staticmethod
    def do_nothing():
        return