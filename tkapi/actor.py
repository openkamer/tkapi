import tkapi


class ActorFilter(tkapi.Filter):

    def __init__(self):
        super().__init__()


class Actor(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'Actor'

    @staticmethod
    def create_filter():
        return ActorFilter()

    @property
    def zaken(self):
        from tkapi.zaak import Zaak
        return self.related_items(Zaak)

    @property
    def parlementaire_documenten(self):
        from tkapi.document import ParlementairDocument
        return self.related_items(ParlementairDocument)

    @property
    def stemming(self):
        from tkapi.stemming import Stemming
        return self.related_item(Stemming)


class FractieFilter(ActorFilter):

    def filter_actief(self):
        self.filters.append("DatumInactief eq null")
        self.filters.append("DatumActief ne null")


class Fractie(Actor):
    url = 'Fractie'
    # expand_param = 'ZaakActorPersoon'
    # expand_param = 'Lid'

    @staticmethod
    def create_filter():
        return FractieFilter()

    @property
    def leden(self):
        return self.related_items(Lid)

    @property
    def leden_actief(self):
        filter = Lid.create_filter()
        filter.filter_actief()
        return self.related_items(Lid, filter=filter)

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


class LidFilter(ActorFilter):

    def filter_actief(self):
        self.filters.append("TotEnMet eq null")
        self.filters.append("Verwijderd eq false")


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


class FractieLid(Lid):
    url = 'FractieLid'

    @property
    def fractie(self):
        return self.related_item(Fractie)


class FractieOrganisatie(Lid):
    url = 'FractieOrganisatie'

    @property
    def fractie(self):
        return self.related_item(Fractie)

    @property
    def naam(self):
        return self.get_property_or_empty_string('Waarde')
