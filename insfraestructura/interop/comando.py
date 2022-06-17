from holter_comands import *
from abc import ABCMeta, abstractmethod
from holter_comands import *
from enlace import *
import time


class AbsComando(metaclass=ABCMeta):

    def __init__(self, destinatario, comando, respuesta):
        self._destinatario = destinatario
        self._comando = comando
        self._respuesta = respuesta

    @abstractmethod
    def ejecutar(self):
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

    def ejecutar(self):
        # Lee estatus del holter
        self._comando.armar_comando()
        self._destinatario.conectar()
        self._destinatario.enviar(self._comando.paquete)
        paquete_recibido = self._destinatario.recibir(1)
        if not self.is_expected_response(paquete_recibido):
            self._destinatario.desenlazar()
            return
        # # # self._respuesta.desarmar_respuesta(paquete_recibido)
        # # # self._destinatario.desenlazar()
        return
        

class LectorConfiguracionHolter(AbsComando):

    def ejecutar(self):
        # lee Configuracion del holter
        self._comando.armar_comando()
        self._destinatario.conectar()
        self._destinatario.enviar(self._comando.paquete)
        print(self._comando.paquete)
        configuracion = self._destinatario.recibir(1)
        if configuracion == [False]:
            self._destinatario.desenlazar()
            time.sleep(3)
            return

        return self._respuesta.desarmar_respuesta(configuracion)
        

class IdentificadorHolter(AbsComando):
    pass


class ObtenerMemoria(AbsComando):
    pass


class ObtenerEventos(AbsComando):
    pass


class ObtenerEGC(AbsComando):
    pass


class PonerHora(AbsComando):
    pass


class PonerModo(AbsComando):
    pass


class PonerModoMonitoreo(AbsComando):
    def ejecutar(self):
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
    def ejecutar(self):
        print ('Datos de GetECG')
        datos_ecg_monitoreo = self._destinatario.recibir(10)
        # if not self.is_expected_response(datos_ecg_monitoreo):
        #     return [[1],[2],[3]]
        return self._respuesta.desarmar_respuesta(datos_ecg_monitoreo)


class PonerConfiguracion(AbsComando):
    pass


class BorrarMemoria(AbsComando):
    pass


class HolterDisconnect(AbsComando):

    def ejecutar(self):
        # response = self._destinatario.recibir(1)
        correct_response = self._respuesta.desarmar_respuesta(response)
        while (not correct_response):
            response = self._destinatario.recibir(1)
            correct_response = self._respuesta.desarmar_respuesta(response)
        self._destinatario.desenlazar()


class SetIdleMode(AbsComando):
    
    def ejecutar(self):
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

    def ejecutar(self, nombre):
        if nombre in self._comandos.keys():
            recibido = self._comandos[nombre].ejecutar()
            return recibido
        else:
            raise 'Comando no reconocido'
    
    