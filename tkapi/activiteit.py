from enum import Enum

import tkapi


class ActiviteitFilter(tkapi.SoortFilter, tkapi.ZaakRelationFilter):

    def __init__(self):
        super().__init__()

    def _filter_kamerstukdossier_str(self, numer):
        filter_str = super()._filter_kamerstukdossier_str(numer=numer)
        filter_str += ' or '
        filter_str += 'Agendapunt/any(a: a/Zaak/any(z: z/Kamerstukdossier/any(d: d/Nummer eq {})))'.format(numer)
        return filter_str

    def filter_kamerstukdossier(self, nummer):
        filter_str = self._filter_kamerstukdossier_str(numer=nummer)
        self.add_filter_str(filter_str)

    def filter_kamerstuk(self, nummer, ondernummer, is_or=False):
        filter_str = super()._filter_kamerstukdossier_str(numer=nummer)
        filter_str += ' and '
        filter_str += super()._filter_kamerstuk_str(ondernummer=ondernummer)
        filter_str += ' or '
        filter_str += 'Agendapunt/any(a: a/Zaak/any(z: z/Kamerstukdossier/any(d: d/Nummer eq {})))'.format(nummer)
        filter_str += ' and '
        filter_str += 'Agendapunt/any(a: a/Zaak/any(z: z/Volgnummer eq {}))'.format(ondernummer)
        self.add_filter_str(filter_str)


class Activiteit(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'Activiteit'

    @staticmethod
    def create_filter():
        return ActiviteitFilter()

    @property
    def documenten(self):
        from tkapi.document import Document
        return self.related_items(Document)

    @property
    def zaken(self):
        from tkapi.zaak import Zaak
        return self.related_items(Zaak)

    @property
    def agendapunten(self):
        from tkapi.agendapunt import Agendapunt
        return self.related_items(Agendapunt)

    @property
    def voortouwcommissies(self):
        from tkapi.commissie import VoortouwCommissie
        return self.related_items(VoortouwCommissie)

    @property
    def onderwerp(self):
        return self.get_property_or_empty_string('Onderwerp')

    @property
    def begin(self):
        return self.get_datetime_or_none('Aanvangstijd')

    @property
    def einde(self):
        return self.get_datetime_or_none('Eindtijd')

    @property
    def soort(self):
        return self.get_property_or_empty_string('Soort')

    @property
    def nummer(self):
        return self.get_property_or_empty_string('Nummer')

    @staticmethod
    def begin_date_key():
        return 'Aanvangstijd'

    @staticmethod
    def end_date_key():
        return 'Eindtijd'


class ActiviteitSoort(Enum):
    AANBIEDING = 'Aanbieding'
    AFSCHEID = 'Afscheid'
    ALGEMEEN_OVERLEG = 'Algemeen overleg'
    BEEDIGING = 'Beëdiging'
    BEGROTINGSOVERLEG = 'Begrotingsoverleg'
    BIJZONDERE_PROCEDURE = 'Bijzondere procedure'
    CONSTITUERENDE_VERGADERING = 'Constituerende vergadering'
    DELEGATIEVERGADERING = 'Delegatievergadering'
    EMAILPROCEDURE = 'E-mailprocedure'
    GESPREK = 'Gesprek'
    HAMERSTUKKEN = 'Hamerstukken'
    HERDENKING = 'Herdenking'
    HOORZITTING = 'Hoorzitting'
    HOORZITTING_RONDETAFELGESPREK = 'Hoorzitting / rondetafelgesprek'
    INBRENG_FEITELIJKE_VRAGEN = 'Inbreng feitelijke vragen'
    INBRENG_SCHRIFTELIJK_OVERLEG = 'Inbreng schriftelijk overleg'
    INTERPELLATIEDEBAT = 'Interpellatiedebat'
    MEDEDELINGEN = 'Mededelingen'
    NOTAOVERLEG = 'Notaoverleg'
    ONTBIJTBIJEENKOMST_PARLEMENT_WETENSCHAP = 'Ontbijtbijeenkomst Parlement en Wetenschap'
    OPENING = 'Opening'
    OVERIG = 'Overig'
    PETITIE = 'Petitie'
    PLENAIR_DEBAT = 'Plenair debat'
    PROCEDUREVERGADERING = 'Procedurevergadering'
    REGELING_VAN_WERKZAAMHEDEN = 'Regeling van werkzaamheden'
    RONDETAFELGESPREK = 'Rondetafelgesprek'
    SCHRIFTELIJK_COMMENTAAR_ALGEMEEN = 'Schriftelijk commentaar algemeen'
    SCHRIFTELIJK_COMMENTAAR_GERICHT = 'Schriftelijk commentaar gericht'
    SLUITING = 'Sluiting'
    STEMMINGEN = 'Stemmingen'
    TECHNISCHE_BRIEFING = 'Technische briefing'
    VERGADERING = 'Vergadering'
    VERKLARING = 'Verklaring'
    VRAGENUUR = 'Vragenuur'
    WERKBEZOEK = 'Werkbezoek'
    WETGEVINGSOVERLEG = 'Wetgevingsoverleg'
    WETSVOORSTEL_INBRENG_VERSLAG = 'Inbreng verslag (wetsvoorstel)'
