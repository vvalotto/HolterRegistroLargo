"""
Clase que inicializa la configuración de descarga.
"""

from aplicacion.gestores.manager_download import DownloadManager
from aplicacion.gestores.gestor_operacion import GestorOperacion
from aplicacion.gestores.gestor_vinculo import GestorVinculo
from aplicacion.gestores.manager_study import StudyManager, StudyEKG
from aplicacion.gestores.gestor_signal import SignalManager

from infraestructura.persistencia.mapeadores.register_EKG_mapper import *
from infraestructura.persistencia.contexto.directories_context import *
from infraestructura.persistencia.repositorios.signal_register_repository import *


class DownloadConfigurator:
    
    def __init__(self, invocator) -> None:
        # Datos del estudio
        self._study = StudyEKG()
        self._study_manager = StudyManager(self._study)
        information_study = self._study_manager.get_study_configuration()
        # Inicialización de repositorio y creación de directorios
        resource = ['Holter Bagó', information_study [0], information_study [1]]
        repository_of_download = SignalRegisterRepository(DirContext(resource), RegisterDataMapper())
        repository_of_download.create() 
        # Vínculo con dispositivo Holter
        self._gestor_vinculo = GestorVinculo(invocator)
        self._gestor_vinculo.set_download_mode()
        # Inicio de proceso de descarga por archivo
        self._manager_download = DownloadManager(invocator)
        self._manager_download.assign_repostory(repository_of_download)
        self._manager_download.start_download()


       