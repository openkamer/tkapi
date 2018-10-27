import tkapi


class BesluitRelationFilter(tkapi.RelationFilter):

    @property
    def related_url(self):
        return Besluit.url


class BesluitFilter(tkapi.SoortFilter, tkapi.ZaakRelationFilter):

    def __init__(self):
        super().__init__()


class Besluit(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'Besluit'

    @staticmethod
    def create_filter():
        return BesluitFilter()

    @property
    def zaken(self):
        from tkapi.zaak import Zaak
        return self.related_items(Zaak)

    @property
    def stemmingen(self):
        from tkapi.stemming import Stemming
        return self.related_items(Stemming)

    @property
    def agendapunt(self):
        from tkapi.agendapunt import Agendapunt
        return self.related_items(Agendapunt)

    @property
    def soort(self):
        return self.get_property_or_empty_string('Soort')

    @property
    def status(self):
        return self.get_property_or_empty_string('Status')

    @property
    def slottekst(self):
        return self.get_property_or_empty_string('Slottekst')
