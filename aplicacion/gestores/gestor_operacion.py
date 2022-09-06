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
    
    def get_memory_information(self):
        amount_files = self._invocador.ejecutar ("informacion_memoria_holter")
        return amount_files
        
    def erase_holter_memory (self):
        self._invocador.ejecutar ("borrar_memoria_holter")

    def get_file_time(self, file_number):
        file_date = self._invocador.ejecutar("descargar_archivo", file_number) # hora del archivo # en gestor download ?
        return file_date        
    
    def get_information_file_page(self):
        information_file_page = self._invocador.ejecutar("informacion_pagina_archivo") # datos de la pagina
        return information_file_page
    
    def download_files(self):
        file_data = b''
        while(True):
            payload = self._invocador.ejecutar("descargar_datos_registro")
            if payload == 'EOF':
                break
            else:
                file_data = file_data + payload        
        return file_data, payload
        
    # def get_information_file_page(self): #CONTIENE 2 ACCIONES DENTRO. REVISAR.
    #     samples_page = {}
    #     bytes_page = {}
    #     register_data = []
    #     payload = None        
    #     while(True): # lectura por pagina, se suponen 64 ciclos (64 páginas)
    #         information_file_page = self._invocador.ejecutar("informacion_pagina_archivo") # datos de la pagina
    #         # la idea es guardar los bytes y muestras por pagina - lista de bytes por pagina
    #         if (information_file_page == 'EOF') or (payload == 'EOF'):
    #             break
    #         if information_file_page!=None:
    #             samples_page[information_file_page[0]] = information_file_page[1]
    #             bytes_page[information_file_page[0]] = information_file_page[2]
    #             information_file_page = None
            
    #         file_data, payload = self.download_files()
    #         register_data.append(file_data)
    #     return register_data, samples_page, bytes_page

    # def download_file(self):
    #     # self._invocador.ejecutar("descargar_archivo", file_number) # hora del archivo # en gestor download ?
        
    #     samples_page = {}
    #     bytes_page = {}
    #     register_data = []
    #     data = b''
    #     payload = None
        
    #     while(True): # lectura por pagina, se suponen 64 ciclos (64 páginas)
    #         information_file_page = self._invocador.ejecutar("informacion_pagina_archivo") # datos de la pagina
    #         # la idea es guardar los bytes y muestras por pagina - lista de bytes por pagina
    #         if (information_file_page == 'EOF') or (payload == 'EOF'):
    #             break
    #         if information_file_page!=None:
    #             samples_page[information_file_page[0]] = information_file_page[1]
    #             bytes_page[information_file_page[0]] = information_file_page[2]
                
    #             self._append_download_data = True
    #             information_file_page = None

    #         while(self._append_download_data):
                
    #             payload = self._invocador.ejecutar("descargar_datos_registro")
    #             if payload == 'EOF':
    #                 break
    #             else:
    #                 data = data + payload
            
    #         register_data.append(data)
    #         data = b''
    #         self._append_download_data = False

    #     return register_data, samples_page, bytes_page
            
            # TODO: Pensar en un DTO y ENTIDAD. Mantener los datos en un lugar para que,
            # llamando a otro método (almacenamiento/persistencia/save_csv) del gestor
            # se guarden los datos en la estructura definida en archivos csv.
        