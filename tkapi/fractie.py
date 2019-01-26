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
        filter = FractieZetel.create_filter()
        filter.filter_actief()
        return self.related_items(FractieZetel, filter=filter, item_key='Lid')

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

    @staticmethod
    def begin_date_key():
        return 'DatumActief'

    @staticmethod
    def end_date_key():
        return 'DatumInactief'

    def __str__(self):
        return '{} ({}) ({} zetels)'.format(self.naam, self.afkorting, self.zetels)


class Lid(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'Lid'

    @staticmethod
    def create_filter():
        return FractieZetelPersoonFilter()

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

    @staticmethod
    def begin_date_key():
        return 'Van'

    @staticmethod
    def end_date_key():
        return 'TotEnMet'


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


class FractieZetelPersoonFilter(tkapi.Filter):

    def filter_actief(self):
        self._filters.append("TotEnMet eq null")
        self._filters.append("Verwijderd eq false")


class FractieZetelRelationFilter(tkapi.RelationFilter):

    @property
    def related_url(self):
        return 'FractieZetel'

    def filter_is_fractiezetel(self):
        self._filter_non_empty()


class FractieZetel(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'FractieZetel'

    @property
    def fractie(self):
        return self.related_item(Fractie)

    @property
    def fractie_zetel_persoon(self):
        return self.related_item(FractieZetelPersoon)

    @property
    def persoon(self):
        return self.fractie_zetel_persoon.persoon


class FractieZetelPersoon(Lid):
    url = 'FractieZetelPersoon'

    @property
    def fractie_zetel(self):
        return self.related_item(FractieZetel)
