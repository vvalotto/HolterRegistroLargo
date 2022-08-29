"""
Clase Abstracta Contexto para uso de repositorios
"""
from abc import ABCMeta, abstractmethod


class GenericContext(metaclass=ABCMeta):
    """
    Clase abstracta que define la interfaz de la persistencia de datos
    """
    @abstractmethod
    def __init__(self, resource):

        self._resource = None
        if resource is None or resource == "":
            raise Exception("Name of resource its empty")
        self._resource = resource

    @property
    def resource(self):
        return self._resource