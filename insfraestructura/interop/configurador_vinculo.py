# from multiprocessing import connection
from comando import *
from holter_comands import *


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