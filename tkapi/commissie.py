from enum import Enum

import tkapi


class CommissieFunctie(Enum):
    VOORZITTER = 'Voorzitter'
    ONDERVOORZITTER = 'Ondervoorzitter'
    FNG_ONDERVOORZITTER = 'Fng ondervoorzitter'
    LID = 'Lid'
    PLAATSVERVANGEND_LID = 'Plv. lid'
    VERVANGER_AMBTELIJK_LID = 'Vervanger (ambtelijk lid)'
    EERSTE_ONDERVOORZITTER_TK = 'Eerste ondervoorzitter Tweede Kamer'


class CommissieFilter(tkapi.SoortFilter):

    def filter_naam(self, naam):
        filter_str = "NaamNL eq " + "'" + naam.replace("'", "''") + "'"
        self._filters.append(filter_str)


class CommissieZetelFilter(tkapi.Filter):

    def filter_commissie(self, commissie):
        filter_str = "Commissie_Id eq {}".format(commissie.id)
        self._filters.append(filter_str)

    def filter_active(self):
        """Filters CommissieZetels with at least one active CommissieZetelPersoon."""
        filter_str = "(CommissieZetelVastPersoon/any(p:p/TotEnMet eq null) or CommissieZetelVervangerPersoon/any(p:p/TotEnMet eq null))"
        self._filters.append(filter_str)


class CommissieZetelPersoonFilter(tkapi.Filter):

    def filter_active(self):
        filter_str = "{} eq null".format(CommissieZetelPersoon.end_date_key())
        self._filters.append(filter_str)

    def filter_commissie(self, commissie):
        filter_str = "CommissieZetel/Commissie/Id eq {}".format(commissie.id)
        self._filters.append(filter_str)

    def filter_functie(self, functie: CommissieFunctie):
        filter_str = "Functie eq '{}'".format(functie.value)
        self._filters.append(filter_str)


class Commissie(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'Commissie'

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


class VoortouwCommissie(Commissie):
    url = 'Voortouwcommissie'


class CommissieZetel(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'CommissieZetel'

    @staticmethod
    def create_filter():
        return CommissieZetelFilter()

    @property
    def personen_vast(self):
        return self.related_items(CommissieZetelVastPersoon)

    @property
    def personen_vast_active(self):
        filter = tkapi.Filter()
        filter.add_filter_str('{} eq null'.format(CommissieZetelPersoon.end_date_key()))
        return self.related_items(CommissieZetelVastPersoon, filter=filter)

    @property
    def personen_vervangend(self):
        return self.related_items(CommissieZetelVervangerPersoon)

    @property
    def personen_vervangend_active(self):
        filter = tkapi.Filter()
        filter.add_filter_str('{} eq null'.format(CommissieZetelPersoon.end_date_key()))
        return self.related_items(CommissieZetelVervangerPersoon, filter=filter)

    @property
    def commissie(self):
        return self.related_item(Commissie)


class CommissieZetelPersoon(tkapi.TKItemRelated, tkapi.TKItem):

    @staticmethod
    def create_filter():
        return CommissieZetelPersoonFilter()

    @property
    def persoon(self):
        from tkapi.persoon import Persoon
        return self.related_item(Persoon)

    @property
    def zetel(self):
        return self.related_item(CommissieZetel)

    @property
    def functie(self):
        return self.get_property_enum_or_none('Functie', CommissieFunctie)

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


class CommissieZetelVastPersoon(CommissieZetelPersoon):
    url = 'CommissieZetelVastPersoon'


class CommissieZetelVervangerPersoon(CommissieZetelPersoon):
    url = 'CommissieZetelVervangerPersoon'
