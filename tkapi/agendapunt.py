import tkapi


class AgendapuntFilter(tkapi.SoortFilter):

    def __init__(self):
        super().__init__()


class Agendapunt(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'Agendapunt'
    # expand_param = 'Zaak, ParlementairDocument'

    @staticmethod
    def create_filter():
        return AgendapuntFilter()

    @property
    def zaken(self):
        from tkapi.zaak import Zaak
        return self.related_items(Zaak)

    @property
    def parlementaire_documenten(self):
        from tkapi.document import ParlementairDocument
        return self.related_items(ParlementairDocument)
