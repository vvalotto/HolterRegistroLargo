# import sys
# sys.path.append('../../')
from datetime import datetime

from aplicacion.gestores.manager_study import StudyManager
from aplicacion.gestores.gestor_operacion import GestorOperacion

from dominio.entidades.study import StudyEKG

class LoggingManager:
    def __init__(self, invocador):
        self._invocador = invocador

        self._study = StudyEKG()
        self.study_manager = StudyManager(self._study)
        self.operation_manager = GestorOperacion(self._invocador)
    
    def update_configuration_command(self,current_time):
        config = self.study_manager.get_study_configuration(current_time)
        self.operation_manager.set_study_configuration(config)

    def logging_start(self):
        current_time = datetime.now()
        self.operation_manager.set_current_time(current_time)
        self.study_manager.time_init_configuration(current_time)
        self.update_configuration_command(current_time)
        self.operation_manager.start_logging_mode()