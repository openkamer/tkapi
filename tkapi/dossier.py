from typing import List

from tkapi.core import TKItem
from tkapi.document import Document
from tkapi.filter import ZaakRelationFilter


class DossierFilter(ZaakRelationFilter):

    def filter_nummer(self, nummer):
        filter_str = "Nummer eq {}".format(nummer)
        self._filters.append(filter_str)

    def filter_toevoeging(self, toevoeging: str):
        filter_str = "Toevoeging eq '{}'".format(toevoeging)
        self._filters.append(filter_str)

    def filter_zaak(self, zaak_number):
        filter_str = "Zaak/any(z:z/Nummer eq '{}')".format(zaak_number)
        self._filters.append(filter_str)

    def filter_afgesloten(self, is_afgesloten=True):
        is_afgesloten_str = 'true' if is_afgesloten else 'false'
        filter_str = "Afgesloten eq {}".format(is_afgesloten_str)
        self._filters.append(filter_str)


class Dossier(TKItem):
    type = 'Kamerstukdossier'

    @staticmethod
    def create_filter():
        return DossierFilter()

    @property
    def zaken(self):
        from tkapi.zaak import Zaak
        return self.related_items(Zaak)

    @property
    def documenten(self) -> List[Document]:
        return self.related_items(Document)

    @property
    def nummer(self):
        return self.get_property_or_none('Nummer')

    @property
    def toevoeging(self):
        return self.get_property_or_none('Toevoeging')

    @property
    def afgesloten(self):
        return self.json['Afgesloten']

    @property
    def titel(self):
        return self.get_property_or_empty_string('Titel')

    @property
    def organisatie(self):
        return self.get_property_or_empty_string('Organisatie')


class DossierWetsvoorstel(Dossier):
    from tkapi.zaak import ZaakSoort
    filter_param = 'Zaak/any(z:z/Soort eq \'{}\') or Zaak/any(z:z/Soort eq \'{}\') or Zaak/any(z:z/Soort eq \'{}\')'\
        .format(ZaakSoort.WETGEVING.value, ZaakSoort.INITIATIEF_WETGEVING.value, ZaakSoort.BEGROTING.value)
