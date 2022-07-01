# from abc import ABCMeta, abstractmethod
# from datetime import datetime

class StudyEKG:

    def __init__(self) -> None:
        
        self._time_init = None # datetime
        self._time_stop = None # int o float
        self._channels: int = None
        self._events_type_byte_1 = None # int
        self._events_type_byte_2 = None # int
        self._interface = None # int
        self._events_amount = None # lista de int 

    @property
    def time_init(self):
        return self._time_init
    @time_init.setter
    def time_init(self, value):
        self._time_init = value

    @property
    def time_stop(self):
        return self._time_stop
    @time_stop.setter
    def time_stop(self, value):
        self._time_stop = value
        
    @property
    def channels(self):
        return self._channels
    @channels.setter
    def channels(self, value):
        self._channels = value

    @property
    def events_type_byte_1(self):
        return self._events_type_byte_1
    @events_type_byte_1.setter
    def events_type_byte_1(self, value):
        self._events_type_byte_1 = value

    @property
    def events_type_byte_2(self):
        return self._events_type_byte_2
    @events_type_byte_2.setter
    def events_type_byte_2(self, value):
        self._events_type_byte_2 = value
    
    @property
    def interface(self):
        return self._interface
    @interface.setter
    def interface(self, value):
        self._interface = value

    @property
    def events_amount(self):
        return self._events_amount
    @events_amount.setter
    def events_amount(self, value):
        self._events_amount = value