from aplicacion.gestores.gestor_operacion import GestorOperacion
from aplicacion.gestores.gestor_signal import SignalManager
from aplicacion.DTOs.register_DTO import RegisterDTO


class DownloadManager:
    def __init__(self, invocador):

        self._invocador = invocador
        self._operation_manager = GestorOperacion(self._invocador)
        self._signal_dto = RegisterDTO()
        self._manager_signal = SignalManager(self._signal_dto, None, None) # Usar **kwargs

    def start_download(self):
        amount_files = self._operation_manager.get_memory_information()
        # ahora se implementa el de descarga/captura de archivos
        # se debe pedir de a un archivo. para esto se envia a armar 
        # comando el dato del nro de archivo que se pide

        for file_number in range(amount_files):
            register_data, samples_page, bytes_page = self._operation_manager.download_file(file_number)

            self._manager_signal.save_register_channels(register_data, samples_page, bytes_page, file_number) # podría ir en otro hilo - *observer*

