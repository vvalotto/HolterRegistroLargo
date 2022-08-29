from dominio.entidades.register import Register # no es necesaria la importación
from aplicacion.DTOs.register_DTO import RegisterDTO # no es necesario la importación
from infraestructura.persistencia.mapeadores.mapper import AbsMapper

class RegisterDataMapper(AbsMapper):

    def __init__(self): # , context):
        # self._context = context
        self._entity = None
        self._dto_register_data = None

    def dto_to_entity(self, dto:RegisterDTO):
        self._dto_register_data = dto

        self._entity = Register()
        self._entity.type = self._dto_register_data.type
        self._entity.channel_1 = self._dto_register_data.channel_1.copy()
        self._entity.channel_2 = self._dto_register_data.channel_2.copy()
        self._entity.channel_3 = self._dto_register_data.channel_3.copy()
        self._entity.register_data = self._dto_register_data.register_data.copy()

        return self._entity

    def entity_to_dto(self, register:Register):
        self._entity = register

        self._dto_register_data = RegisterDTO()

        self._dto_register_data.type = self._entity.type
        self._dto_register_data.channel_1 = self._entity.channel_1.copy()
        self._dto_register_data.channel_2 = self._entity.channel_2.copy()
        self._dto_register_data.channel_3 = self._entity.channel_3.copy()
        self._dto_register_data.register_data = self._entity.register_data.copy()

        return self._dto_register_data