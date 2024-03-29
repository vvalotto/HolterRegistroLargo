"""
Clase que inicializa la configuración de descarga.
"""
import sys
sys.path.append('../../')

from aplicacion.gestores.manager_download import DownloadManager
from aplicacion.gestores.gestor_operacion import GestorOperacion
from aplicacion.gestores.gestor_vinculo import GestorVinculo
from aplicacion.gestores.manager_study import StudyManager, StudyEKG
from aplicacion.gestores.gestor_signal import SignalManager

from infraestructura.persistencia.mapeadores.register_EKG_mapper import *
from infraestructura.persistencia.contexto.directories_context import *
from infraestructura.persistencia.repositorios.signal_register_repository import *

from dominio.servicios.observer import DownloadObserver


class DownloadConfigurator:
    
    def __init__(self, invocator, download_subject) -> None:
        # Datos del estudio
        self._study = StudyEKG()
        self._study_manager = StudyManager(self._study)
        study_information = self._study_manager.get_study_configuration()
        # Inicialización de repositorio y creación de directorios
        resource = ['Holter_Bago', study_information [0], study_information [1]]
        download_repository = SignalRegisterRepository(DirectoryContext(resource), RegisterDataMapper())
        # Vínculo con dispositivo Holter
        self._gestor_vinculo = GestorVinculo(invocator)
        self._gestor_vinculo.set_download_mode()
        # Inicio de proceso de descarga por archivo
        self._manager_download = DownloadManager(invocator)
        
        ## observador
        download_observer = DownloadObserver(self._manager_download)
        download_subject.attach(download_observer)
        self._manager_download.subject = download_subject
        self._manager_download.assign_repostory(download_repository)
        self._manager_download.start_download()
