import tkapi


class ZaakFilter(tkapi.SoortFilter):

    def filter_date_range(self, start_datetime, end_datetime):
        filter_str = "GestartOp ge " + tkapi.util.datetime_to_odata(start_datetime)
        self.filters.append(filter_str)
        filter_str = "GestartOp lt " + tkapi.util.datetime_to_odata(end_datetime)
        self.filters.append(filter_str)

    def add_afgedaan(self, is_afgedaan):
        is_afgedaan_str = 'true' if is_afgedaan else 'false'
        filter_str = "Afgedaan eq " + is_afgedaan_str
        self.filters.append(filter_str)

    def update_afgedaan(self, is_afgedaan):
        is_afgedaan_new_str = 'true' if is_afgedaan else 'false'
        is_afgedaan_remove_str = 'false' if is_afgedaan else 'true'
        filter_new_str = "Afgedaan eq " + is_afgedaan_new_str
        filter_remove_str = "Afgedaan eq " + is_afgedaan_remove_str
        self.filters.remove(filter_remove_str)
        self.filters.append(filter_new_str)

    def filter_nummer(self, nummer):
        filter_str = "Nummer eq " + "'" + nummer.replace("'", "''") + "'"
        self.filters.append(filter_str)

    def filter_onderwerp(self, onderwerp):
        filter_str = "Onderwerp eq " + "'" + onderwerp.replace("'", "''") + "'"
        self.filters.append(filter_str)

    def filter_empty_besluit(self):
        filter_str = 'Besluit/any(b: true)'
        self.filters.append(filter_str)

    def filter_empty_activiteit(self):
        filter_str = 'Activiteit/any(b: true)'
        self.filters.append(filter_str)

    def filter_empty_agendapunt(self):
        filter_str = 'Agendapunt/any(b: true)'
        self.filters.append(filter_str)


class Zaak(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'Zaak'
    expand_param = ''
    orderby_param = 'GestartOp'

    def __str__(self):
        return 'Zaak: ' + str(self.nummer) + ', soort: ' + self.soort + ', onderwerp: ' + self.onderwerp + ', afgedaan: ' + str(self.afgedaan)

    @staticmethod
    def create_filter():
        return ZaakFilter()

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
    def voortouwcommissies(self):
        from tkapi.commissie import VoortouwCommissie
        return self.related_items(VoortouwCommissie)

    @property
    def dossier(self):
        from tkapi.dossier import Dossier
        return self.related_item(Dossier)

    @property
    def onderwerp(self):
        return self.get_property_or_empty_string('Onderwerp')

    @property
    def soort(self):
        return self.get_property_or_empty_string('Soort')

    @property
    def nummer(self):
        return self.get_property_or_empty_string('Nummer')

    @property
    def afgedaan(self):
        return self.json['Afgedaan']

    @property
    def gestart_op(self):
        return self.get_date_or_none('GestartOp')


## Mogelijke Zaak-Soorten zoals gevonden in Zaken van 2016:
# Amendement
# Artikelen/onderdelen (wetsvoorstel)
# Begroting
# Brief commissie
# Brief Europese Commissie
# Brief Kamer
# Brief regering
# Brief van lid/fractie/commissie
# EU-voorstel
# Initiatiefnota
# Initiatiefwetgeving
# Lijst met EU-voorstellen
# Mondelinge vragen
# Motie
# Nationale ombudsman
# Netwerkverkenning
# Nota naar aanleiding van het (nader) verslag
# Nota van wijziging
# Overig
# Parlementair onderzoeksrapport
# PKB/Structuurvisie
# Position paper
# Rapport/brief Algemene Rekenkamer
# Rondvraagpunt procedurevergadering
# Schriftelijke vragen
# Verdrag
# Verzoek bij regeling van werkzaamheden
# Verzoekschrift
# Voordrachten en benoemingen
# Wetgeving
# Wijziging RvO
# Wijzigingen voorgesteld door de regering
