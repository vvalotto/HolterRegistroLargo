"""
COMMANDS
========

    In this module is implemented the Pattern Command. In this pattern, are extracted all 
"""

from abc import ABCMeta, abstractmethod
from infraestructura.interop.holter_comands import *
from infraestructura.interop.holter_responses import *
from infraestructura.interop.enlace import *
import time


class AbsComando(metaclass=ABCMeta):

    def __init__(self, destinatario, comando, respuesta):
        self._destinatario = destinatario
        self._comando = comando
        self._respuesta = respuesta

    @abstractmethod
    def ejecutar(self, payload_data = None):
        pass

    def is_expected_response(self,response):
        try:
            if response[0] == False:
                return False
            else: 
                return True
        except:
            return False


class LectorStatusHolter(AbsComando):

    def ejecutar(self, payload_data = None):
        # Lee estatus del holter
        self._comando.armar_comando()
        self._destinatario.conectar()
        self._destinatario.enviar(self._comando.paquete)
        paquete_recibido = self._destinatario.recibir(1)
        if not self.is_expected_response(paquete_recibido):
            self._destinatario.desenlazar()
            return
        self._respuesta.desarmar_respuesta(paquete_recibido)
        # # # self._destinatario.desenlazar()
        return    


class LectorConfiguracionHolter(AbsComando):
    
    def ejecutar(self, payload_data = None):
        # lee Configuracion del holter
        self._comando.armar_comando()
        self._destinatario.conectar()
        self._destinatario.enviar(self._comando.paquete)
        configuracion = self._destinatario.recibir(1)
        if configuracion == [False]:
            self._destinatario.desenlazar()
            time.sleep(3)
            return

        return self._respuesta.desarmar_respuesta(configuracion)


class SetHolterTime(AbsComando):
    
    def ejecutar(self, current_time):
        self._comando.armar_comando(current_time) # payload_data = hora actual 
        self._destinatario.conectar()
        self._destinatario.enviar(self._comando.paquete)
        configuracion = self._destinatario.recibir(10)
        self._respuesta.desarmar_respuesta(configuracion)
        while (not self._respuesta.authenticate_response()):
            configuracion = self._destinatario.recibir(10)
            self._respuesta.desarmar_respuesta(configuracion)
            if configuracion == [False]:
                self._destinatario.desenlazar()
                return
        return self._respuesta.authenticate_response()


class SetHolterConfig(AbsComando):
    
    def ejecutar(self, payload_data = None): # arreglar la abstracta : config = None
        self._comando.armar_comando(payload_data)
        self._destinatario.conectar()
        self._destinatario.enviar(self._comando.paquete)
        configuracion = self._destinatario.recibir(1)
        if configuracion == [False]:
            self._destinatario.desenlazar()
            return
        self._respuesta.desarmar_respuesta(configuracion)
        return self._respuesta.authenticate_response()


class SetLoggingMode(AbsComando):

    def ejecutar(self, payload_data = None):
        self._comando.armar_comando()
        self._destinatario.conectar()
        self._destinatario.enviar(self._comando.paquete)
        configuracion = self._destinatario.recibir(1)
        if configuracion == [False]:
            self._destinatario.desenlazar()
            return
        self._respuesta.desarmar_respuesta(configuracion)
        return self._respuesta.authenticate_response()


class SetDownloadMode(AbsComando):

    def ejecutar(self, payload_data = None):
        self._comando.armar_comando()
        self._destinatario.conectar()
        self._destinatario.enviar(self._comando.paquete)
        configuracion = self._destinatario.recibir(1)
        if configuracion == [False]:
            self._destinatario.desenlazar()
            return
        self._respuesta.desarmar_respuesta(configuracion)
        return self._respuesta.authenticate_response()


class GetDownloadFile(AbsComando):
    def ejecutar(self, payload_data = None):
        self._comando.armar_comando(payload_data)
        # self._destinatario.conectar()
        self._destinatario.enviar(self._comando.paquete)
        file = self._destinatario.recibir(1)
        print (file, 'RECIBIR EN GETDOWNLOADFILE')
        if file == [False]:
            self._destinatario.desenlazar()
            return None

        file_contents = self._respuesta.desarmar_respuesta(file)
        return file_contents


class InformationFilePage(AbsComando):
    def ejecutar(self, payload_data):
        """
        This method return three parameters without send any command.

        Args:
            payload_data (int, optional): _description_. Defaults to None.

        Returns:
            list: return a list with 3 elements: number of page, amount bytes and samples.
        """
        if (payload_data == None) or (payload_data == True):
            response = self._destinatario.recibir(1)
        else:
            response = payload_data
        information_page = self._respuesta.desarmar_respuesta(response)
        return information_page


class DownloadRegisterData(AbsComando):
    def ejecutar(self, payload_data = None):
        response = self._destinatario.recibir(1)
        data_payload = self._respuesta.desarmar_respuesta(response)
        return data_payload


