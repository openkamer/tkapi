from tkapi.core import TKItem
from tkapi.filter import RelationsFilter
from tkapi.filter import SoortFilter
from tkapi.filter import ZaakRelationFilter


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
    def activiteit(self):
        from tkapi.activiteit import Activiteit
        return self.related_item(Activiteit)

    @property
    def besluit(self):
        from tkapi.besluit import Besluit
        return self.related_item(Besluit)

    @property
    def documenten(self):
        from tkapi.document import Document
        return self.related_items(Document)
