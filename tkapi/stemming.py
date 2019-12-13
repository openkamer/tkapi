from tkapi.core import TKItem
from tkapi.filter import ZaakRelationFilter

from tkapi.persoon import Persoon
from tkapi.fractie import Fractie


class StemmingFilter(ZaakRelationFilter):

    @property
    def zaak_related_url(self):
        return 'Besluit/Zaak'

    def filter_fractie(self, fractie_id):
        filter_str = "Fractie_Id eq {}".format(fractie_id)
        self._filters.append(filter_str)

    def filter_persoon(self, persoon_id):
        filter_str = "Persoon_id eq {}".format(persoon_id)
        self._filters.append(filter_str)

    def filter_persoon_stemmingen(self):
        filter_str = "Persoon_id ne null"
        self._filters.append(filter_str)

    def filter_fractie_stemmingen(self):
        filter_str = "Fractie_Id ne null"
        self._filters.append(filter_str)


class Stemming(TKItem):
    type = 'Stemming'

    @staticmethod
    def create_filter():
        return StemmingFilter()

    @property
    def besluit(self):
        from tkapi.besluit import Besluit
        return self.related_item(Besluit)

    @property
    def fractie(self) -> Fractie:
        return self.related_item(Fractie)

    @property
    def persoon(self) -> Persoon:
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
    def persoon_id(self):
        return self.get_property_or_none('Persoon_Id')

    @property
    def fractie_id(self):
        return self.get_property_or_none('Fractie_Id')

    @property
    def is_hoofdelijk(self):
        return 'hoofdelijk' in self.besluit.tekst.lower()
