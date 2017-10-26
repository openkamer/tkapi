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

    def __init__(self, document_json):
        super().__init__(document_json)

    @staticmethod
    def get_params_default():
        params = {
            '$orderby': 'Datum',
            '$expand': 'Zaak, Activiteit, Kamerstuk/Kamerstukdossier',
        }
        return params

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
    def title(self):
        return self.get_property_or_empty_string('Titel')

    @property
    def vergaderjaar(self):
        return self.get_property_or_empty_string('Vergaderjaar')

    @property
    def kamerstuk(self):
        return self.json['Kamerstuk']

    @property
    def activiteit(self):
        return self.json['Activiteit']

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
        zaken = []
        for zaak_json in self.json['Zaak']:
            zaken.append(Zaak(zaak_json))
        return zaken
