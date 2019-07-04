import tkapi

from tkapi.actor import Actor

from tkapi.fractie import FractieZetelPersoonRelationFilter, FractieZetel


class PersoonFilter(FractieZetelPersoonRelationFilter):

    def filter_achternaam(self, achternaam):
        filter_str = 'Achternaam eq \'{}\''.format(achternaam)
        self.add_filter_str(filter_str)


class Persoon(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'Persoon'
    orderby_param = 'Achternaam'
    filter_param = 'Achternaam ne null'

    @staticmethod
    def create_filter():
        return PersoonFilter()

    @property
    def fracties(self):
        return [lid.fractie for lid in self.fractieleden]

    @property
    def fractieleden(self):
        from .fractie import FractieZetelPersoon
        return self.related_items(FractieZetelPersoon)

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
    def functie(self):
        return self.get_property_or_empty_string('Functie')

    @property
    def geboorteland(self):
        return self.get_property_or_empty_string('Geboorteland')

    @property
    def geboorteplaats(self):
        return self.get_property_or_empty_string('Geboorteplaats')

    @property
    def geslacht(self):
        return self.get_property_or_empty_string('Geslacht')

    @property
    def geboortedatum(self):
        return self.get_date_from_datetime_or_none('Geboortedatum')

    @property
    def woonplaats(self):
        return self.get_property_or_empty_string('Woonplaats')

    @property
    def titels(self):
        return self.get_property_or_empty_string('Titels')

    @property
    def reizen(self):
        return self.related_items(PersoonReis)

    @property
    def onderwijs(self):
        return self.related_items(PersoonOnderwijs)

    @property
    def loopbaan(self):
        return self.related_items(PersoonLoopbaan)

    @property
    def geschenken(self):
        return self.related_items(PersoonGeschenk)

    @property
    def nevenfuncties(self):
        return self.related_items(PersoonNevenfunctie)

    def __str__(self):
        pretty_print = ''
        if self.roepnaam:
            pretty_print = str(self.roepnaam) + ' '
        pretty_print += str(self.achternaam) + ' '
        if self.initialen:
            pretty_print += '(' + str(self.initialen) + ')'
        return pretty_print


class PersoonEntity(tkapi.TKItemRelated, tkapi.TKItem):

    @property
    def persoon(self):
        return self.related_item(Persoon)


class PersoonReis(PersoonEntity):
    url = 'PersoonReis'

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

    @staticmethod
    def begin_date_key():
        return 'Van'

    @staticmethod
    def end_date_key():
        return 'TotEnMet'


class PersoonOnderwijs(PersoonEntity):
    url = 'PersoonOnderwijs'

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

    @staticmethod
    def begin_date_key():
        return 'Van'

    @staticmethod
    def end_date_key():
        return 'TotEnMet'


class PersoonLoopbaan(PersoonEntity):
    url = 'PersoonLoopbaan'

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
        return self.get_date_or_none('Van')

    @property
    def tot_en_met(self):
        return self.get_date_or_none('TotEnMet')

    @staticmethod
    def begin_date_key():
        return 'Van'

    @staticmethod
    def end_date_key():
        return 'TotEnMet'


class PersoonGeschenk(PersoonEntity):
    url = 'PersoonGeschenk'

    @property
    def omschrijving(self):
        return self.get_property_or_empty_string('Omschrijving')

    @property
    def datum(self):
        return self.get_datetime_or_none('Datum')

    @staticmethod
    def begin_date_key():
        return 'Datum'


class PersoonNevenfunctie(PersoonEntity):
    url = 'PersoonNevenfunctie'

    @property
    def inkomsten(self):
        return self.related_items(PersoonNevenfunctieInkomsten)

    @property
    def omschrijving(self):
        return self.get_property_or_empty_string('Omschrijving')

    @property
    def van(self):
        return self.get_datetime_or_none('PeriodeVan')

    @property
    def tot_en_met(self):
        return self.get_datetime_or_none('PeriodeTotEnMet')

    @staticmethod
    def begin_date_key():
        return 'PeriodeVan'

    @staticmethod
    def end_date_key():
        return 'PeriodeTotEnMet'

    @property
    def is_actief(self):
        return self.get_property_or_none('IsActief')

    @property
    def soort(self):
        return self.get_property_or_empty_string('VergoedingSoort')

    @property
    def toelichting(self):
        return self.get_property_or_empty_string('VergoedingToelichting')


class PersoonNevenfunctieInkomsten(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'PersoonNevenfunctieInkomsten'

    @property
    def nevenfunctie(self):
        return self.related_item(PersoonNevenfunctie)

    @property
    def omschrijving(self):
        return self.get_property_or_empty_string('Omschrijving')

    @property
    def datum(self):
        return self.get_datetime_or_none('Datum')

    @staticmethod
    def begin_date_key():
        return 'Datum'
