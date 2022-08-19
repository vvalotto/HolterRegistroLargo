from abc import ABCMeta, abstractmethod
from threading import Lock
from aplicacion.DTOs.signal_DTO import AbsEKGDTO

class RegisterDTO(AbsEKGDTO):
    def __init__(self) -> None:
        
        self.type = 'register'
        self._state = False # Determina si esta registrando o no
        
        self._channel_1 = []
        self._channel_2 = []
        self._channel_3 = []

        self._register_data = []
    
    @property
    def register_data(self):
        return self._register_data
    @register_data.setter
    def register_data(self, value):
        self._register_data = value
    
    @property
    def state(self):
        return self._state
    @state.setter
    def state(self,value):
        self._state = value

    @property
    def channel_1(self):
        return self._channel_1

    @channel_1.setter
    def channel_1(self, valor):
        self._channel_1 = valor

    @property
    def channel_2(self):
        return self._channel_2

    @channel_2.setter
    def channel_2(self, valor):
        self._channel_2 = valor

    @property
    def channel_3(self):
        return self._channel_3

    @channel_3.setter
    def channel_3(self, valor):
        self._channel_3 = valor

