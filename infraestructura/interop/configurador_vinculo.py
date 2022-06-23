from infraestructura.interop.comando import *
from infraestructura.interop.holter_comands import *
from infraestructura.interop.holter_responses import *

class InvocatorInit:

    def __init__(self, connection_type):
        
        if connection_type == 'USB_CONNECTION':
            connection_type = EnlaceUSB()

        if connection_type == 'DONGLE_CONNECTION':
            connection_type = EnlaceDongle()    

        self._holter_connected_to = Destinatario (connection_type)    

        self._invocador = Invocador()
   
# Leer Status Holter
        comando = ComandoLecturaStatusEnvio()
        self._invocador.registrar_comando("leer_estado", LectorStatusHolter(self._holter_connected_to, 
                                            comando,
                                            RespuestaHolterStatus()))

# Configurar Holter
        self._invocador.registrar_comando("leer_configuracion",   LectorConfiguracionHolter(self._holter_connected_to, 
                                                    ComandoLecturaConfiguracionEnvio(), 
                                                    RespuestaHolterConfiguracion()))

# Parar Holter
        self._invocador.registrar_comando("parar_modo_holter",    SetIdleMode(self._holter_connected_to, 
                                                    ComandoEscrituraModoIdleEnvio(),
                                                    RespuestaHolterEscritiuraOK()))

# Poner Modo Monitoreo
        self._invocador.registrar_comando("poner_modo_monitoreo", PonerModoMonitoreo(self._holter_connected_to, 
                                                    ComandoEscrituraModoMonitoreoEnvio(),
                                                    RespuestaHolterEscritiuraOK()))

# Obtener ECG Monitoreo
        self._invocador.registrar_comando("obtener_ecg_monitoreo",GetECGMonitor(self._holter_connected_to, 
                                                    ComandEmpty(),
                                                    RespuestaHolterEGCMonitoreo()))

# desenlazar_holter
        self._invocador.registrar_comando("desenlazar_holter",    HolterDisconnect (self._holter_connected_to, 
                                                    ComandEmpty(),
                                                    RespuestaHolterEscritiuraOK()))

    @property
    def invocador (self):
        return self._invocador
        
    @invocador.setter
    def invocador (self, value):
        self._invocador = value

def init_invocator(connection_type):#->str('USB_CONNECTION'):

    if connection_type == 'USB_CONNECTION':
        connection_type = EnlaceUSB()

    if connection_type == 'DONGLE_CONNECTION':
        connection_type = EnlaceDongle()    

    holter_connected_to = Destinatario (connection_type)    

    invocador = Invocador()
   
# Leer Status Holter
    comando = ComandoLecturaStatusEnvio()
    invocador.registrar_comando("leer_estado", LectorStatusHolter(holter_connected_to, 
                                            comando,
                                            RespuestaHolterStatus()))

# Configurar Holter
    invocador.registrar_comando("leer_configuracion",   LectorConfiguracionHolter(holter_connected_to, 
                                                    ComandoLecturaConfiguracionEnvio(), 
                                                    RespuestaHolterConfiguracion()))

# Parar Holter
    invocador.registrar_comando("parar_modo_holter",    SetIdleMode(holter_connected_to, 
                                                    ComandoEscrituraModoIdleEnvio(),
                                                    RespuestaHolterEscritiuraOK()))

# Poner Modo Monitoreo
    invocador.registrar_comando("poner_modo_monitoreo", PonerModoMonitoreo(holter_connected_to, 
                                                    ComandoEscrituraModoMonitoreoEnvio(),
                                                    RespuestaHolterEscritiuraOK()))

# Obtener ECG Monitoreo
    invocador.registrar_comando("obtener_ecg_monitoreo",GetECGMonitor(holter_connected_to, 
                                                    ComandEmpty(),
                                                    RespuestaHolterEGCMonitoreo()))

# desenlazar_holter
    invocador.registrar_comando("desenlazar_holter",    HolterDisconnect (holter_connected_to, 
                                                    ComandEmpty(),
                                                    RespuestaHolterEscritiuraOK()))
    return invocador