import tkapi
from tkapi.zaak import ZaakSoort


class DossierFilter(tkapi.ZaakRelationFilter):

    def filter_nummer(self, nummer):
        filter_str = "Nummer eq " + str(nummer)
        self._filters.append(filter_str)

    def filter_zaak(self, zaak_number):
        filter_str = "Zaak/any(z:z/Nummer eq '{}')".format(zaak_number)
        self._filters.append(filter_str)

    def filter_afgesloten(self, is_afgesloten):
        is_afgesloten_str = 'true' if is_afgesloten else 'false'
        filter_str = "Afgesloten eq " + is_afgesloten_str
        self._filters.append(filter_str)


class Dossier(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'Kamerstukdossier'

    @staticmethod
    def create_filter():
        return DossierFilter()

    @property
    def zaken(self):
        from tkapi.zaak import Zaak
        return self.related_items(Zaak)

    @property
    def documenten(self):
        from tkapi.document import Document
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
    filter_param = 'Zaak/any(z:z/Soort eq \'{}\') or Zaak/any(z:z/Soort eq \'{}\') or Zaak/any(z:z/Soort eq \'{}\')'\
        .format(ZaakSoort.WETGEVING.value, ZaakSoort.INITIATIEF_WETGEVING.value, ZaakSoort.BEGROTING.value)
