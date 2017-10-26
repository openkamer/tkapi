import unittest
import datetime

from tkapi import api
from tkapi.zaak import Zaak
from tkapi.activiteit import Activiteit
from tkapi.document import ParlementairDocument
from tkapi.dossier import Dossier


class TestMetaData(unittest.TestCase):

    @staticmethod
    def print_entity_example(item_class, uid):
        item = api.get_item(item_class, uid)
        print('\n=== ' + item.url + ' ===')
        item.print_json()
        print('\n\n')

    def test_activiteit_metadata(self):
        TestMetaData.print_entity_example(
            item_class=Activiteit,
            uid='01aeb96f-ad46-48ec-9213-000ab9dbaf75'
        )

    def test_zaak_metadata(self):
        TestMetaData.print_entity_example(
            item_class=Zaak,
            uid='7f61ac7d-c798-47c3-9303-8837ea774c1b'
        )

    def test_dossier_metadata(self):
        TestMetaData.print_entity_example(
            item_class=Dossier,
            uid='e680e889-6ed3-4448-8e5a-3f52a1290bd5'
        )

    def test_parlementair_document_metadata(self):
        TestMetaData.print_entity_example(
            item_class=ParlementairDocument,
            uid='a1ab86b1-a681-4849-b7c8-fe5481fc654d'
        )