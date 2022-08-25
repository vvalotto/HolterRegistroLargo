"""
Clase Abstracta Repositorio - de las entidades contenidas en señal.
"""
from abc import *


class BaseRepository(metaclass=ABCMeta):

    @property
    def context(self):
        return self._context

    def __init__(self, context):
        self._context = context
        return

    @abstractmethod
    def create(self, entity):
        pass

    @abstractmethod
    def read(self, id):
        pass

    @abstractmethod
    def update(self, entity):
        pass

    @abstractmethod
    def delete(self, id):
        pass

    