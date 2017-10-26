import tkapi
from tkapi.zaak import Zaak


class ParlementairDocumentFilter(tkapi.SoortFilter):

    def __init__(self):
        super().__init__()

    def filter_date_range(self, start_datetime, end_datetime):
        filter_str = "Datum ge " + tkapi.util.datetime_to_odata(start_datetime)
        self.filters.append(filter_str)
        filter_str = "Datum lt " + tkapi.util.datetime_to_odata(end_datetime)
        self.filters.append(filter_str)


class ParlementairDocument(tkapi.TKItem):
    url = 'ParlementairDocument'
    expand_param = 'Zaak, Activiteit, Kamerstuk/Kamerstukdossier'
    orderby_param = 'Datum'

    def __init__(self, document_json):
        super().__init__(document_json)
        self.activiteiten_cache = []
        self.zaken_cache = []

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
    def kamerstuk(self):
        return self.json['Kamerstuk']

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
    def dossier(self):
        from tkapi.dossier import DossierFilter
        dossier_filter = DossierFilter()
        dossier_filter.filter_vetnummer(self.kamerstuk['Kamerstukdossier']['Vetnummer'])
        dossiers = tkapi.api.get_dossiers(dossier_filter)
        assert len(dossiers) == 1
        return dossiers[0]

    @property
    def zaken(self):
        if self.zaken_cache:
            return self.zaken_cache
        zaken = []
        for zaak_json in self.json['Zaak']:
            zaken.append(tkapi.api.get_item(Zaak, zaak_json['Id']))
        self.zaken_cache = zaken
        return zaken
