import tkapi


class StemmingFilter(tkapi.SoortFilter):

    def __init__(self):
        super().__init__()


class Stemming(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'Stemming'
    # expand_param = 'Besluit'

    @staticmethod
    def create_filter():
        return StemmingFilter()

    @property
    def besluit(self):
        from tkapi.besluit import Besluit
        return self.related_item(Besluit)

    @property
    def zaken(self):
        from tkapi.zaak import Zaak
        return self.related_items(Zaak)

    @property
    def soort(self):
        return self.get_property_or_empty_string('Soort')

    @property
    def vergissing(self):
        return self.get_property_or_none('Vergissing')

    @property
    def fractie_size(self):
        return self.get_property_or_none('fractieGrootte')
