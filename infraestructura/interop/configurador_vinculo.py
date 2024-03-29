from infraestructura.interop.comando import *
from infraestructura.interop.holter_comands import *
from infraestructura.interop.holter_responses import *

class InvocatorInit:
    """
    This class initializes a calling object with a single connection type
    and registers all commands for communication with the device.
    Each command record action needs an associated command that contains a
    Holter command and a response command.
    """

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

# Leer Configuración Holter
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

# Poner holter en hora
        self._invocador.registrar_comando("poner_hora",    SetHolterTime (self._holter_connected_to, 
                                                    CommandWriteTime(),
                                                    RespuestaHolterEscritiuraOK()))

# Poner Configuración del holter
        self._invocador.registrar_comando("poner_configuracion",    SetHolterConfig (self._holter_connected_to, 
                                                    CommandWriteConfig(),
                                                    RespuestaHolterEscritiuraOK()))

# Poner Modo Logging (iniciar registro)
        self._invocador.registrar_comando("poner_modo_logging",    SetLoggingMode (self._holter_connected_to, 
                                                    CommandLoggingMode(),
                                                    RespuestaHolterEscritiuraOK()))

# Poner Modo Download
        self._invocador.registrar_comando("poner_modo_descarga",    SetDownloadMode (self._holter_connected_to, 
                                                    CommandDownloadMode(),
                                                    RespuestaHolterEscritiuraOK()))

# Pedir información de memoria
        self._invocador.registrar_comando("informacion_memoria_holter",    GetMemoryInformation (self._holter_connected_to, 
                                                    CommandMemoryInformation(),
                                                    RespuestaInformacionMemoria()))

# Borrar la memoria // si o sí tiene que estar en modo download
        self._invocador.registrar_comando("borrar_memoria_holter",    EraseHolterMemory (self._holter_connected_to, 
                                                    CommandEraseMemory(),
                                                    RespuestaHolterEscritiuraOK()))

# Descargar un archivo
        self._invocador.registrar_comando("descargar_archivo",    GetDownloadFile (self._holter_connected_to, 
                                                    CommandDownloadFile(),
                                                    RespuestaDescargaArchivo()))

# Información de página de archivo
        self._invocador.registrar_comando("informacion_pagina_archivo",    InformationFilePage (self._holter_connected_to, 
                                                    ComandEmpty(),
                                                    RespuestaDescargaInformacionPagina()))

# Descarga datos de registro
        self._invocador.registrar_comando("descargar_datos_registro",    DownloadRegisterData (self._holter_connected_to, 
                                                    ComandEmpty(),
                                                    RespuestaDownloadRegisterData()))

    @property
    def invocador (self):
        return self._invocador
        
    @invocador.setter
    def invocador (self, value):
        self._invocador = value