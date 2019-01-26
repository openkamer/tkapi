import tkapi

from tkapi.document import Document


class KamerstukFilter(tkapi.Filter):

    def filter_ondernummer(self, ondernumer):
        filter_str = "Ondernummer eq " + "'" + str(ondernumer) + "'"
        self._filters.append(filter_str)

    def filter_kamerstukdossier(self, nummer):
        filter_str = 'Kamerstukdossier/Nummer eq {}'.format(nummer)
        self.add_filter_str(filter_str)


class Kamerstuk(tkapi.TKItemRelated, tkapi.TKItem):
    url = 'Kamerstuk'

    @staticmethod
    def create_filter():
        return KamerstukFilter()

    @property
    def document(self):
        return self.related_item(Document)

    @property
    def dossiers(self):
        from tkapi.dossier import Dossier
        return self.related_items(Dossier)

    @property
    def dossier(self):
        if self.dossiers:
            return self.dossiers[0]
        return None

    @property
    def ondernummer(self):
        return self.get_property_or_empty_string('Ondernummer')
