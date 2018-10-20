import tkapi

from tkapi.actor import Actor
from tkapi.actor import FractieLid

from tkapi.actor import ActorFilter


class Persoon(Actor):
    url = 'Persoon'
    orderby_param = 'Achternaam'
    filter_param = 'Achternaam ne null'

    @property
    def fracties(self):
        return [lid.fractie for lid in self.fractieleden]

    @property
    def fractieleden(self):
        return self.related_items(FractieLid, item_key='Fractielid')

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
    def reizen(self):
        return self.related_items(PersoonReis, item_key='Reis')

    @property
    def onderwijs(self):
        return self.related_items(PersoonOnderwijs, item_key='Onderwijs')

    @property
    def functies(self):
        return self.related_items(PersoonFunctie, item_key='Functie')

    @property
    def loopbaan(self):
        return self.related_items(PersoonLoopbaan, item_key='Loopbaan')

    @property
    def geschenken(self):
        return self.related_items(PersoonGeschenk, item_key='PersoonGeschenk')

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


class PersoonReis(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'PersoonReis'

    @staticmethod
    def create_filter():
        return ActorFilter()

    @property
    def persoon(self):
        return self.related_item(Persoon)

    @property
    def doel(self):
        return self.get_property_or_empty_string('Doel')

    @property
    def bestemming(self):
        return self.get_property_or_empty_string('Bestemming')

    @property
    def van(self):
        return self.get_date_or_none('Van')

    @property
    def tot_en_met(self):
        return self.get_date_or_none('TotEnMet')

    @property
    def betaald_door(self):
        return self.get_property_or_empty_string('BetaaldDoor')


class PersoonOnderwijs(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'PersoonOnderwijs'

    @staticmethod
    def create_filter():
        return ActorFilter()

    @property
    def persoon(self):
        return self.related_item(Persoon)

    @property
    def opleiding_nl(self):
        return self.get_property_or_empty_string('OpleidingNl')

    @property
    def opleiding_en(self):
        return self.get_property_or_empty_string('OpleidingEn')

    @property
    def instelling(self):
        return self.get_property_or_empty_string('Instelling')

    @property
    def plaats(self):
        return self.get_property_or_empty_string('Plaats')

    @property
    def van(self):
        return self.get_year_or_none('Van')

    @property
    def tot_en_met(self):
        return self.get_year_or_none('TotEnMet')


class PersoonFunctie(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'PersoonFunctie'

    @staticmethod
    def create_filter():
        return ActorFilter()

    @property
    def persoon(self):
        return self.related_item(Persoon)

    @property
    def omschrijving(self):
        return self.get_property_or_empty_string('Waarde')


class PersoonLoopbaan(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'PersoonLoopbaan'

    @staticmethod
    def create_filter():
        return ActorFilter()

    @property
    def persoon(self):
        return self.related_item(Persoon)

    @property
    def functie(self):
        return self.get_property_or_empty_string('Functie')

    @property
    def werkgever(self):
        return self.get_property_or_empty_string('Werkgever')

    @property
    def omschrijving(self):
        return self.get_property_or_empty_string('OmschrijvingNl')

    @property
    def omschrijving_en(self):
        return self.get_property_or_empty_string('OmschrijvingEn')

    @property
    def plaats(self):
        return self.get_property_or_empty_string('Plaats')

    @property
    def van(self):
        return self.get_year_or_none('Van')

    @property
    def tot_en_met(self):
        return self.get_year_or_none('TotEnMet')


class PersoonGeschenk(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'PersoonGeschenk'

    @staticmethod
    def create_filter():
        return ActorFilter()

    @property
    def persoon(self):
        return self.related_item(Persoon)

    @property
    def omschrijving(self):
        return self.get_property_or_empty_string('Omschrijving')

    @property
    def datum(self):
        return self.get_datetime_or_none('Datum')
