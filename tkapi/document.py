from enum import Enum
import requests

from tkapi.core import TKItem
from tkapi.filter import Filter
from tkapi.filter import SoortFilter
from tkapi.filter import ZaakRelationFilter
from tkapi.util import util


class DocumentSoort(Enum):
    AANBIEDINGSBRIEF = 'Aanbiedingsbrief'
    AANHANGSEL_VAN_DE_HANDELINGEN = 'Aanhangsel van de Handelingen'
    ADVIES_AAN_PRESIDIUM = 'Advies aan Presidium'
    ADVIES_AFDELING_ADVISERING_RAAD_VAN_STATE = 'Advies Afdeling advisering Raad van State'
    ADVIES_AFDELING_ADVISERING_RAAD_VAN_STATE_EN_NADER_RAPPORT = 'Advies Afdeling advisering Raad van State en Nader rapport'
    ADVIES_AFDELING_ADVISERING_RAAD_VAN_STATE_EN_REACTIE_VAN_DE_INITIATIEFNEMERS = 'Advies Afdeling advisering Raad van State en Reactie van de initiatiefnemer(s)'
    ADVIES_COMMISSIE = 'Advies commissie'
    ADVIES_VAN_ANDERE_ADVIESORGANEN = 'Advies van andere adviesorganen'
    ADVIESAANVRAAG_AFDELING_ADVISERING_RAAD_VAN_STATE = 'Adviesaanvraag Afdeling advisering Raad van State'
    AGENDA_PLENAIRE_VERGADERING = 'Agenda plenaire vergadering'
    AGENDA_PROCEDUREVERGADERING = 'Agenda procedurevergadering'
    AGENDA_STRATEGISCHE_PROCEDUREVERGADERING = 'Agenda strategische procedurevergadering'
    AMENDEMENT = 'Amendement'
    AMENDEMENT_GEWIJZIGD = 'Amendement (gewijzigd/nader/vervangend)'
    ANTWOORD_SCHRIFTELIJKE_VRAGEN = 'Antwoord schriftelijke vragen'
    ANTWOORD_SCHRIFTELIJKE_VRAGEN_NADER = 'Antwoord schriftelijke vragen (nader)'
    BEGROTINGSTOELICHTING = 'Begrotingstoelichting'
    BESLUITENLIJST_PROCEDUREVERGADERING = 'Besluitenlijst procedurevergadering'
    BESLUITENLIJST_STRATEGISCHE_PROCEDUREVERGADERING = 'Besluitenlijst strategische procedurevergadering'
    BIJGEWERKTE_TEKST = 'Bijgewerkte tekst'
    BIJLAGE = 'Bijlage'
    BRIEF_AFDELING_ADVISERING_RAAD_VAN_STATE = 'Brief Afdeling advisering Raad van State'
    BRIEF_ALGEMENE_REKENKAMER = 'Brief Algemene Rekenkamer'
    BRIEF_COMMISSIE = 'Brief commissie'
    BRIEF_COMMISSIE_AAN_BEWINDSPERSOON = 'Brief commissie aan bewindspersoon'
    BRIEF_CTIVD = 'Brief CTIVD'
    BRIEF_EERSTE_KAMER = 'Brief Eerste Kamer'
    BRIEF_EUROPESE_COMMISSIE = 'Brief Europese Commissie'
    BRIEF_FORMATEUR = 'Brief formateur'
    BRIEF_INFORMATEUR = 'Brief informateur'
    BRIEF_KAMER = 'Brief Kamer'
    BRIEF_LID__FRACTIE = 'Brief lid / fractie'
    BRIEF_NATIONALE_OMBUDSMAN = 'Brief Nationale ombudsman'
    BRIEF_PRESIDENT_HOGE_RAAD = 'Brief president Hoge Raad'
    BRIEF_PRESIDIUM = 'Brief Presidium'
    BRIEF_REGERING = 'Brief regering'
    BRIEF_VERKENNER = 'Brief verkenner'
    BRIEF_VOORZITTER = 'Brief Voorzitter'
    CONVOCATIE_COMMISSIEACTIVITEIT = 'Convocatie commissieactiviteit'
    CONVOCATIE_INBRENG = 'Convocatie inbreng'
    EINDTEKST = 'Eindtekst'
    EU_VOORSTEL = 'EU-voorstel'
    GELEIDENDE_BRIEF = 'Geleidende brief'
    GROENBOEKWITBOEK = 'Groenboek/witboek'
    INBRENG_VERSLAG_SCHRIFTELIJK_OVERLEG = 'Inbreng verslag schriftelijk overleg'
    INITIATIEFNOTA = 'Initiatiefnota'
    INTERPELLATIEVRAGEN = 'Interpellatievragen'
    JAARVERSLAG = 'Jaarverslag'
    KONINKLIJKE_BOODSCHAP = 'Koninklijke boodschap'
    LIJST_MET_EU_VOORSTELLEN = 'Lijst met EU-voorstellen'
    LIJST_VAN_INGEKOMEN_STUKKEN = 'Lijst van ingekomen stukken'
    LIJST_VAN_VRAGEN = 'Lijst van vragen'
    LIJST_VAN_VRAGEN_EN_ANTWOORDEN = 'Lijst van vragen en antwoorden'
    MEDEDELING = 'Mededeling'
    MEDEDELING_UITSTEL_ANTWOORD = 'Mededeling (uitstel antwoord)'
    MEMORIE_VAN_TOELICHTING = 'Memorie van toelichting'
    MEMORIE_VAN_TOELICHTING_INITIATIEFVOORSTEL = 'Memorie van toelichting (initiatiefvoorstel)'
    MONDELINGE_VRAGEN = 'Mondelinge vragen'
    MOTIE = 'Motie'
    MOTIE_GEWIJZIGDNADER = 'Motie (gewijzigd/nader)'
    NADER_RAPPORT = 'Nader rapport'
    NOTA = 'Nota'
    NOTA_NAV_HET_NADERTWEEDE_NADERENZ_VERSLAG = 'Nota n.a.v. het (nader/tweede nader/enz.) verslag'
    NOTA_VAN_VERBETERING = 'Nota van verbetering'
    NOTA_VAN_WIJZIGING = 'Nota van wijziging'
    NOTA_VAN_WIJZIGING_INITIATIEFVOORSTEL = 'Nota van wijziging (initiatiefvoorstel)'
    ONDERZOEKSVOORSTEL = 'Onderzoeksvoorstel'
    OORSPRONKELIJKE_TEKST = 'Oorspronkelijke tekst'
    OVERIG = 'Overig'
    OVERIG_OPENBAAR = 'Overig (openbaar)'
    OVERZICHT_VERZOEKEN_COMMISSIE_REGELING_VAN_WERKZAAMHEDEN = 'Overzicht verzoeken commissie-regeling van werkzaamheden'
    POSITION_PAPER = 'Position paper'
    RAMING_VAN_DE_UITGAVEN = 'Raming van de uitgaven'
    RAPPORT = 'Rapport'
    RAPPORT_ALGEMENE_REKENKAMER = 'Rapport Algemene Rekenkamer'
    REACTIE_INITIATIEFNEMERS = 'Reactie initiatiefnemer(s)'
    SCHRIFTELIJKE_VRAGEN = 'Schriftelijke vragen'
    SPREKERSLIJST = 'Sprekerslijst'
    STEMMINGSLIJST = 'Stemmingslijst'
    STEMMINGSUITSLAGEN = 'Stemmingsuitslagen'
    STENOGRAM = 'Stenogram'
    VERSLAG_INITIATIEFWETSVOORSTEL_NADER = 'Verslag (initiatief)wetsvoorstel (nader)'
    VERSLAG_COMMISSIE_VERZOEKSCHRIFTEN_EN_DE_BURGERINITIATIEVEN = 'Verslag commissie Verzoekschriften en de Burgerinitiatieven'
    VERSLAG_HOUDENDE_EEN_LIJST_VAN_VRAGEN_EN_ANTWOORDEN = 'Verslag houdende een lijst van vragen en antwoorden'
    VERSLAG_VAN_EEN_ALGEMEEN_OVERLEG = 'Verslag van een algemeen overleg'
    VERSLAG_VAN_EEN_BIJEENKOMST = 'Verslag van een bijeenkomst'
    VERSLAG_VAN_EEN_COMMISSIEDEBAT = 'Verslag van een commissiedebat'
    VERSLAG_VAN_EEN_HOORZITTING__RONDETAFELGESPREK = 'Verslag van een hoorzitting / rondetafelgesprek'
    VERSLAG_VAN_EEN_NOTAOVERLEG = 'Verslag van een notaoverleg'
    VERSLAG_VAN_EEN_POLITIEKE_DIALOOG = 'Verslag van een politieke dialoog'
    VERSLAG_VAN_EEN_RAPPORTEUR = 'Verslag van een rapporteur'
    VERSLAG_VAN_EEN_SCHRIFTELIJK_OVERLEG = 'Verslag van een schriftelijk overleg'
    VERSLAG_VAN_EEN_WERKBEZOEK = 'Verslag van een werkbezoek'
    VERSLAG_VAN_EEN_WETGEVINGSOVERLEG = 'Verslag van een wetgevingsoverleg'
    VOORDRACHT = 'Voordracht'
    VOORLICHTING_AFDELING_ADVISERING_RAAD_VAN_STATE = 'Voorlichting Afdeling advisering Raad van State'
    VOORSTEL_TOT_WIJZIGING_REGLEMENT_VAN_ORDE = 'Voorstel tot wijziging Reglement van Orde'
    VOORSTEL_VAN_WET = 'Voorstel van wet'
    VOORSTEL_VAN_WET_INITIATIEFVOORSTEL = 'Voorstel van wet (initiatiefvoorstel)'
    VOORSTEL_VAN_WET_TWEEDE_LEZING = 'Voorstel van wet (tweede lezing)'
    WETENSCHAPPELIJKE_FACTSHEET = 'Wetenschappelijke factsheet'
    WIJZIGINGEN_VOORGESTELD_DOOR_DE_REGERING = 'Wijzigingen voorgesteld door de regering'


