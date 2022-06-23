import sys
sys.path.append('../../')
from infraestructura.interop.comando import Invocador
from aplicacion.gestores.gestor_signal import SignalManager

class GestorOperacion:
    """Este gestor tiene la responsabilidad de indicarle al dispositivo la operación
    o acción que debe comenzar o finalizar.
    El dispositivo debe estar, primero, vinculado con el sistema (ver gestor_vinculo).
    """

    def __init__(self, invocador):
        self._invocador = invocador

    def monitorear_holter(self, monitor_ecg, lock_monitor,event_monitor):
        manager_signal = SignalManager(monitor_ecg, lock_monitor, event_monitor) # Usar **kwargs
        while (monitor_ecg.state):
            channels = self._invocador.ejecutar("obtener_ecg_monitoreo")
            manager_signal.set_dto_channels(channels)
        event_monitor.set()     
        print ('fin del ciclo de adquisición')

    def preparar_holter_para_monitoreo(self):
        self._invocador.ejecutar("poner_hora")
        self._invocador.ejecutar("poner_configuracion")