import tkapi


class StemmingFilter(tkapi.SoortFilter):

    def __init__(self):
        super().__init__()


class Stemming(tkapi.TKItem):
    url = 'Stemming'
    expand_param = 'Besluit, Persoon, Fractie'

    def __init__(self, stemming_json):
        super().__init__(stemming_json)

    @property
    def soort(self):
        return self.get_property_or_empty_string('Soort')

    @property
    def vergissing(self):
        return self.json['Vergissing']

    @property
    def fractie_size(self):
        return self.get_property_or_none('fractieGrootte')

    @property
    def besluit(self):
        from tkapi.besluit import Besluit
        return tkapi.api.get_item(Besluit, self.json['Besluit']['Id'])

    # @property
    # def zaak(self):
    #     from tkapi.zaak import Zaak
    #     return tkapi.api.get_item(Zaak, self.json['Zaak']['Id'])