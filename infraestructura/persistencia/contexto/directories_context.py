from infraestructura.persistencia.contexto.context import GenericContext
from dateutil import parser

from math import ceil

class DirContext(GenericContext):
    """ Especific context for create and manipulate directories

    Args:
        GenericContext (_type_): _description_
    """
    @property
    def resource(self):
        return self._resource

    def __init__(self, resource):
        super().__init__(resource)
        self._resource = self._adapt_resourse(resource)

    def _adapt_resourse(self, resource):
        name = resource[0]
        date = parser.parse (resource[1])
        amount_days = ceil((self.resource[2])/(24*60))
    
        return [name, date, amount_days]