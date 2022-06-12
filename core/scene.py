from typing import List

from core.object import GameObject, GameObjectDict
from config.timer import LoopableThread, threadify

class Scene:
    __threads__: GameObjectDict
    __objects__: List[GameObject]

    def __init__(self):
        self.__objects__ = []
        self.__threads__ = GameObjectDict()

    def add(self, game_object: GameObject):
        self.__objects__.append(game_object)
        threads: List[LoopableThread] = []
        for behavior in game_object.behaviors:
            behavior.start()
            for starting_task in behavior.on_started:
                starting_task()
            def run_updating_task(main_task = behavior.update, sub_tasks = behavior.on_updated):
                main_task()
                for sub_task in sub_tasks:
                    sub_task()
            thread = threadify(run_updating_task)
            threads.append(thread)
            thread.setName(f'{game_object.name}-{behavior.id}')
            thread.start()
        def stop_threads(threads: List[LoopableThread] = threads):
            for thread in threads:
                thread.stop()
        game_object.on_disposed.append(stop_threads)
        self.__threads__.put(game_object, threads)

    def remove(self, game_object: GameObject):
        self.__objects__.remove(game_object)
        game_object.dispose()

    def stop(self):
        for game_object in self.__objects__:
            game_object.dispose()
        self.__objects__.clear()
