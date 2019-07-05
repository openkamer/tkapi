import tkapi


class StemmingFilter(tkapi.ZaakRelationFilter):

    @property
    def zaak_related_url(self):
        return 'Besluit/Zaak'


class Stemming(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'Stemming'

    @staticmethod
    def create_filter():
        return StemmingFilter()

    @property
    def besluit(self):
        from tkapi.besluit import Besluit
        return self.related_item(Besluit)

    @property
    def fractie(self):
        from tkapi.fractie import Fractie
        return self.related_item(Fractie)

    @property
    def persoon(self):
        from tkapi.persoon import Persoon
        return self.related_item(Persoon)

    @property
    def soort(self):
        return self.get_property_or_empty_string('Soort')

    @property
    def vergissing(self):
        return self.get_property_or_none('Vergissing')

    @property
    def fractie_size(self):
        return self.get_property_or_none('FractieGrootte')

    @property
    def actor_naam(self):
        return self.get_property_or_none('ActorNaam')

    @property
    def actor_fractie(self):
        return self.get_property_or_none('ActorFractie')

    @property
    def is_hoofdelijk(self):
        return 'hoofdelijk' in self.besluit.tekst.lower()
