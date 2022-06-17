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


class RespuestaHolter(metaclass=ABCMeta):
    
    PACKAGE_LENGTH = 13
    ANSWER_OK = b'\xa5\x0A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xaf'

    @property
    def paquete(self):
        return self._datos

    def __init__(self):
        self._header = None
        self._type = None
        self._payload = None
        self._checksum = None
        self._datos = None
        # self._datos = [b'x00' for i in range(self.PACKAGE_LENGTH)] # inicializarlo en 0
        self._correct_answer = False

    @abstractmethod
    def desarmar_respuesta(self, datos):
        pass
    
    @property
    def authenticate_response (self):
        return self._correct_answer
        
    def _obtener_checksum(self, datos):
        checksum = 0
        for i in range(self.PACKAGE_LENGTH - 1):
            checksum ^= datos[i]
        return checksum

    def _desarmar_paquete(self, datos):

        if not (datos == None):
            checksum = self._obtener_checksum(datos).to_bytes(1, 'big')

            if (datos[-1].to_bytes(1, 'big') == checksum):
                self._header = datos[0]
                self._type = datos[1]
                self._payload = datos[2:12]
                self._checksum = checksum
                self._datos = datos
            else: print('Error de paquete. Checksum incorrecto.')
        else: print ('Error de datos recibidos. "datos == None". Paquete no desarmado.')


class RespuestaHolterStatus(RespuestaHolter):

    def desarmar_respuesta(self, datos):
        self._desarmar_paquete(datos)
        return self._payload

    def authenticate_response (self):
        pass

    def guardar_estado(self):
        return self._datos


class RespuestaHolterConfiguracion(RespuestaHolter):

    def desarmar_respuesta(self, datos):
        pass

    def authenticate_response (self):
        pass


class RespuestaHolterMemoria(RespuestaHolter):
    pass


class RespuestaHolterProduccion(RespuestaHolter):
    pass


class RespuestaHolterEGCMonitoreo(RespuestaHolter):

    def desarmar_respuesta(self, datos):
        channel_1 = []
        channel_2 = []
        channel_3 = []
        # print ('Datos GetECG',(len(datos)/self.PACKAGE_LENGTH))
        for i in range (0, int (len(datos)/self.PACKAGE_LENGTH)):
            self._desarmar_paquete(datos[i*self.PACKAGE_LENGTH:(i+1)*self.PACKAGE_LENGTH])
            channel_1.append(self._payload[:3])
            channel_2.append(self._payload[3:6])
            channel_3.append(self._payload[6:9])
        channels = [channel_1, channel_2, channel_3]
        return channels

    def authenticate_response (self):
        pass

class RespuestaHolterEvento(RespuestaHolter):
    pass


class RespuestaHolterEGC(RespuestaHolter):
    pass


class RespuestaHolterEscritiuraOK(RespuestaHolter):
    
    def desarmar_respuesta(self, datos):

        self._correct_answer = False

        for i in range (0, int (len(datos)/self.PACKAGE_LENGTH)):
            self._desarmar_paquete(datos[i*self.PACKAGE_LENGTH:(i+1)*self.PACKAGE_LENGTH])
            if self._datos == self.ANSWER_OK:
                self._correct_answer = True
                return self._payload

        return self._payload

    def authenticate_response (self):
        return self._correct_answer


class RespuestaHolterBorrado(RespuestaHolter):
    pass


class RespuestaHolterApagado(RespuestaHolter):

    def desarmar_respuesta(self, datos):
        pass

    def authenticate_response (self):
        pass
