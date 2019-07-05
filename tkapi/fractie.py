import tkapi
from tkapi.actor import Actor


class Fractie(Actor):
    url = 'Fractie'

    @staticmethod
    def create_filter():
        return FractieFilter()

    @property
    def leden(self):
        leden = []
        for zetel in self.zetels:
            leden.append(zetel.fractie_zetel_persoon)
        return leden

    @property
    def zetels(self):
        return self.related_items(FractieZetel)

    @property
    def leden_actief(self):
        filter = FractieZetelPersoon.create_filter()
        filter.filter_fractie_id(uid=self.id)
        filter.filter_actief()
        return self.related_items_deep(FractieZetelPersoon, filter=filter)

    @property
    def naam(self):
        return self.get_property_or_empty_string('NaamNL')

    @property
    def afkorting(self):
        return self.get_property_or_empty_string('Afkorting')

    @property
    def zetels_aantal(self):
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
        return '{} ({}) ({} zetels)'.format(self.naam, self.afkorting, self.zetels_aantal)


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

    @staticmethod
    def begin_date_key():
        return 'Van'

    @staticmethod
    def end_date_key():
        return 'TotEnMet'


class LidFilter(tkapi.Filter):

    def filter_actief(self):
        self._filters.append("TotEnMet eq null")
        self._filters.append("Verwijderd eq false")


class FractieFilter(tkapi.Filter):

    def filter_fractie(self, naam):
        self._filters.append("NaamNL eq '{}'".format(naam))

    def filter_fractie_id(self, uid):
        self._filters.append("Id eq {}".format(uid))

    def filter_actief(self):
        self._filters.append("DatumInactief eq null")
        self._filters.append("DatumActief ne null")


class FractieZetelPersoonFilter(LidFilter):

    def filter_fractie(self, naam):
        self._filters.append("FractieZetel/Fractie/NaamNL eq '{}'".format(naam))

    def filter_fractie_id(self, uid):
        self._filters.append("FractieZetel/Fractie/Id eq {}".format(uid))

    def filter_actief(self):
        self._filters.append("TotEnMet eq null")
        self._filters.append("Verwijderd eq false")


class FractieZetelFilter(tkapi.Filter):

    def filter_fractie(self, naam):
        self._filters.append("Fractie/NaamNL eq '{}'".format(naam))

    def filter_fractie_id(self, uid):
        self._filters.append("Fractie/Id eq {}".format(uid))


class FractieZetelPersoonRelationFilter(tkapi.RelationsFilter):

    @property
    def related_url(self):
        return 'FractieZetelPersoon'

    def filter_is_fractiezetel(self):
        self._filter_non_empty()


class FractieZetel(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'FractieZetel'

    @staticmethod
    def create_filter():
        return FractieZetelFilter()

    @property
    def fractie(self):
        return self.related_item(Fractie)

    @property
    def fractie_zetel_persoon(self):
        return self.related_item(FractieZetelPersoon)

    @property
    def persoon(self):
        return self.fractie_zetel_persoon.persoon

    @property
    def gewicht(self):
        return self.get_property_or_empty_string('Gewicht')


class FractieZetelPersoon(Lid):
    url = 'FractieZetelPersoon'

    @staticmethod
    def create_filter():
        return FractieZetelPersoonFilter()

    @property
    def fractie_zetel(self):
        return self.related_item(FractieZetel)

    @property
    def fractie(self):
        return self.fractie_zetel.fractie
