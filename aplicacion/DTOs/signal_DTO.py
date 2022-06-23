from abc import ABCMeta, abstractmethod
from threading import Lock

class AbsEKGDTO(metaclass=ABCMeta):
    
    def __init__(self): #,datos):
        self._state = True # bool = None
        # self._datos = datos
        self.lock = Lock()
        with self.lock:
            self._channel_1 = []
            self._channel_2 = []
            self._channel_3 = []

    abstractmethod    
    def separar_datos_canal(self):
        pass
    
    abstractmethod
    def almacenar_datos(self):
        pass


class RegisterDTO(AbsEKGDTO):
    pass


class EventsDTO(AbsEKGDTO):
    pass


# class MonitorDTO(AbsEKGDTO):
#     # state = True
#     def separar_datos_canal(self):
#         self._channel_1 = self._datos [2:5]
#         self._channel_2 = self.datos [5:8]
#         self._channel_3 = self.datos [8:11]
    
#     @property
#     def state(self):
#         return self._state
#     @state.setter
#     def state(self,value):
#         self._state = value

class SignalEKG(AbsEKGDTO):
    
    def __init__(self, RegisterEKG: RegisterDTO, EventsEKG:EventsDTO):
        super().__init__()