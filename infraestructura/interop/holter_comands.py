from abc import ABCMeta, abstractmethod

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