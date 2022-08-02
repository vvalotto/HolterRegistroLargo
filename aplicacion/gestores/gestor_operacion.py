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

    def set_current_time(self, current_time): # cambiar nombre a configurar holter
        
        time_set = self._invocador.ejecutar("poner_hora", current_time)
        if time_set:
            print ("Se configuró la hora correctamente")
        else: 
            print ("NO pudo configurarse la hora correctamente")

    def set_study_configuration(self, config=None):

        config_set = self._invocador.ejecutar("poner_configuracion", config)

        if config_set:
            print ("Se configuró el holter correctamente")
        else: 
            print ("NO pudo configurarse el holter correctamente")

    def start_logging_mode(self):
        self._invocador.ejecutar("poner_modo_logging")
    
    def erase_holter_memory (self):
        self._invocador.ejecutar ("borrar_memoria_holter")