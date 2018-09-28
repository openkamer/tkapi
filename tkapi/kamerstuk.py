import tkapi

from tkapi.document import ParlementairDocument


class KamerstukFilter(tkapi.Filter):

    def __init__(self):
        super().__init__()

    def filter_ondernummer(self, ondernumer):
        filter_str = "Ondernummer eq " + "'" + str(ondernumer) + "'"
        self.filters.append(filter_str)


class Kamerstuk(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'Kamerstuk'
    expand_param = 'Kamerstukdossier, ParlementairDocument'

    def __init__(self, kamerstuk_json):
        super().__init__(kamerstuk_json)

    @staticmethod
    def create_filter():
        return KamerstukFilter()

    @property
    def parlementair_document(self):
        return self.related_item(ParlementairDocument)

    @property
    def dossiers(self):
        from tkapi.dossier import Dossier
        return self.related_items(Dossier)

    @property
    def ondernummer(self):
        return self.get_property_or_empty_string('Ondernummer')

    @property
    def dossier(self):
        dossiers = self.dossiers
        if dossiers:
            return dossiers[0]
        return None
