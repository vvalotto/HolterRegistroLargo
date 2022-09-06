"""
Se implementa el repositorio del Registro de la señal.
"""
from dominio.repositories.base_signal_repository import *
from infraestructura.persistencia.mapeadores.mapper import AbsMapper # no es necesario


class SignalRegisterRepository (BaseSignalRepository):

    def __init__(self, context, mapper:AbsMapper):
        super().__init__(context)
        self._mapper = mapper
        
    def create(self, dto, file_date):
        self.context.new_file(dto, file_date)
        return
    
    def read(self, id):
        return super().read(id)
    
    def update(self, register):
        dto = self._mapper.entity_to_dto(register)
        return super().update(register)
    
    def delete(self, id):
        return super().delete(id)

    @property
    def file_date (self):
        return self._file_date
    
    @file_date.setter
    def file_date(self, value):
        self._file_date = value