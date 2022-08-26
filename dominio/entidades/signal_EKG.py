from abc import ABCMeta, abstractmethod
from threading import Lock

class AbsEKGEntity(metaclass=ABCMeta):
    
    def __init__(self): #,datos):
        self._state: True # bool = None
        # self._datos = datos
        self.lock = Lock()
        with self.lock:
            self._channel_1 = []
            self._channel_2 = []
            self._channel_3 = []