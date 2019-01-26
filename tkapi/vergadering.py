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


class Vergadering(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'Vergadering'

    @staticmethod
    def create_filter():
        return VergaderingFilter()

    @property
    def verslagen(self):
        from tkapi.document import Document
        return self.related_items(Document)

    @property
    def activiteiten(self):
        from tkapi.activiteit import Activiteit
        return self.related_items(Activiteit)

    @property
    def soort(self):
        return self.get_property_or_empty_string('Soort')

    @property
    def titel(self):
        return self.get_property_or_empty_string('Titel')

    @property
    def nummer(self):
        return self.get_property_or_none('Nummer')

    @property
    def zaal(self):
        return self.get_property_or_empty_string('Zaal')

    @property
    def begin(self):
        return self.get_datetime_or_none('Begin')

    @property
    def einde(self):
        return self.get_datetime_or_none('Einde')

    @property
    def samenstelling(self):
        return self.get_property_or_empty_string('Samenstelling')
    #
    # @staticmethod
    # def begin_date_key():
    #     return 'Begin'
    #
    # @staticmethod
    # def end_date_key():
    #     return 'Einde'
