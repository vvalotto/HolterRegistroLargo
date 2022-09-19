import sys

sys.path.append('../../')
from infraestructura.interop.comando import Invocador
from aplicacion.gestores.gestor_signal import SignalManager

import time

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
        event_monitor.clear()
        # event_monitor.set()     
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
    
    def get_memory_information(self):
        amount_files = self._invocador.ejecutar ("informacion_memoria_holter")
        return amount_files
        
    def erase_holter_memory (self):
        self._invocador.ejecutar ("borrar_memoria_holter")

    def get_file_time(self, file_number):
        file_date = self._invocador.ejecutar("descargar_archivo", file_number) # hora del archivo # en gestor download ?
        return file_date        
    
    def get_information_file_page(self, payload):
        information_file_page = self._invocador.ejecutar("informacion_pagina_archivo", payload) # datos de la pagina
        return information_file_page
    
    def download_files(self):
        file_data = b''

        while(True):
            datos = self._invocador.ejecutar("descargar_datos_registro")
            if datos[1] == 'EOF':
                return file_data, datos [1]
            if datos[1]:
                return file_data, datos[0]
            else:
                file_data = file_data + datos[0] # CAMBIO DE INDICES SE AGREGÓ [2:12]  
        # return file_data, datos [0]