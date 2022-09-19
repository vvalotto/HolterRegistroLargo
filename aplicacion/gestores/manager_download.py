from aplicacion.gestores.gestor_operacion import GestorOperacion
from aplicacion.gestores.gestor_signal import SignalManager
from aplicacion.DTOs.register_DTO import RegisterDTO

from dominio.servicios.channel_splitter import channel_splitter
from dominio.servicios.decoder import decode_register_channels


class DownloadManager:
    def __init__(self, invocador):

        self._invocador = invocador
        self._operation_manager = GestorOperacion(self._invocador)
        self._signal_dto = RegisterDTO()
        self._manager_signal = SignalManager(self._signal_dto, None, None) # Usar **kwargs
        #TODO: VER. En el repositorio que le asigno ya le paso un mapeador de señal, que se encuentra en persistencia. 
        self._repository = None

    def start_download(self):
        # amount_files = self._operation_manager.get_memory_information() # Pasarle este dato al repositorio?. Para control de descarga..
        amount_files = self._memory_information()
        # ahora se implementa el de descarga/captura de archivos
        # se debe pedir de a un archivo. para esto se envia a armar 
        # comando el dato del nro de archivo que se pide

        for file_number in range(1,amount_files): # TODO: Luego de corregir el firmware se debe sumar uno a amount_files
            # El dispositivo comienza a entregar los archivos desde el nro 1
            # adquiere los datos de un archivo desde el dispositivo
            # Hora del archivo
            print (file_number, 'NUMERO DE ARCHIVO')
            file_date = self._operation_manager.get_file_time(file_number)
            # Datos por página de archivo
            samples_page = {}
            bytes_page = {}
            register_data = []
            datos = None    
            information_file_page = None
            contador_muestras = 0
            while(True): # lectura por pagina
                if (information_file_page == 'EOF') or (datos == 'EOF'):
                    break
                information_file_page = self.file_page_information(datos)
                # la idea es guardar los bytes y muestras por pagina - lista de bytes por pagina
                if information_file_page!=None:
                    samples_page[information_file_page[0]] = information_file_page[1]
                    contador_muestras += information_file_page[1]
                    bytes_page[information_file_page[0]] = information_file_page[2]

                file_data, datos = self._operation_manager.download_files()
                
                # if information_file_page[0] != 0:
                register_data.append(file_data)
            # Fin de uso del gestor de operación.
            
            # separador de canales sin decodificarlos
            channels_undecoded = channel_splitter(register_data, samples_page, bytes_page) # Podría ser llamado por el gestor de señal.
            # decodificación de canales
            channels = decode_register_channels(register_data, channels_undecoded) # Podría ser llamado por el gestor de señal.

            # El repositorio se encarga de almacenar los datos obtenidos desde el dispositivo
            # Almacena archivo por archivo. Unidad atómica establecida: archivo

            self._manager_signal.set_register_dto(register_data,channels_undecoded, channels)

            self._repository.create(self._signal_dto, [file_date, contador_muestras])

    def file_page_information(self, payload):
        return self._operation_manager.get_information_file_page(payload)

    def _memory_information(self):
        return self._operation_manager.get_memory_information()

    def assign_repostory(self, repository):
        self._repository = repository
        return
