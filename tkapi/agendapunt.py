import tkapi


class AgendapuntFilter(tkapi.SoortFilter):

    def __init__(self):
        super().__init__()


class Agendapunt(tkapi.TKItem):
    url = 'Agendapunt'
    expand_param = 'Zaak, ParlementairDocument'

    def __init__(self, agendapunt_json):
        super().__init__(agendapunt_json)
        self.zaken_cache = []
        self.parlementaire_documenten_cache = []

    @staticmethod
    def create_filter():
        return AgendapuntFilter()

    @property
    def zaken(self):
        if self.zaken_cache:
            return self.zaken_cache
        from tkapi.zaak import Zaak
        zaken = []
        for zaak_json in self.json['Zaak']:
            zaken.append(tkapi.api.get_item(Zaak, zaak_json['Id']))
        self.zaken_cache = zaken
        return zaken

    @property
    def parlementaire_documenten(self):
        if self.parlementaire_documenten_cache:
            return self.parlementaire_documenten_cache
        from tkapi.document import ParlementairDocument
        parlementaire_documenten = []
        for pd_json in self.json['ParlementairDocument']:
            parlementaire_documenten.append(tkapi.api.get_item(ParlementairDocument, pd_json['Id']))
        self.parlementaire_documenten_cache = parlementaire_documenten
        return parlementaire_documenten