class DocumentFilter(SoortFilter, ZaakRelationFilter):

    def filter_date_range(self, start_datetime, end_datetime):
        filter_str = "Datum ge " + util.datetime_to_odata(start_datetime)
        self.add_filter_str(filter_str)
        filter_str = "Datum lt " + util.datetime_to_odata(end_datetime)
        self.add_filter_str(filter_str)

    def filter_has_agendapunt(self):
        filter_str = 'Agendapunt/any(a:a ne null)'
        self.add_filter_str(filter_str)

    def filter_has_activiteit(self):
        filter_str = 'Activiteit/any(a:a ne null)'
        self.add_filter_str(filter_str)

    def filter_onderwerp(self, onderwerp: str):
        filter_str = "Onderwerp eq '{}'".format(self.escape(onderwerp))
        self.add_filter_str(filter_str)

    def filter_titel(self, titel: str):
        filter_str = "Titel eq '{}'".format(self.escape(titel))
        self.add_filter_str(filter_str)

    def filter_aanhangselnummer(self, aanhangselnummer):
        filter_str = "Aanhangselnummer eq '{}'".format(aanhangselnummer)
        self.add_filter_str(filter_str)

    def filter_nummer(self, documentnummer):
        filter_str = "DocumentNummer eq '{}'".format(documentnummer)
        self.add_filter_str(filter_str)

    def filter_volgnummer(self, volgnummer):
        filter_str = 'Volgnummer eq {}'.format(volgnummer)
        self.add_filter_str(filter_str)

    def filter_alias(self, alias):
        filter_str = "Alias eq '{}'".format(alias)
        self.add_filter_str(filter_str)

    def filter_vergaderjaar(self, vergaderjaar):
        filter_str = "Vergaderjaar eq '{}'".format(vergaderjaar)
        self.add_filter_str(filter_str)

    def filter_dossier(self, nummer, toevoeging=None):
        filter_str = "Kamerstukdossier/any(d: d/Nummer eq {})".format(nummer)
        self.add_filter_str(filter_str)
        if toevoeging:
            filter_str = "Kamerstukdossier/any(d: d/Toevoeging eq '{}')".format(toevoeging)
            self.add_filter_str(filter_str)


