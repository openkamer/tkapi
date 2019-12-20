from typing import List
from tkapi.core import TKItem
from tkapi.filter import RelationsFilter
from tkapi.filter import SoortFilter
from tkapi.filter import ZaakRelationFilter
from tkapi.activiteit import Activiteit
from tkapi.document import Document


class AgendapuntRelationFilter(RelationsFilter):

    @property
    def related_url(self):
        return Agendapunt.type


class AgendapuntFilter(SoortFilter, ZaakRelationFilter):

    def __init__(self):
        super().__init__()

    def filter_has_activiteit(self):
        filter_str = 'Activiteit/any(a:a ne null)'
        self._filters.append(filter_str)


class Agendapunt(TKItem):
    type = 'Agendapunt'
    expand_params = ['Activiteit', 'Besluit', 'Document']

    @staticmethod
    def create_filter():
        return AgendapuntFilter()

    @property
    def zaken(self):
        from tkapi.zaak import Zaak
        return self.related_items(Zaak)

    @property
    def activiteit(self) -> Activiteit:
        return self.related_item(Activiteit)

    @property
    def besluit(self):
        from tkapi.besluit import Besluit
        return self.related_item(Besluit)

    @property
    def documenten(self) -> List[Document]:
        return self.related_items(Document)

    @property
    def onderwerp(self):
        return self.get_property_or_empty_string('Onderwerp')

    @property
    def volgorde(self):
        return self.get_property_or_none('Volgorde')

    @property
    def begin(self):
        return self.get_datetime_or_none('Aanvangstijd')

    @property
    def einde(self):
        return self.get_datetime_or_none('Eindtijd')

    @property
    def rubriek(self):
        return self.get_property_or_empty_string('Rubriek')

    @property
    def noot(self):
        return self.get_property_or_empty_string('Noot')
