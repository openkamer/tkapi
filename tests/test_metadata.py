from tkapi.actor import Persoon
from tkapi.actor import FractieLid
from tkapi.actor import Fractie
from tkapi.activiteit import Activiteit
from tkapi.besluit import Besluit
from tkapi.commissie import Commissie
from tkapi.dossier import Dossier
from tkapi.document import ParlementairDocument
from tkapi.kamerstuk import Kamerstuk
from tkapi.stemming import Stemming
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

    def test_activiteit_metadata(self):
        self.print_entity_example(
            item_class=Activiteit,
            uid='9763a274-42ff-469f-a9ed-003b0feae686'
        )

    def test_zaak_metadata(self):
        self.print_entity_example(
            item_class=Zaak,
            uid='5073c915-51bf-43e7-b07f-d9c6d39d11c4'
        )

    def test_dossier_metadata(self):
        self.print_entity_example(
            item_class=Dossier,
            uid='f659c5c9-5d02-423d-921f-006436140b7f'
        )

    def test_parlementair_document_metadata(self):
        self.print_entity_example(
            item_class=ParlementairDocument,
            uid='2b65bd6a-2b2c-421b-8d03-1b7d5f85be0a'
        )

    def test_commissie_metadata(self):
        self.print_entity_example(
            item_class=Commissie,
            uid='1349488c-8474-4704-bdad-26fa54ea9789'
        )

    def test_kamerstuk_metadata(self):
        self.print_entity_example(
            item_class=Kamerstuk,
            uid='79471b03-156c-4124-9203-0041dee38963'
        )

    def test_stemming_metadata(self):
        self.print_entity_example(
            item_class=Stemming,
            uid='1e4b1b74-ade5-462c-a46c-0002b7066192'
        )

    def test_besluit_metadata(self):
        self.print_entity_example(
            item_class=Besluit,
            uid='6dd32b4b-68f2-4c5a-a94d-00020bac3677'
        )

    def test_persoon_metadata(self):
        self.print_entity_example(
            item_class=Persoon,
            uid='96a61016-76f0-4e73-80f0-0f554d919a93'
        )

    def test_fractielid_metadata(self):
        self.print_entity_example(
            item_class=FractieLid,
            uid='63ec44ec-4b04-460c-b46e-2230c26b3ade'
        )

    def test_fractie_metadata(self):
        self.print_entity_example(
            item_class=Fractie,
            uid='97d432a7-8a64-4db9-9189-cc9f70a4109b'
        )
