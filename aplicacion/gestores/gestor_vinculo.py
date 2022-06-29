from platform import release
import sys
sys.path.append('../../')
from infraestructura.interop.comando import Invocador


class GestorVinculo:
    """Este gestor tiene la tarea de vincular el sistema con el dispositivo.
    No se encarga de indicar acciones al dispositivo específicas al dispositivo, 
    sino que sólo establece la conexión y desconexión del mismo según el comando 
    indicado.
    """

    def __init__(self, invocador):
        self._invocador = invocador

    def obtener_status_holter(self):
        self._invocador.ejecutar("leer_estado")

    def obtener_configuracion_holter(self):
        self._invocador.ejecutar("leer_configuracion")

    def poner_modo_monitoreo(self):
        self._invocador.ejecutar("poner_modo_monitoreo")

    def parar_holter(self): # modo IDLE
        self._invocador.ejecutar("parar_modo_holter")

    def set_download_mode(self):
        self._invocador.ejecutar ("poner_modo_descarga")

    def desenlazar_holter(self):
        self._invocador.ejecutar("desenlazar_holter")