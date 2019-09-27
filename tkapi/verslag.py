from enum import Enum

import tkapi


class VerslagStatus(Enum):
    CASCO = 'Casco'
    GECORRIGEERD = 'Gecorrigeerd'
    GERECTIFICEERD = 'Gerectificeerd'
    ONGECORRIGEERD = 'Ongecorrigeerd'


class VerslagSoort(Enum):
    EINDPUBLICATIE = 'Eindpublicatie'
    TUSSENPUBLICATIE = 'Tussenpublicatie'
    VOORPUBLICATIE = 'Voorpublicatie'


class VerslagFilter(tkapi.SoortFilter):

    def __init__(self):
        super().__init__()

    def filter_status(self, status):
        self.filter_property(property_name='Status', value=status)


class Verslag(tkapi.TKItem):
    type = 'Verslag'
    expand_params = ['Vergadering']

    @staticmethod
    def create_filter():
        return VerslagFilter()

    @property
    def vergadering(self):
        from tkapi.vergadering import Vergadering
        return self.related_item(Vergadering)

    @property
    def soort(self):
        return self.get_property_enum_or_none('Soort', VerslagSoort)

    @property
    def status(self):
        return self.get_property_enum_or_none('Status', VerslagStatus)
