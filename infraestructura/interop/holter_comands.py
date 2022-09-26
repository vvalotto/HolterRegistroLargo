"""
Holter Commands
===============

    This module contains the methods to assemble the commands to be
    sent to the device to perform the desired task.
      Each command is constituted for a:
          - Header
          - Types
          - Pyload
          - Checksum

      The process is started with a call to some command object, values
      are assigned to the header, types and pyload attributes and checksum
      (with the 'obtain_checksum' method).
"""


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
    """
    This 'command' object generates the sequence that will be sent
    to request device status.

    Args:
        ComandoHolter (abstract class): Inheritance
    """

    def armar_comando(self, payload=None):
        self._header = b'\xa5'
        self._type = b'\x60'
        self._payload = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        self._armar_paquete()
 

class ComandoLecturaConfiguracionEnvio(ComandoHolter):
    """
    This 'command' object generates the sequence that will be sent
    to request device configuration.

    Args:
        ComandoHolter (abstract class): Inheritance
    """

    def armar_comando(self, payload=None):
        self._header = b'\xa5'
        self._type = b'\x61'
        self._payload = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        self._armar_paquete()


class ComandoEscrituraModoIdleEnvio(ComandoHolter):
    """
    This 'command' object generates the sequence that will be sent
    to set device 'IDLE' mode.

    Args:
        ComandoHolter (abstract class): Inheritance
    """
    def armar_comando(self, payload=None):
        self._header = b'\xa5'
        self._type = b'\x81'
        self._payload = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        self._armar_paquete()


class ComandoEscrituraModoMonitoreoEnvio(ComandoHolter):
    """
    This 'command' object generates the sequence that will be sent
    to set device 'MONITOR' mode.

    Args:
        ComandoHolter (abstract class): Inheritance
    """
    def armar_comando(self, payload=None):
        self._header = b'\xa5'
        self._type = b'\x81'
        self._payload = b'\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00'
        self._armar_paquete()


class CommandWriteTime(ComandoHolter):
    """
    This 'command' object generates the sequence that will be sent
    to set device date.

    Args:
        ComandoHolter (abstract class): Inheritance
    """
    def armar_comando(self, payload):
        
        current_time = payload        
        actual_time = current_time

        self._header = b'\xa5'
        self._type = b'\x80'
        self._payload = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        # cambiar formato de asignación
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
    """
    This 'command' object generates the sequence that will be sent
    to set device configuration.

    Args:
        ComandoHolter (abstract class): Inheritance
    """
    STUDY_TIME = 7200  # minutes // QUE SEA ATRIBUTO DE LA ENTIDAD "ESTUDIO"

    def armar_comando(self, payload=None):
        # endtime = datetime.now() + timedelta(minutes = self.STUDY_TIME)
        self._header = b'\xa5'
        self._type = b'\x82'
        self._payload = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        if payload != None:
            # aux = datetime.strptime(payload[0], '%y-%m-%d %H:%M:%S')#2022-08-01 17:34:15.012371)
            payload[0] = dateutil.parser.parse(payload[0])

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
    """
    This 'command' object generates the sequence that will be sent
    to set device 'LOGGING' mode.

    Args:
        ComandoHolter (abstract class): Inheritance
    """
    def armar_comando(self, payload=None):
        self._header = b'\xa5'
        self._type = b'\x81'
        self._payload = b'\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00'
        self._armar_paquete()


class CommandDownloadMode(ComandoHolter):
    """
    This 'command' object generates the sequence that will be sent
    to set device 'DOWNLOAD' mode.

    Args:
        ComandoHolter (abstract class): Inheritance
    """
    def armar_comando(self, payload=None):
        self._header = b'\xa5'
        self._type = b'\x81'
        self._payload = b'\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00'
        self._armar_paquete()


class CommandDownloadFile(ComandoHolter):
    """
    This 'command' object generates the sequence that will be sent
    to request a file download.

    Args:
        ComandoHolter (abstract class): Inheritance
    """
    def armar_comando(self, payload=None):
        file_number = payload

        self._header = b'\xa5'
        self._type = b'\x66'
        self._payload = bytearray (b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        
        self._payload[0] =  int(file_number / 256)
        self._payload[1] = (file_number - int(file_number / 256) * 256)
        print (self._payload, len(self._payload))
        self._armar_paquete()


class CommandMemoryInformation(ComandoHolter):
    """
    This 'command' object generates the sequence that will be sent
    to request a memory information.

    Args:
        ComandoHolter (abstract class): Inheritance
    """
    def armar_comando(self, payload = None):
        self._header = b'\xa5'
        self._type = b'\x62'
        self._payload = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        self._armar_paquete()


class CommandEraseMemory(ComandoHolter):
    """
    This 'command' object generates the sequence that will be sent
    to request the memory clear.

    Args:
        ComandoHolter (abstract class): Inheritance
    """

    def armar_comando(self, payload = None):
        self._header = b'\xa5'
        self._type = b'\x90'
        self._payload = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        self._armar_paquete()