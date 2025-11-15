from enum import Enum

from tkapi.core import TKItem
from tkapi.filter import Filter
from tkapi.persoon import Persoon


class Fractie(TKItem):
    type = 'Fractie'

    @staticmethod
    def create_filter():
        return FractieFilter()

    @property
    def zetels(self):
        return self.related_items(FractieZetel)

    @property
    def leden(self):
        leden = []
        for zetel in self.zetels:
            leden.append(zetel.fractie_zetel_persoon)
        return leden

    @property
    def leden_actief(self):
        filter = FractieZetelPersoon.create_filter()
        filter.filter_fractie_id(uid=self.id)
        filter.filter_actief()
        return self.related_items_deep(FractieZetelPersoon, filter=filter)

    @property
    def stemmingen(self):
        # WARNING: this may take long
        from tkapi.stemming import Stemming
        return self.related_items(Stemming)

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
        return self.get_property_or_empty_string('Organisatie')

    @staticmethod
    def begin_date_key():
        return 'DatumActief'

    @staticmethod
    def end_date_key():
        return 'DatumInactief'

    def __str__(self):
        return '{} ({}) ({} zetels)'.format(self.naam, self.afkorting, self.zetels_aantal)


class Lid(TKItem):
    type = 'Lid'
    expand_params = ['Persoon']

    @staticmethod
    def create_filter():
        return LidFilter()

    @property
    def persoon(self) -> Persoon:
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


class LidFilter(Filter):

    def filter_actief(self):
        self._filters.append("TotEnMet eq null")
        self._filters.append("Verwijderd eq false")


class FractieFilter(Filter):

    def filter_fractie(self, naam):
        self._filters.append("NaamNL eq '{}'".format(self.escape(naam)))

    def filter_fractie_id(self, uid):
        self._filters.append("Id eq {}".format(uid))

    def filter_actief(self):
        self._filters.append("DatumInactief eq null")
        self._filters.append("DatumActief ne null")


class FractieZetelPersoonFilter(LidFilter):

    def filter_fractie(self, naam):
        naam = self.escape(naam)
        self._filters.append("FractieZetel/Fractie/NaamNL eq '{}'".format(naam))

    def filter_fractie_id(self, uid):
        self._filters.append("FractieZetel/Fractie/Id eq {}".format(uid))

    def filter_actief(self):
        self._filters.append("TotEnMet eq null")
        self._filters.append("Verwijderd eq false")


class FractieZetelFilter(Filter):

    def filter_fractie(self, naam):
        naam = self.escape(naam)
        self._filters.append("Fractie/NaamNL eq '{}'".format(naam))

    def filter_fractie_id(self, uid):
        self._filters.append("Fractie/Id eq {}".format(uid))


class FractieZetel(TKItem):
    type = 'FractieZetel'

    @staticmethod
    def create_filter():
        return FractieZetelFilter()

    @property
    def fractie(self) -> Fractie:
        return self.related_item(Fractie)

    @property
    def fractie_zetel_persoon(self):
        return self.related_item(FractieZetelPersoon)

    @property
    def fractie_zetel_vacature(self):
        return self.related_items(FractieZetelVacature)

    @property
    def persoon(self):
        return self.fractie_zetel_persoon.persoon

    @property
    def gewicht(self):
        return self.get_property_or_empty_string('Gewicht')


class FractieZetelPersoon(Lid):
    type = 'FractieZetelPersoon'

    @staticmethod
    def create_filter():
        return FractieZetelPersoonFilter()

    @property
    def fractie_zetel(self) -> FractieZetel:
        return self.related_item(FractieZetel)

    @property
    def fractie(self) -> Fractie:
        return self.fractie_zetel.fractie


class FractieZetelVacatureSoort(Enum):
    LID = 'Lid'
    FRACTIEVOORZITTER = 'Fractievoorzitter'


class FractieZetelVacature(TKItem):
    type = 'FractieZetelVacature'

    @staticmethod
    def create_filter():
        return Filter()

    @property
    def fractie_zetel(self) -> FractieZetel:
        return self.related_item(FractieZetel)

    @property
    def fractie(self) -> Fractie:
        return self.fractie_zetel.fractie

    @property
    def functie(self) -> FractieZetelVacatureSoort:
        return self.get_property_enum_or_none('Functie', FractieZetelVacatureSoort)

    @property
    def van(self):
        return self.get_datetime_or_none('Van')

    @property
    def tot_en_met(self):
        return self.get_datetime_or_none('TotEnMet')
