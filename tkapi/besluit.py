import tkapi


class BesluitFilter(tkapi.SoortFilter, tkapi.ZaakRelationFilter):

    def __init__(self):
        super().__init__()


class Besluit(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'Besluit'
    # expand_param = 'Zaak, Stemming'

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
    def soort(self):
        return self.get_property_or_empty_string('Soort')

    @property
    def status(self):
        return self.get_property_or_empty_string('Status')
