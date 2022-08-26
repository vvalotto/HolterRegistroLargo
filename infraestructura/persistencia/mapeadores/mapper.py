from abc import ABCMeta, abstractmethod

class AbsMapper(metaclass=ABCMeta):
    
    def __init__(self):
        pass

    abstractmethod
    def dto_to_entity(self, dto):
        pass

    abstractmethod
    def entity_to_dto(self, entity):
        pass