class PonerModoMonitoreo(AbsComando):
    def ejecutar(self, payload_data = None):
        # Activar modo monitoreo
        self._comando.armar_comando()
        self._destinatario.conectar()
        self._destinatario.enviar(self._comando.paquete)
        
        response = self._destinatario.recibir(1)
        if self.is_expected_response(response):
            self._respuesta.desarmar_respuesta(response)        

        while(not self._respuesta.authenticate_response()):
            print ('Datos de Poner Modo monitoreo')
            response = self._destinatario.recibir(1)
            if not self.is_expected_response(response):
                self._destinatario.desenlazar()
                print ('Error de respuesta.')
                return
            self._respuesta.desarmar_respuesta(response)

        if self._respuesta.authenticate_response():
            print ('Modo monitoreo ok')
        else:
            self._destinatario.desenlazar()
            print ('Error de respuesta.')
            return


class GetECGMonitor(AbsComando):
    def ejecutar(self, payload_data = None):
        # print ('Datos de GetECG')
        datos_ecg_monitoreo = self._destinatario.recibir(1)
        return self._respuesta.desarmar_respuesta(datos_ecg_monitoreo)


class GetMemoryInformation(AbsComando):
    def ejecutar(self, payload_data = None):
        self._comando.armar_comando()
        self._destinatario.conectar()
        self._destinatario.enviar(self._comando.paquete)
        information = self._destinatario.recibir(1)
        print ("INFORMACION MEMORIA")
        print (information)
        if information == [False]:
            self._destinatario.desenlazar()
            print ("Error al obtener información de memoria.")
            return
        return self._respuesta.desarmar_respuesta(information)


class EraseHolterMemory(AbsComando):
    def ejecutar(self, payload_data = None):
        self._comando.armar_comando()
        self._destinatario.conectar()
        self._destinatario.enviar(self._comando.paquete)
        configuracion = self._destinatario.recibir(1)
        if configuracion == [False]:
            self._destinatario.desenlazar()
            print ("Error. La memoria no pudo borrarse.")
            return
        self._respuesta.desarmar_respuesta(configuracion)
        return self._respuesta.authenticate_response()


class HolterDisconnect(AbsComando):

    def ejecutar(self, payload_data = None):
        # self._destinatario.conectar()
        response = self._destinatario.recibir(1)
        payload = self._respuesta.desarmar_respuesta(response)
        correct_response = self._respuesta.authenticate_response()

        while (not correct_response):
            response = self._destinatario.recibir(1)
            payload = self._respuesta.desarmar_respuesta(response)
            correct_response = self._respuesta.authenticate_response()

        self._destinatario.desenlazar()


class SetIdleMode(AbsComando):
    
    def ejecutar(self, payload_data = None):
        # Activar modo idle y desenlazar holter
        self._comando.armar_comando()

        if not self._destinatario._connected:            
            self._destinatario.conectar()
        self._destinatario.enviar(self._comando.paquete)

        response = self._destinatario.recibir(1)
        if not self.is_expected_response(response):
            self._destinatario.desenlazar()
            return
        self._respuesta.desarmar_respuesta(response) 
        print('Datos de Modo IDLE')
        while(not self._respuesta.authenticate_response()):
            print('Datos de Modo IDLE')
            response = self._destinatario.recibir(1)
            if not self.is_expected_response(response):
                self._destinatario.desenlazar()
                return
            self._respuesta.desarmar_respuesta(response)

        if self._respuesta.authenticate_response():
            self._destinatario.desenlazar()
            return
        else:
            print ('Error de respuesta. No se desenlazó el puerto.')
        return
        

class Destinatario:
    
    def __init__(self, tipo_vinculo):
        self._tipo_vinculo = tipo_vinculo
        self._connected = False

    def conectar(self):
        try:
            self._tipo_vinculo.conectar()
            self._connected = True
        except:
            self._connected = False
            print ('Error de conexión. Intente nuevamente.')

    def enviar(self, paquete):
        self._tipo_vinculo.enviar(paquete)

    def recibir(self, amount_packages = 1):
        return self._tipo_vinculo.recibir(amount_packages)
    
    def desenlazar(self):
        try:
            self._tipo_vinculo.desconectar()
            self._connected = False
        except:
            print ('Error de desconección.')


class Invocador:
    @property
    def link_type(self):
        return self._link_type
    @link_type.setter
    def link_type(self, value):
        self._link_type = value
        
    def __init__(self):
        self._comandos = {}
        self._link_type = None

    def registrar_comando(self, nombre, comando):
        self._comandos[nombre] = comando

    def ejecutar(self, nombre, payload_data = None):
        if nombre in self._comandos.keys():
            recibido = self._comandos[nombre].ejecutar(payload_data)
            return recibido
        else:
            raise 'Comando no reconocido'