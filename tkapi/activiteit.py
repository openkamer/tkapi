from enum import Enum

import tkapi


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


class ActiviteitStatus(Enum):
    GEANNULEERD = 'Geannuleerd'
    GEPLAND = 'Gepland'
    UITGEVOERD = 'Uitgevoerd'
    VERPLAATS = 'Verplaatst'


class DatumSoort(Enum):
    DAG = 'Dag'
    MEERDAAGS = 'Meerdaags'
    ONBEKEND = 'Nog geen datum bekend'
    WEEKNUMMER = 'Weeknummer'


class ActiviteitFilter(tkapi.SoortFilter, tkapi.ZaakRelationFilter):

    def __init__(self):
        super().__init__()


class Activiteit(tkapi.TKItem):
    type = 'Activiteit'

    @staticmethod
    def create_filter() -> ActiviteitFilter:
        return ActiviteitFilter()

    @staticmethod
    def begin_date_key():
        return 'Aanvangstijd'

    @staticmethod
    def end_date_key():
        return 'Eindtijd'

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
    def status(self) -> ActiviteitStatus:
        return self.get_property_enum_or_none('Status', ActiviteitStatus)

    @property
    def datum(self):
        return self.get_datetime_or_none('Datum')

    @property
    def datum_soort(self) -> DatumSoort:
        return self.get_property_enum_or_none('DatumSoort', DatumSoort)

    @property
    def begin(self):
        return self.get_datetime_or_none('Aanvangstijd')

    @property
    def einde(self):
        return self.get_datetime_or_none('Eindtijd')

    @property
    def soort(self) -> ActiviteitSoort:
        return self.get_property_enum_or_none('Soort', ActiviteitSoort)

    @property
    def nummer(self):
        return self.get_property_or_empty_string('Nummer')

    @property
    def vergaderjaar(self):
        return self.get_property_or_empty_string('Vergaderjaar')
