import time
from threading import Thread, Event

DELTA_TIME = 200

def threadify(task):
    return LoopableThread(target=task)

class TimeoutThread(Thread):
    def __init__(self, target = None, timeout = 0):
        super().__init__(target=target)
        self.timeout = timeout
        self._stop = Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        if self.stopped():
            return
        if self._target != None:
            time.sleep(self.timeout / 1000)
            self._target()

class LoopableThread(Thread):
    def __init__(self, target = None):
        super().__init__(target=target)
        self._stop = Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        while True:
            if self.stopped():
                return
            if self._target != None:
                self._target()
                time.sleep(DELTA_TIME / 1000)