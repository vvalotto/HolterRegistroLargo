"""
Se implementa el repositorio del Registro de la señal.
"""
from dominio.repositories.base_signal_repository import *
from infraestructura.persistencia.modelo.directories_register import *

class SignalRegisterRepository (BaseSignalRepository):

    def __init__(self, context, mapper):
        super().__init__(context)
        self._mapper = mapper

    def create(self, entity):
        return super().create(entity)
    
    def read(self, id):
        return super().read(id)
    
    def update(self, entity):
        return super().update(entity)
    
    def delete(self, id):
        return super().delete(id)

    