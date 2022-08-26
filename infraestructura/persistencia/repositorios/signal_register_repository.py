"""
Se implementa el repositorio del Registro de la señal.
"""
from dominio.repositories.base_signal_repository import *
from infraestructura.persistencia.modelo.directories_register import *
from infraestructura.persistencia.mapeadores.mapper import AbsMapper

class SignalRegisterRepository (BaseSignalRepository):

    def __init__(self, context, mapper:AbsMapper):
        super().__init__(context)
        self._mapper = mapper

    def create(self, register):
        # dto = self._mapper.entity_to_dto(register) # no es necesario acá
        self._create_dir (self.context.resourse)
        #create_dir
        #create_subdir
    
    def read(self, id):
        return super().read(id)
    
    def update(self, register):
        dto = self._mapper.entity_to_dto(register)
        return super().update(register)
        #save_files
    
    def delete(self, id):
        return super().delete(id)

    def _create_dir(self, resourse):
        pass

    def _create_sub_dir(self, resourse):
        pass


    