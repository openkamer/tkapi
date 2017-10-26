import tkapi


class ZaakFilter(tkapi.SoortFilter):

    def __init__(self):
        super().__init__()

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

    def add_onderwerp(self, onderwerp):
        filter_str = "Onderwerp eq " + "'" + onderwerp.replace("'", "''") + "'"
        self.filters.append(filter_str)


class Zaak(tkapi.TKItem):
    url = 'Zaak'

    def __init__(self, zaak_json):
        super().__init__(zaak_json)
        self.filters = []

    @staticmethod
    def get_params_default():
        params = {
            '$orderby': 'GestartOp'
        }
        return params

    @staticmethod
    def filter_onderwerp(onderwerp):
        filter_str = "Onderwerp eq " + "'" + onderwerp.replace("'", "''") + "'"
        params = {
            '$filter': filter_str,
        }
        return params

    @staticmethod
    def add_filter_soort(soort):
        filter_str = "Soort eq " + "'" + soort.replace("'", "''") + "'"
        params = {
            '$filter': filter_str,
        }
        return params

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
        return self.get_property_or_empty_string('Afgedaan')


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
