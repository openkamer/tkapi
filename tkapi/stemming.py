import tkapi


class StemmingFilter(tkapi.SoortFilter):

    def __init__(self):
        super().__init__()

    def filter_kamerstuk(self, dossier_nr, ondernummer):
        filter_str = 'Besluit/Zaak/any(z: z/Volgnummer eq {} and z/Kamerstukdossier/any(d: d/Vetnummer eq {}))'.format(ondernummer, dossier_nr)
        self.filters.append(filter_str)


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
    def fractie(self):
        from tkapi.actor import Fractie
        return self.related_item(Fractie)

    @property
    def soort(self):
        return self.get_property_or_empty_string('Soort')

    @property
    def vergissing(self):
        return self.get_property_or_none('Vergissing')

    @property
    def fractie_size(self):
        return self.get_property_or_none('fractieGrootte')
