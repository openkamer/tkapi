from enum import Enum
from typing import List

import tkapi
from tkapi.persoon import Persoon
from tkapi.util import util


class ZaakFilter(tkapi.SoortFilter):

    def filter_date_range(self, start_datetime, end_datetime):
        filter_str = "GestartOp ge " + util.datetime_to_odata(start_datetime)
        self._filters.append(filter_str)
        filter_str = "GestartOp lt " + util.datetime_to_odata(end_datetime)
        self._filters.append(filter_str)

    def filter_begin_date_not_empty(self):
        filter_str = "GestartOp ne null"
        self._filters.append(filter_str)

    def filter_afgedaan(self, is_afgedaan=True):
        is_afgedaan_str = 'true' if is_afgedaan else 'false'
        filter_str = "Afgedaan eq " + is_afgedaan_str
        self._filters.append(filter_str)

    def update_afgedaan(self, is_afgedaan):
        is_afgedaan_new_str = 'true' if is_afgedaan else 'false'
        is_afgedaan_remove_str = 'false' if is_afgedaan else 'true'
        filter_new_str = "Afgedaan eq " + is_afgedaan_new_str
        filter_remove_str = "Afgedaan eq " + is_afgedaan_remove_str
        self._filters.remove(filter_remove_str)
        self._filters.append(filter_new_str)

    def filter_kamerstukdossier(self, nummer):
        filter_str = 'Kamerstukdossier/any(d: d/Nummer eq {})'.format(nummer)
        self.add_filter_str(filter_str)

    def filter_nummer(self, nummer):
        filter_str = "Nummer eq '{}'".format(nummer)
        self._filters.append(filter_str)

    def filter_document(self, volgnummer):
        filter_str = 'Document/any(d: d/Volgnummer eq {})'.format(volgnummer)
        self.add_filter_str(filter_str)

    def filter_volgnummer(self, nummer):
        filter_str = "Volgnummer eq {}".format(nummer)
        self._filters.append(filter_str)

    def filter_onderwerp(self, onderwerp):
        filter_str = "Onderwerp eq '{}'".format(onderwerp)
        self._filters.append(filter_str)

    def filter_has_besluit(self):
        filter_str = 'Besluit/any(b:b ne null)'
        self._filters.append(filter_str)

    def filter_has_activiteit(self):
        filter_str = 'Activiteit/any(a:a ne null)'
        self._filters.append(filter_str)

    def filter_has_agendapunt(self):
        filter_str = 'Agendapunt/any(a:a ne null)'
        self._filters.append(filter_str)

    def filter_kabinetsappreciatie(self, kabinetsappreciatie):
        if isinstance(kabinetsappreciatie, Enum):
            kabinetsappreciatie = kabinetsappreciatie.value
        filter_str = "Kabinetsappreciatie eq '{}'".format(kabinetsappreciatie)
        self._filters.append(filter_str)


