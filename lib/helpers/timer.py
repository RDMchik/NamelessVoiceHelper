from operator import le
import time


class Timer(object):
    """A timer."""

    def __init__(self, length: int) -> None:
        
        self.finish_time = time.time() + length

    def __update(self) -> bool:

        if self.finish_time <= time.time():
            return True

        return False

    def __call__(self) -> bool:
        return self.__update()