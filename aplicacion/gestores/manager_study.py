# import sys
# sys.path.append('../../')

from dominio.entidades.study import StudyEKG
from aplicacion.mapeadores.mapper_study import StudyMapper

class StudyManager:
    
    def __init__(self, study:StudyEKG) -> None:
        self._study = study
        self._study_mapper = StudyMapper()
    
    def get_study_configuration(self,current_time):
        self._study_mapper.defect_study_config(current_time)
        
        self._study_mapper.update_study_config(self._study)
        
        information_study = self._study_mapper.get_study_config(self._study)
        return information_study
    
    def time_init_configuration(self,current_time):
        self._study_mapper.set_time_init(self._study,current_time)



