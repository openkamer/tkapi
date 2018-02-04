import unittest
import datetime

from tkapi import api
from tkapi.activiteit import Activiteit
from tkapi.besluit import Besluit
from tkapi.commissie import Commissie
from tkapi.dossier import Dossier
from tkapi.document import ParlementairDocument
from tkapi.kamerstuk import Kamerstuk
from tkapi.persoon import Persoon
from tkapi.stemming import Stemming
from tkapi.zaak import Zaak


class TestMetaData(unittest.TestCase):

    @staticmethod
    def print_entity_example(item_class, uid):
        item_class.expand_param = ''
        item = api.get_item(item_class, uid)
        print('\n=== ' + item.url + ' ===')
        item.print_json()
        print('\n\n')

    def test_activiteit_metadata(self):
        TestMetaData.print_entity_example(
            item_class=Activiteit,
            uid='9763a274-42ff-469f-a9ed-003b0feae686'
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

    def test_commissie_metadata(self):
        TestMetaData.print_entity_example(
            item_class=Commissie,
            uid='1349488c-8474-4704-bdad-26fa54ea9789'
        )

    def test_kamerstuk_metadata(self):
        TestMetaData.print_entity_example(
            item_class=Kamerstuk,
            uid='8d5481b7-d6b9-4452-921d-003819845c48'
        )

    def test_persoon_metadata(self):
        TestMetaData.print_entity_example(
            item_class=Persoon,
            uid='96a61016-76f0-4e73-80f0-0f554d919a93'
        )

    def test_stemming_metadata(self):
        TestMetaData.print_entity_example(
            item_class=Stemming,
            uid='91ce3690-34c7-4834-9982-00a76ec14eed'
        )

    def test_besluit_metadata(self):
        TestMetaData.print_entity_example(
            item_class=Besluit,
            uid='e2a08641-6ed7-4a96-9353-001663f136ba'
        )
