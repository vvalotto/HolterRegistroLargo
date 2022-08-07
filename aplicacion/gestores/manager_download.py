from aplicacion.gestores.gestor_operacion import GestorOperacion


class DownloadManager:
    def __init__(self, invocador):
        self._invocador = invocador
        self.operation_manager = GestorOperacion(self._invocador)

    def start_download(self):
        amount_files = self.operation_manager.get_memory_information()
        # ahora se implementa el de descarga/captura de archivos
