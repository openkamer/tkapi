import tkapi


class ActorFilter(tkapi.Filter):

    def __init__(self):
        super().__init__()


class Actor(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'Actor'
    expand_param = ''

    def __init__(self, stemming_json):
        super().__init__(stemming_json)

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


class Fractie(Actor):
    url = 'Fractie'
    # expand_param = 'ZaakActorPersoon'
    # expand_param = 'Lid'

    def __init__(self, stemming_json):
        super().__init__(stemming_json)

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
    def leden(self):
        return self.related_items(Lid)

    @property
    def datum_actief(self):
        return self.get_date_or_none('DatumActief')

    @property
    def datum_inactief(self):
        return self.get_date_or_none('DatumInactief')


class Persoon(Actor):
    url = 'Persoon'
    expand_param = 'Fractielid/Fractie'
    orderby_param = 'Achternaam'
    filter_param = 'Achternaam ne null'

    def __init__(self, persoon_json):
        super().__init__(persoon_json)

    @property
    def fracties(self):
        return [lid.fractie for lid in self.fractieleden]

    @property
    def fractieleden(self):
        # we cannot use related_items() here because the type (FractieLid) is different from the key (Fractielid)
        fractieleden = []
        for lid_json in self.json['Fractielid']:
            fractieleden.append(FractieLid(lid_json))
        return fractieleden

    @property
    def achternaam(self):
        return self.get_property_or_empty_string('Achternaam')

    @property
    def initialen(self):
        return self.get_property_or_empty_string('Initialen')

    @property
    def roepnaam(self):
        return self.get_property_or_empty_string('Roepnaam')

    @property
    def voornamen(self):
        return self.get_property_or_empty_string('Voornamen')

    @property
    def geboortedatum(self):
        return self.get_property_or_empty_string('Geboortedatum')

    def __str__(self):
        pretty_print = ''
        if self.roepnaam:
            pretty_print = str(self.roepnaam) + ' '
        pretty_print += str(self.achternaam) + ' '
        if self.initialen:
            pretty_print += '(' + str(self.initialen) + ')'
        return pretty_print


class FractieLid(Actor):
    url = 'FractieLid'

    def __init__(self, json):
        super().__init__(json)

    @property
    def fractie(self):
        return self.related_item(Fractie)


class Lid(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'Lid'

    def __init__(self, json):
        super().__init__(json)

    @property
    def persoon(self):
        return self.related_item(Persoon)

    @property
    def van(self):
        return self.get_date_or_none('Van')

    @property
    def tot_en_met(self):
        return self.get_date_or_none('TotEnMet')
