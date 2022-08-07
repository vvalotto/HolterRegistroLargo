from abc import ABCMeta, abstractmethod
import dateutil.parser
from datetime import timedelta

class ComandoHolter(metaclass=ABCMeta):
    PACKAGE_LENGTH = 13

    @property
    def paquete(self):
        return self._datos

    def __init__(self):
        self._header = None
        self._type = None
        self._payload = None
        self._checksum = None
        self._datos = None

    @abstractmethod
    def armar_comando(self, payload=None):
        pass
    
    def _obtener_checksum(self, datos):
        checksum = 0
        for i in range(self.PACKAGE_LENGTH - 1):
            checksum ^= datos[i]
        return checksum

    def _armar_paquete(self):
        self._datos = self._header + \
                self._type + \
                self._payload

        self._checksum = self._obtener_checksum(self._datos).to_bytes(1, 'big')
        self._datos += self._checksum


class ComandEmpty(ComandoHolter):
    
    def armar_comando(self, payload=None):
        pass


class ComandoLecturaStatusEnvio(ComandoHolter):

    def armar_comando(self, payload=None):
        self._header = b'\xa5'
        self._type = b'\x60'
        self._payload = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        self._armar_paquete()
 

class ComandoLecturaConfiguracionEnvio(ComandoHolter):

    def armar_comando(self, payload=None):
        self._header = b'\xa5'
        self._type = b'\x61'
        self._payload = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        self._armar_paquete()


class ComandoEscrituraModoIdleEnvio(ComandoHolter):
    
    def armar_comando(self, payload=None):
        self._header = b'\xa5'
        self._type = b'\x81'
        self._payload = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        self._armar_paquete()


class ComandoEscrituraModoMonitoreoEnvio(ComandoHolter):
    
    def armar_comando(self, payload=None):
        self._header = b'\xa5'
        self._type = b'\x81'
        self._payload = b'\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00'
        self._armar_paquete()


class CommandWriteTime(ComandoHolter):
    
    def armar_comando(self, current_time):
        
        actual_time = current_time
        print (current_time, 'ARMAR COMANDO')
        self._header = b'\xa5'
        self._type = b'\x80'
        self._payload = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

        # actual_time = datetime.now()

        seconds = actual_time.second.to_bytes(1, 'big')
        minutes = actual_time.minute.to_bytes(1, 'big')
        hour = actual_time.hour.to_bytes(1, 'big')
        date = actual_time.date().isocalendar()[2].to_bytes(1, 'big')
        day = actual_time.day.to_bytes(1, 'big')
        month = actual_time.month.to_bytes(1, 'big')
        year = (actual_time.year-2000).to_bytes(1, 'big')
        empty = b'\x00'

        self._payload = seconds +\
                        minutes + \
                        hour + \
                        date + \
                        day + \
                        month + \
                        year + \
                        empty + \
                        empty +\
                        empty


        self._armar_paquete()


class CommandWriteConfig(ComandoHolter):
    
    STUDY_TIME = 7200  # minutes // QUE SEA ATRIBUTO DE LA ENTIDAD "ESTUDIO"

    def armar_comando(self, payload=None):
        # endtime = datetime.now() + timedelta(minutes = self.STUDY_TIME)
        self._header = b'\xa5'
        self._type = b'\x82'
        self._payload = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        if payload != None:
            # aux = datetime.strptime(payload[0], '%y-%m-%d %H:%M:%S')#2022-08-01 17:34:15.012371)
            payload[0] = dateutil.parser.parse(payload[0])
            print ('str to datetime', type(payload[0]))
            print (payload[0])
            endtime = payload[0] + timedelta(minutes = payload[1])
            self._payload[0] = payload[2]
            self._payload[1] = payload[3]
            self._payload[2] = payload[4]
            self._payload[3] = payload[5]
            self._payload[4] = endtime.minute
            self._payload[5] = endtime.hour
            self._payload[6] = endtime.day

        self._armar_paquete()


class CommandLoggingMode(ComandoHolter):
    
    def armar_comando(self, payload=None):
        self._header = b'\xa5'
        self._type = b'\x81'
        self._payload = b'\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00'
        self._armar_paquete()


class CommandDownloadMode(ComandoHolter):
    
    def armar_comando(self, payload=None):
        self._header = b'\xa5'
        self._type = b'\x81'
        self._payload = b'\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00'
        self._armar_paquete()


class CommandMemoryInformation(ComandoHolter):
    def armar_comando(self, payload = None):
        self._header = b'\xa5'
        self._type = b'\x62'
        self._payload = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        self._armar_paquete()


class CommandEraseMemory(ComandoHolter):

    def armar_comando(self, payload = None):
        self._header = b'\xa5'
        self._type = b'\x90'
        self._payload = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        self._armar_paquete()