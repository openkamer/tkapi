import json

import tkapi

from tkapi.document import ParlementairDocument
from tkapi.dossier import Dossier


class KamerstukFilter(tkapi.Filter):

    def __init__(self):
        super().__init__()

    def filter_ondernummer(self, ondernumer):
        filter_str = "Ondernummer eq " + "'" + str(ondernumer) + "'"
        self.filters.append(filter_str)


class Kamerstuk(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'Kamerstuk'
    # expand_param = 'Kamerstukdossier, ParlementairDocument'

    def __init__(self, kamerstuk_json):
        super().__init__(kamerstuk_json)

    @property
    def dossiers(self):
        from tkapi.dossier import Dossier
        return self.related_items(Dossier)

    @staticmethod
    def create_filter():
        return KamerstukFilter()

    @property
    def ondernummer(self):
        return self.get_property_or_empty_string('Ondernummer')

    @property
    def parlementair_document(self):
        pd_uid = self.get_property_or_none('ParlementairDocument')['Id']
        return tkapi.api.get_item(ParlementairDocument, pd_uid)

    @property
    def dossier(self):
        dossier_uid = self.get_property_or_none(Dossier.url)['Id']
        return tkapi.api.get_item(Dossier, dossier_uid)
