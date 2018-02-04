import tkapi


class ParlementairDocumentFilter(tkapi.SoortFilter, tkapi.ZaakRelationFilter):

    def __init__(self):
        super().__init__()

    def filter_date_range(self, start_datetime, end_datetime):
        filter_str = "Datum ge " + tkapi.util.datetime_to_odata(start_datetime)
        self.filters.append(filter_str)
        filter_str = "Datum lt " + tkapi.util.datetime_to_odata(end_datetime)
        self.filters.append(filter_str)

    def filter_empty_agendapunt(self):
        filter_str = 'Agendapunt/any(a: true)'
        self.filters.append(filter_str)

    def filter_onderwerp(self, onderwerp):
        filter_str = 'Onderwerp eq ' + "'" + onderwerp.replace("'", "''") + "'"
        self.filters.append(filter_str)

    def filter_titel(self, titel):
        filter_str = 'Titel eq ' + "'" + titel.replace("'", "''") + "'"
        self.filters.append(filter_str)


class ParlementairDocument(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'ParlementairDocument'
    expand_param = 'Zaak, Activiteit, Agendapunt, Kamerstuk/Kamerstukdossier'
    # expand_param = ''
    orderby_param = 'Datum'

    def __init__(self, document_json):
        super().__init__(document_json)
        self.activiteiten_cache = []
        self.agendapunten_cache = []
        self.kamerstuk_cache = None
        self.dossier_cache = None

    @staticmethod
    def create_filter():
        return ParlementairDocumentFilter()

    @property
    def activiteiten(self):
        if self.activiteiten_cache:
            return self.activiteiten_cache
        from tkapi.activiteit import Activiteit
        activiteiten = []
        for activiteit_json in self.json['Activiteit']:
            activiteiten.append(tkapi.api.get_item(Activiteit, activiteit_json['Id']))
        self.activiteiten_cache = activiteiten
        return activiteiten

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
        dossiers = []
        for kamerstuk in self.kamerstukken:
            kamerstuk += kamerstuk.dossiers
        return dossiers

    @property
    def kamerstukken(self):
        from tkapi.kamerstuk import Kamerstuk
        return self.related_items(Kamerstuk)

    @property
    def aanhangselnummer(self):
        return self.get_property_or_empty_string('Aanhangselnummer')

    @property
    def onderwerp(self):
        return self.get_property_or_empty_string('Onderwerp')

    @property
    def datum(self):
        return self.get_date_or_none('Datum')

    @property
    def nummer(self):
        return self.get_property_or_empty_string('Nummer')

    @property
    def soort(self):
        return self.get_property_or_empty_string('Soort')

    @property
    def titel(self):
        return self.get_property_or_empty_string('Titel')

    @property
    def vergaderjaar(self):
        return self.get_property_or_empty_string('Vergaderjaar')

    @property
    def alias(self):
        return self.get_property_or_empty_string('Alias')

    @property
    def dossier_vetnummer(self):
        if self.json['Kamerstuk'] and self.json['Kamerstuk']['Kamerstukdossier'] and self.json['Kamerstuk']['Kamerstukdossier']['Vetnummer']:
            return self.json['Kamerstuk']['Kamerstukdossier']['Vetnummer']
        return None

