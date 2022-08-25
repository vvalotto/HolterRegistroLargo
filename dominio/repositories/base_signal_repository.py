"""
Clase Abstracta que define el repositorio de las señales
"""

from base_repository import *


class BaseSignalRepository(BaseRepository):

    @abstractmethod
    def read_for_date(self, event):
        pass
    @abstractmethod
    def read_for_channel(self, event):
        pass