class Document(TKItem):
    type = 'Document'
    orderby_param = 'Datum'

    @staticmethod
    def create_filter():
        return DocumentFilter()

    @staticmethod
    def begin_date_key():
        return 'Datum'

    @property
    def bestand_url(self):
        return self.get_resource_url_or_none()

    @property
    def actors(self):
        return self.related_items(DocumentActor)

    @property
    def activiteiten(self):
        from tkapi.activiteit import Activiteit
        return self.related_items(Activiteit)

    @property
    def zaken(self):
        from tkapi.zaak import Zaak
        return self.related_items(Zaak)

    @property
    def agendapunten(self):
        agendapunten = []
        for zaak in self.zaken:
            agendapunten += zaak.agendapunten
        return agendapunten

    @property
    def dossiers(self):
        from tkapi.dossier import Dossier
        return self.related_items(Dossier)

    @property
    def aanhangselnummer(self):
        return self.get_property_or_empty_string('Aanhangselnummer')

    @property
    def onderwerp(self):
        return self.get_property_or_empty_string('Onderwerp')

    @property
    def datum(self):
        return self.get_date_from_datetime_or_none('Datum')

    @property
    def nummer(self):
        return self.get_property_or_empty_string('DocumentNummer')

    @property
    def volgnummer(self):
        return self.get_property_or_none('Volgnummer')

    @property
    def soort(self) -> DocumentSoort:
        return self.get_property_enum_or_none('Soort', DocumentSoort)

    @property
    def titel(self):
        return self.get_property_or_empty_string('Titel')

    @property
    def titel_citeer(self):
        return self.get_property_or_empty_string('Citeertitel')

    @property
    def alias(self):
        return self.get_property_or_empty_string('Alias')

    @property
    def vergaderjaar(self):
        return self.get_property_or_empty_string('Vergaderjaar')

    @property
    def dossier_nummers(self):
        return [dossier.nummer for dossier in self.dossiers]

    @property
    def versies(self):
        return self.related_items(DocumentVersie)


