import tkapi
from tkapi.persoon import Persoon


class CommissieFilter(tkapi.SoortFilter):

    def filter_naam(self, naam):
        filter_str = "NaamNL eq " + "'" + naam.replace("'", "''") + "'"
        self.filters.append(filter_str)


class Commissie(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'Commissie'
    # expand_param = 'Organisatie'

    @staticmethod
    def create_filter():
        return CommissieFilter()

    @property
    def zetels(self):
        return self.related_items(CommissieZetel)

    @property
    def afkorting(self):
        return self.get_property_or_empty_string('Afkorting')

    @property
    def naam(self):
        return self.get_property_or_empty_string('NaamNL')

    @property
    def naam_web(self):
        return self.get_property_or_empty_string('NaamWebNL')

    @property
    def soort(self):
        return self.get_property_or_empty_string('Soort')

    @property
    def nummer(self):
        return self.get_property_or_empty_string('Nummer')

    def __str__(self):
        pretty_print = self.id + ': '
        pretty_print += self.naam
        if self.afkorting:
            pretty_print += ' (' + self.afkorting + ')'
        return pretty_print


class VoortouwCommissie(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'Voortouwcommissie'


class CommissieZetel(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'CommissieZetel'

    @property
    def personen_vast(self):
        return self.related_items(CommissieVastPersoon)

    @property
    def commissie(self):
        return self.related_item(Commissie)

    @property
    def vast_van(self):
        return self.get_date_from_datetime_or_none('VastVan')

    @property
    def vast_tot_en_met(self):
        return self.get_date_from_datetime_or_none('VastTotEnMet')


class CommissieVastPersoon(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'CommissieVastPersoon'

    @property
    def persoon(self):
        from tkapi.persoon import Persoon
        return self.related_item(Persoon)

    @property
    def zetel(self):
        return self.related_item(CommissieZetel)

    @property
    def functie(self):
        return self.get_property_or_empty_string('Functie')

    @property
    def van(self):
        return self.get_date_from_datetime_or_none('Van')

    @property
    def tot_en_met(self):
        return self.get_date_from_datetime_or_none('TotEnMet')
