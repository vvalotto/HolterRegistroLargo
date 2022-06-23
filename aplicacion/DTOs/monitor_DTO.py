"""DTO MONITOREO"""
from abc import ABCMeta, abstractmethod
from threading import Lock
from aplicacion.DTOs.signal_DTO import AbsEKGDTO

class MonitorDTO(AbsEKGDTO):

    def __init__(self) -> None:
        self.type = 'monitor'
        self._state = True # Determina si está monitoreando o no. 
                        # Se usa en presentación y en gestor_operación,
                        #  pero no es información necesaria en dominio.
        self._link_type = ''
        self.lock = Lock()
        with self.lock:
            self._channel_1 = []
            self._channel_2 = []
            self._channel_3 = []

    @property
    def link_type(self):
        print ('dto',self._link_type)
        return self._link_type
    @link_type.setter
    def link_type(self, value):
        print ('valor ',value)
        self._link_type = value
    
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
