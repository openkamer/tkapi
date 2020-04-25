from enum import Enum

from tkapi.core import TKItem
from tkapi.filter import SoortFilter


class VerslagStatus(Enum):
    CASCO = 'Casco'
    GECORRIGEERD = 'Gecorrigeerd'
    GERECTIFICEERD = 'Gerectificeerd'
    ONGECORRIGEERD = 'Ongecorrigeerd'


class VerslagSoort(Enum):
    EINDPUBLICATIE = 'Eindpublicatie'
    TUSSENPUBLICATIE = 'Tussenpublicatie'
    VOORPUBLICATIE = 'Voorpublicatie'


class VerslagFilter(SoortFilter):

    def __init__(self):
        super().__init__()

    def filter_status(self, status):
        self.filter_property(property_name='Status', value=status)


class Verslag(TKItem):
    type = 'Verslag'
    expand_params = ['Vergadering']

    @staticmethod
    def create_filter():
        return VerslagFilter()

    @property
    def vergadering(self) -> "Vergadering":
        from tkapi.vergadering import Vergadering
        return self.related_item(Vergadering)

    @property
    def soort(self) -> VerslagSoort:
        return self.get_property_enum_or_none('Soort', VerslagSoort)

    @property
    def status(self) -> VerslagStatus:
        return self.get_property_enum_or_none('Status', VerslagStatus)
