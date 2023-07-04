from enum import Enum

from tkapi.core import TKItem
from tkapi.filter import SoortFilter
from tkapi.util import util
from tkapi.verslag import Verslag


class VergaderingSoort(Enum):
    COMMISSIE = 'Commissie'
    PLENAIR = 'Plenair'


class VergaderingFilter(SoortFilter):

    def __init__(self):
        super().__init__()

    def filter_date_range(self, begin_datetime, end_datetime=None):
        filter_str = "Begin ge {}".format(util.datetime_to_odata(begin_datetime))
        self._filters.append(filter_str)

        if end_datetime:
            filter_str = "Einde lt {}".format(util.datetime_to_odata(end_datetime))
            self._filters.append(filter_str)

    def filter_changed_since(self, since_datetime):
        filter_str = "ApiGewijzigdOp ge {}".format(util.datetime_to_odata(since_datetime))
        self._filters.append(filter_str)


class Vergadering(TKItem):
    type = 'Vergadering'
    expand_params = ['Verslag']

    @staticmethod
    def create_filter() -> VergaderingFilter:
        return VergaderingFilter()

    @property
    def verslag(self) -> Verslag:
        return self.related_item(Verslag)

    @property
    def soort(self) -> VergaderingSoort:
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
