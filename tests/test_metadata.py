from tkapi.persoon import Persoon
from tkapi.fractie import Fractie, FractieZetel
from tkapi.fractie import FractieZetelPersoon
from tkapi.activiteit import Activiteit
from tkapi.besluit import Besluit
from tkapi.commissie import Commissie
from tkapi.dossier import Dossier
from tkapi.document import Document
# from tkapi.kamerstuk import Kamerstuk
from tkapi.stemming import Stemming
# from tkapi.vergadering import Vergadering
from tkapi.zaak import Zaak

from .core import TKApiTestCase


class TestMetaData(TKApiTestCase):

    @classmethod
    def print_entity_example(cls, item_class, uid):
        item_class.expand_param = ''
        item = cls.api.get_item(item_class, uid)
        print('\n=== ' + item.url + ' ===')
        item.print_json()
        print('\n\n')

    @classmethod
    def print_entity_first_example(cls, item_class):
        item_class.expand_param = ''
        item = cls.api.get_items(item_class, max_items=1)[0]
        print('\n=== ' + item.url + ' ===')
        item.print_json()
        print('\n\n')

    def test_activiteit(self):
        self.print_entity_first_example(Activiteit)

    def test_zaak(self):
        self.print_entity_first_example(Zaak)

    def test_dossier(self):
        self.print_entity_first_example(Dossier)

    def test_document(self):
        self.print_entity_first_example(Document)

    def test_commissie(self):
        self.print_entity_first_example(Commissie)

    # def test_kamerstuk(self):
    #     self.print_entity_first_example(Kamerstuk)

    def test_stemming(self):
        self.print_entity_first_example(Stemming)

    def test_besluit(self):
        self.print_entity_first_example(Besluit)

    def test_persoon(self):
        self.print_entity_first_example(Persoon)

    def test_fractiezetel(self):
        self.print_entity_first_example(FractieZetel)

    def test_fractiezetelpersoon(self):
        self.print_entity_first_example(FractieZetelPersoon)

    def test_fractie(self):
        self.print_entity_first_example(Fractie)

    # def test_vergadering(self):
    #     self.print_entity_first_example(Vergadering)
