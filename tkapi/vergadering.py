from enum import Enum

import tkapi
from tkapi.util import util


class VergaderingSoort(Enum):
    COMMISSIE = 'Commissie'
    PLENAIR = 'Plenair'


class VergaderingFilter(tkapi.SoortFilter):

    def __init__(self):
        super().__init__()

    def filter_date_range(self, begin_datetime, end_datetime):
        filter_str = "Begin ge " + util.datetime_to_odata(begin_datetime)
        self._filters.append(filter_str)
        filter_str = "Einde lt " + util.datetime_to_odata(end_datetime)
        self._filters.append(filter_str)


class Vergadering(tkapi.TKItem):
    url = 'Vergadering'
    expand_params = ['Verslag']

    @staticmethod
    def create_filter() -> VergaderingFilter:
        return VergaderingFilter()

    @property
    def verslag(self):
        from tkapi.verslag import Verslag
        return self.related_item(Verslag)

    @property
    def soort(self):
        return self.get_property_enum_or_none('Soort', VergaderingSoort)

    @property
    def titel(self):
        return self.get_property_or_empty_string('Titel')

    @property
    def nummer(self):
        return self.get_property_or_none('VergaderingNummer')

    @property
    def zaal(self):
        return self.get_property_or_empty_string('Zaal')

    @property
    def datum(self):
        return self.get_datetime_or_none('Datum')

    @property
    def begin(self):
        return self.get_datetime_or_none('Aanvangstijd')

    @property
    def einde(self):
        return self.get_datetime_or_none('Sluiting')

    @property
    def samenstelling(self):
        return self.get_property_or_empty_string('Samenstelling')
