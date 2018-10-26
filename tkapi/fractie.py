import tkapi
from tkapi.actor import Actor


class Fractie(Actor):
    url = 'Fractie'

    @staticmethod
    def create_filter():
        return FractieFilter()

    @property
    def leden(self):
        return self.related_items(Lid)

    @property
    def leden_actief(self):
        filter = FractieLid.create_filter()
        filter.filter_actief()
        return self.related_items(FractieLid, filter=filter, item_key='Lid')

    @property
    def naam(self):
        return self.get_property_or_empty_string('NaamNL')

    @property
    def afkorting(self):
        return self.get_property_or_empty_string('Afkorting')

    @property
    def zetels(self):
        return self.get_property_or_none('AantalZetels')

    @property
    def datum_actief(self):
        return self.get_date_from_datetime_or_none('DatumActief')

    @property
    def datum_inactief(self):
        return self.get_date_from_datetime_or_none('DatumInactief')

    @property
    def organisatie(self):
        return self.related_item('Organisatie')

    def __str__(self):
        return '{} ({}) ({} zetels)'.format(self.naam, self.afkorting, self.zetels)


class Lid(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'Lid'

    @staticmethod
    def create_filter():
        return LidFilter()

    @property
    def persoon(self):
        from tkapi.persoon import Persoon
        return self.related_item(Persoon)

    @property
    def is_actief(self):
        return self.tot_en_met is None

    @property
    def van(self):
        return self.get_date_from_datetime_or_none('Van')

    @property
    def tot_en_met(self):
        return self.get_date_from_datetime_or_none('TotEnMet')


class FractieOrganisatie(Lid):
    url = 'FractieOrganisatie'

    @property
    def fractie(self):
        return self.related_item(Fractie)

    @property
    def naam(self):
        return self.get_property_or_empty_string('Waarde')


class FractieFilter(tkapi.Filter):

    def filter_actief(self):
        self._filters.append("DatumInactief eq null")
        self._filters.append("DatumActief ne null")


class LidFilter(tkapi.Filter):

    def filter_actief(self):
        self._filters.append("TotEnMet eq null")
        self._filters.append("Verwijderd eq false")


class FractieLidRelationFilter(tkapi.RelationFilter):

    @property
    def related_url(self):
        return 'Fractielid'

    def filter_is_fractielid(self):
        self._filter_non_empty()


class FractieLid(Lid):
    url = 'FractieLid'

    @property
    def fractie(self):
        return self.related_item(Fractie)