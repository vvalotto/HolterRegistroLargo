from platform import release
import time
from comando import Invocador


class GestorVinculo:

    def __init__(self, invocador):
        self._invocador = invocador

    def obtener_status_holter(self):
        self._invocador.ejecutar("leer_estado")

    def obtener_configuracion_holter(self):
        self._invocador.ejecutar("leer_configuracion")

    def preparar_holter_para_monitoreo(self):
        self._invocador.ejecutar("poner_hora")
        self._invocador.ejecutar("poner_configuracion")

    def poner_modo_monitoreo(self):
        self._invocador.ejecutar("poner_modo_monitoreo")
        time.sleep(1)

    def monitorear_holter(self, monitor_ecg, lock_monitor,event_monitor):

        while (monitor_ecg.state):
            channels = self._invocador.ejecutar("obtener_ecg_monitoreo")
            with lock_monitor:
                if not monitor_ecg._channel_1 == channels[0]:
                    monitor_ecg._channel_1 = channels[0].copy()
                    monitor_ecg._channel_2 = channels[1].copy()
                    monitor_ecg._channel_3 = channels[2].copy()
                    event_monitor.set()
        event_monitor.set()     
        print ('fin del ciclo de adquisición')

    def parar_holter(self): # modo IDLE
        self._invocador.ejecutar("parar_modo_holter")

    def desenlazar_holter(self):
        self._invocador.ejecutar("desenlazar_holter")