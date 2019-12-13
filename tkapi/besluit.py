from enum import Enum
from typing import List

from tkapi.core import TKItem
from tkapi.filter import SoortFilter
from tkapi.filter import RelationsFilter
from tkapi.filter import ZaakRelationFilter
from tkapi.stemming import Stemming
from tkapi.agendapunt import Agendapunt


class BesluitStatus(Enum):
    BESLUIT = 'Besluit'
    CONCEPT = 'Concept voorstel'
    VOORSTEL = 'Voorstel'
    TE_VERWERKEN = 'Nog te verwerken besluit'


class BesluitRelationFilter(RelationsFilter):

    @property
    def related_url(self):
        return Besluit.type


class BesluitFilter(SoortFilter, ZaakRelationFilter):

    def __init__(self):
        super().__init__()


class Besluit(TKItem):
    type = 'Besluit'
    expand_params = ['Stemming']

    @staticmethod
    def create_filter():
        return BesluitFilter()

    @property
    def zaken(self):
        from tkapi.zaak import Zaak
        return self.related_items(Zaak)

    @property
    def zaak(self):
        from tkapi.zaak import Zaak
        return self.related_item(Zaak)

    @property
    def stemmingen(self) -> List[Stemming]:
        return self.related_items(Stemming)

    @property
    def agendapunt(self) -> Agendapunt:
        return self.related_item(Agendapunt)

    @property
    def soort(self):
        return self.get_property_or_empty_string('BesluitSoort')

    @property
    def status(self) -> BesluitStatus:
        return self.get_property_enum_or_none('Status', BesluitStatus)

    @property
    def tekst(self):
        return self.get_property_or_empty_string('BesluitTekst')

    @property
    def stemming_soort(self):
        return self.get_property_or_empty_string('StemmingsSoort')

    @property
    def opmerking(self):
        return self.get_property_or_empty_string('Opmerking')