class DocumentActorFilter(Filter):

    def filter_document_id(self, document_id):
        self.add_filter_str('Document_Id eq {}'.format(document_id))


class DocumentActor(TKItem):
    type = 'DocumentActor'

    @staticmethod
    def create_filter():
        return DocumentFilter()

    @property
    def document(self) -> Document:
        return self.related_item(Document)

    @property
    def naam(self):
        return self.get_property_or_empty_string('ActorNaam')

    @property
    def naam_fractie(self):
        return self.get_property_or_empty_string('ActorFractie')

    @property
    def functie(self):
        return self.get_property_or_empty_string('Functie')

    @property
    def persoon(self):
        from tkapi.persoon import Persoon
        return self.related_item(Persoon)

    @property
    def fractie(self):
        from tkapi.fractie import Fractie
        return self.related_item(Fractie)

    @property
    def commissie(self):
        from tkapi.commissie import Commissie
        return self.related_item(Commissie)


class VerslagAlgemeenOverleg(Document):
    filter_param = "Soort eq '{}'".format(DocumentSoort.VERSLAG_VAN_EEN_ALGEMEEN_OVERLEG.value)

    @property
    def voortouwcommissie_namen(self):
        names = []
        for zaak in self.zaken:
            for zaak_actor in zaak.actors:
                if zaak_actor.is_voortouwcommissie:
                    names.append(zaak_actor.naam)
        return names

    @property
    def document_url(self):
        if not self.dossiers:
            return ''
        dossier = self.dossiers[0]
        dossier_nr = str(dossier.nummer)
        if dossier.toevoeging and '(' not in dossier.toevoeging:
            dossier_nr += '-' + str(dossier.toevoeging)
        dossier_nr += '-' + str(self.volgnummer)
        url = 'https://zoek.officielebekendmakingen.nl/kst-' + dossier_nr
        response = requests.get(url, timeout=60)
        if response.status_code != 200 or '404: Pagina niet gevonden' in response.text:
            return ''
        return url


class DocumentVersie(TKItem):
    type = 'DocumentVersie'

    @staticmethod
    def create_filter():
        return Filter()

    @staticmethod
    def begin_date_key():
        return 'Datum'

    @property
    def document(self) -> Document:
        return self.related_item(Document)

    @property
    def datum(self):
        return self.get_date_from_datetime_or_none('Datum')

    @property
    def nummer(self) -> int or None:
        return self.get_property_or_none('Versienummer')

    @property
    def status(self):
        return self.get_property_or_empty_string('Status')

    @property
    def extensie(self):
        return self.get_property_or_empty_string('Extensie')

    @property
    def bestandsgrootte(self) -> int or None:
        return self.get_property_or_none('Bestandsgrootte')
