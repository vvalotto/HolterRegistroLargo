"""DTO MONITOREO"""
class MonitoreoDTO:

    def __init__(self) -> None:
        self.__channel_1 = []
        self.__channel_2 = []
        self.__channel_3 = []

        self._link_type = ''

    @property
    def link_type(self):
        print ('dto',self._link_type)
        return self._link_type
    @link_type.setter
    def link_type(self, value):
        print ('valor ',value)
        self._link_type = value

    @property
    def channel_1(self):
        return self.__channel_1

    @channel_1.setter
    def channel_1(self, valor):
        self.__channel_1 = valor

    @property
    def channel_2(self):
        return self.__channel_2

    @channel_2.setter
    def channel_2(self, valor):
        self.__channel_2 = valor

    @property
    def channel_3(self):
        return self.__channel_3

    @channel_3.setter
    def channel_3(self, valor):
        self.__channel_3 = valor
