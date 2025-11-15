from enum import Enum
from typing import List

from tkapi.core import TKItem
from tkapi.filter import Filter
from tkapi.filter import SoortFilter
from tkapi.filter import ZaakRelationFilter
from tkapi.persoon import Persoon
from tkapi.fractie import Fractie
from tkapi.commissie import Commissie
from tkapi.document import Document
from tkapi.commissie import VoortouwCommissie


class ActiviteitSoort(Enum):
    AANBIEDING = 'Aanbieding'
    AFSCHEID = 'Afscheid'
    ALGEMEEN_OVERLEG = 'Algemeen overleg'
    BEEDIGING = 'Beëdiging'
    BEGROTINGSOVERLEG = 'Begrotingsoverleg'
    BIJZONDERE_PROCEDURE = 'Bijzondere procedure'
    COMMISSIEDEBAT = 'Commissiedebat'
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
    PLENAIR_DEBAT_2MIN = 'Plenair debat (tweeminutendebat)'
    PLENAIR_DEBAT_DEBAT = 'Plenair debat (debat)'
    PLENAIR_DEBAT_INITIATIEF_WETGEVING = 'Plenair debat (initiatiefwetgeving)'
    PLENAIR_DEBAT_OVERIG = 'Plenair debat (overig)'
    PLENAIR_DEBAT_WETGEVING = 'Plenair debat (wetgeving)'
    PROCEDUREVERGADERING = 'Procedurevergadering'
    REGELING_VAN_WERKZAAMHEDEN = 'Regeling van werkzaamheden'
    STRATEGISCHE_PROCEDUREVERGADERING = 'Strategische procedurevergadering'
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


class ActiviteitFilter(SoortFilter, ZaakRelationFilter):

    def __init__(self):
        super().__init__()


class Activiteit(TKItem):
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
    def documenten(self) -> List[Document]:
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
    def voortouwcommissies(self) -> VoortouwCommissie:
        return self.related_items(VoortouwCommissie)

    @property
    def reservering(self):
        return self.related_item(Reservering)

    @property
    def zaal(self):
        return self.reservering.zaal

    @property
    def onderwerp(self):
        return self.get_property_or_empty_string('Onderwerp')

    @property
    def status(self) -> ActiviteitStatus:
        return self.get_property_enum_or_none('Status', ActiviteitStatus)

    @property
    def actors(self):
        return self.related_items(ActiviteitActor)

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


class StatusCode(Enum):
    R2 = 'R2'
    R3 = 'R3'


class StatusNaam(Enum):
    USR_ADMINISTRATIVELY_COMPLETED = 'UsrAdministrativelyCompleted'
    USR_MADE = 'UsrMade'


class Reservering(TKItem):
    type = 'Reservering'

    @staticmethod
    def create_filter() -> Filter:
        return Filter()

    @property
    def activiteit(self) -> Activiteit:
        return self.related_item(Activiteit)

    @property
    def zaal(self):
        return self.related_item(Zaal)

    @property
    def activiteit_nummer(self):
        return self.get_property_or_empty_string('ActiviteitNummer')

    @property
    def nummer(self):
        return self.get_property_or_empty_string('Nummer')

    @property
    def status_code(self) -> StatusCode:
        return self.get_property_enum_or_none('StatusCode', StatusCode)

    @property
    def status_naam(self) -> StatusNaam:
        return self.get_property_enum_or_none('StatusNaam', StatusNaam)


class Zaal(TKItem):
    type = 'Zaal'

    @staticmethod
    def create_filter() -> Filter:
        return Filter()

    @property
    def reservering(self) -> Reservering:
        return self.related_item(Reservering)

    @property
    def activiteit(self) -> Activiteit:
        return self.reservering.activiteit

    @property
    def naam(self):
        return self.get_property_or_empty_string('Naam')


class ActiviteitRelatieSoort(Enum):
    AANVRAGER = 'Aanvrager'
    AFGEMELD = 'Afgemeld'
    BEWINDSPERSOON = 'Bewindspersoon c.a.'
    DEELNEMENDE_FRACTIE = 'Deelnemende fractie'
    DEELNEMER = 'Deelnemer'
    INITIATIEFNEMER = 'Initiatiefnemer'
    INTERPELLANT = 'Interpellant'
    VOLGCOMMISSIE = 'Volgcommissie'


class ActiviteitActor(TKItem):
    type = 'ActiviteitActor'

    @staticmethod
    def create_filter() -> Filter:
        return Filter()

    @property
    def activiteit(self) -> Activiteit:
        return self.related_item(Activiteit)

    @property
    def persoon(self) -> Persoon:
        return self.related_item(Persoon)

    @property
    def fractie(self) -> Fractie:
        return self.related_item(Fractie)

    @property
    def commissie(self) -> Commissie:
        return self.related_item(Commissie)

    @property
    def naam(self):
        return self.get_property_or_empty_string('ActorNaam')

    @property
    def fractie_naam(self):
        return self.get_property_or_empty_string('ActorFractie')

    @property
    def functie(self):
        return self.get_property_or_empty_string('Functie')

    @property
    def spreektijd(self):
        return self.get_property_or_empty_string('Spreektijd')

    @property
    def volgorde(self):
        return self.get_property_or_none('Volgorde')

    @property
    def relatie(self) -> ActiviteitRelatieSoort:
        return self.get_property_enum_or_none('Relatie', ActiviteitRelatieSoort)