class Zaak(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'Zaak'
    orderby_param = 'GestartOp'

    def __str__(self):
        return 'Zaak: ' + str(self.nummer) + ', soort: ' + self.soort.value + ', onderwerp: ' + self.onderwerp + ', afgedaan: ' + str(self.afgedaan)

    @staticmethod
    def create_filter():
        return ZaakFilter()

    @property
    def documenten(self):
        from tkapi.document import Document
        return self.related_items(Document)

    @property
    def agendapunten(self):
        from tkapi.agendapunt import Agendapunt
        return self.related_items(Agendapunt)

    @property
    def activiteiten(self):
        from tkapi.activiteit import Activiteit
        return self.related_items(Activiteit)

    @property
    def besluiten(self):
        from tkapi.besluit import Besluit
        return self.related_items(Besluit)

    @property
    def indiener(self):
        return self.related_item(ZaakActor, item_key='Indiener')

    @property
    def medeindieners(self):
        return self.related_items(ZaakActor, item_key='Medeindiener')

    @property
    def zaak_actors(self):
        from tkapi.actor import ZaakActor
        return self.related_items(ZaakActor)

    @property
    def dossier(self):
        from tkapi.dossier import Dossier
        return self.related_item(Dossier)

    @property
    def onderwerp(self):
        return self.get_property_or_empty_string('Onderwerp')

    @property
    def soort(self):
        return self.get_property_enum_or_none('Soort', ZaakSoort)

    @property
    def nummer(self):
        return self.get_property_or_empty_string('Nummer')

    @property
    def volgnummer(self):
        return self.get_property_or_empty_string('Volgnummer')

    @property
    def alias(self):
        return self.get_property_or_empty_string('Alias')

    @property
    def afgedaan(self):
        return self.get_property_or_none('Afgedaan')

    @property
    def vervangen_door(self):
        return self.related_item(Zaak, item_key='VervangenDoor')

    @property
    def gestart_op(self):
        return self.get_date_from_datetime_or_none('GestartOp')

    @property
    def kabinetsappreciatie(self):
        return self.get_property_enum_or_none('Kabinetsappreciatie', KabinetsAppreciatie)

    @staticmethod
    def begin_date_key():
        return 'GestartOp'


class ZaakActorFilter(tkapi.Filter):
    pass


class ZaakActor(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'ZaakActor'

    @staticmethod
    def create_filter():
        return ZaakActorFilter()

    @property
    def naam(self):
        return self.get_property_or_empty_string('ActorNaam')

    @property
    def afkorting(self):
        return self.get_property_or_empty_string('ActorAfkorting')

    @property
    def functie(self):
        return self.get_property_or_empty_string('Functie')

    @property
    def relatie(self):
        return self.get_property_or_empty_string('Relatie')

    @property
    def persoon(self):
        from tkapi.persoon import Persoon
        return self.related_item(Persoon)

    @property
    def zaak(self):
        return self.related_item(Zaak)

    @property
    def fractie(self):
        from tkapi.fractie import Fractie
        return self.related_item(Fractie)

    @property
    def commissie(self):
        from tkapi.commissie import Commissie
        return self.related_item(Commissie)


class ZaakSoort(Enum):
    AMENDEMENT = 'Amendement'
    ARTIKELEN_WETSVOORSTEL = 'Artikelen/onderdelen (wetsvoorstel)'
    BEGROTING = 'Begroting'
    BRIEF_COMMISSIE = 'Brief commissie'
    BRIEF_EUROPESE_COMMISSIE = 'Brief Europese Commissie'
    BRIEF_KAMER = 'Brief Kamer'
    BRIEF_REGERING = 'Brief regering'
    BRIEF_LID = 'Brief van lid/fractie/commissie'
    EU_VOORSTEL = 'EU-voorstel'
    INITIATIEF_NOTA = 'Initiatiefnota'
    INITIATIEF_WETGEVING = 'Initiatiefwetgeving'
    LIJST_EU_VOORSTELLEN = 'Lijst met EU-voorstellen'
    MONDELINGE_VRAGEN = 'Mondelinge vragen'
    MOTIE = 'Motie'
    NATIONALE_OMBUDSMAN = 'Nationale ombudsman'
    NETWERKVERKENNING = 'Netwerkverkenning'
    NOTA_VAN_VERSLAG = 'Nota naar aanleiding van het (nader) verslag'
    NOTA_VAN_WIJZIGING = 'Nota van wijziging'
    OVERIG = 'Overig'
    PARLEMENTAIR_ONDERZOEKSRAPPORT = 'Parlementair onderzoeksrapport'
    PKB_STRUCTUURVISIE = 'PKB/Structuurvisie'
    POSITION_PAPER = 'Position paper'
    RAPPORT_ALGEMENE_REKENKAMER = 'Rapport/brief Algemene Rekenkamer'
    RONDVRAAGPUNT_PROCEDUREVERGADERING = 'Rondvraagpunt procedurevergadering'
    SCHRIFTELIJKE_VRAGEN = 'Schriftelijke vragen'
    VERDRAG = 'Verdrag'
    VERZOEK_REGELING_WERKZAAMHEDEN = 'Verzoek bij regeling van werkzaamheden'
    VERZOEKSCHRIFT = 'Verzoekschrift'
    VOORDRACHTEN_EN_BENOEMINGEN = 'Voordrachten en benoemingen'
    WETGEVING = 'Wetgeving'
    WIJZIGING_RVO = 'Wijziging RvO'
    WIJZIGING_VOORGESTELD_REGERING = 'Wijzigingen voorgesteld door de regering'


class KabinetsAppreciatie(Enum):
    OVERGENOMEN = 'Overgenomen'
    ONTRADEN = 'Ontraden'
    ONTRADEN_TENZIJ_GEWIJZGID = 'Ontraden, tenzij gewijzigd'
    OORDEEL_KAMER = 'Oordeel Kamer'
    VERZOCHT_AAN_TE_HOUDEN = 'Verzocht motie aan te houden'
    GEEN_APPRECIATIE = 'Geen (expliciete) appreciatie'
    NIET_BESCHIKBAAR_BIJ_WIJZIGING = 'Niet beschikbaar bij gewijzigde moties en/of amendementen'
    NIET_BESCHIKBAAR = 'Niet beschikbaar bij moties en/of amendementen vóór 1 april 2019'
    NOG_NIET_BEKEND = 'Nog niet bekend'
    NOG_TE_ONTVANGEN = 'Nog te ontvangen'


class ZaakMetBesluitBase(Zaak):

    @property
    def besluit(self):
        besluiten = self.besluiten
        if not besluiten:
            return None
        return self.besluiten[0]

    @property
    def besluit_text(self):
        besluit = self.besluit
        if not besluit:
            return None
        return besluit.tekst

    @property
    def stemmingen(self):
        besluit = self.besluit
        if not besluit:
            return None
        return self.besluit.stemmingen


class ZaakMotie(ZaakMetBesluitBase):
    filter_param = 'Soort eq \'{}\''.format(ZaakSoort.MOTIE.value)


class ZaakAmendement(ZaakMetBesluitBase):
    filter_param = 'Soort eq \'{}\''.format(ZaakSoort.AMENDEMENT.value)
