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

        for file_number in range(amount_files):
            # adquiere los datos de un archivo desde el dispositivo
            # Hora del archivo
            file_date = self._operation_manager.get_file_time(file_number)
            # Datos por página de archivo
            samples_page = {}
            bytes_page = {}
            register_data = []
            payload = None        
            while(True): # lectura por pagina, se suponen 64 ciclos (64 páginas)
                # information_file_page = self._operation_manager.get_information_file_page()
                information_file_page = self._file_page_information()
                # la idea es guardar los bytes y muestras por pagina - lista de bytes por pagina
                if (information_file_page == 'EOF') or (payload == 'EOF'):
                    break
                if information_file_page!=None:
                    samples_page[information_file_page[0]] = information_file_page[1]
                    bytes_page[information_file_page[0]] = information_file_page[2]
                    information_file_page = None

                file_data, payload = self._operation_manager.download_files()
                register_data.append(file_data)
            # Fin de uso del gestor de operación.

            # # # register_data, samples_page, bytes_page = self._operation_manager.download_file()
            
            # separador de canales sin decodificarlos

            channels_undecoded = channel_splitter(register_data, samples_page, bytes_page) # Podría ser llamado por el gestor de señal.
            # decodificación de canales
            channels = decode_register_channels(register_data, channels_undecoded) # Podría ser llamado por el gestor de señal.

            # El repositorio se encarga de almacenar los datos obtenidos desde el dispositivo
            # Almacena archivo por archivo. Unidad atómica establecida: archivo

            self._manager_signal.set_register_dto(register_data,channels_undecoded, channels)

            self._repository.create(self._signal_dto, file_date)

            # self._manager_signal.save_register_channels(register_data, samples_page, bytes_page, file_number, self._repository) # podría ir en otro hilo - *observer*

    def _file_page_information(self):
        return self._operation_manager.get_information_file_page()

    def _memory_information(self):
        return self._operation_manager.get_memory_information()

    def assign_repostory(self, repository):
        self._repository = repository
        return
