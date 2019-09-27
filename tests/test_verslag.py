from tkapi.verslag import Verslag
from tkapi.verslag import VerslagSoort
from tkapi.verslag import VerslagStatus

from .core import TKApiTestCase


class TestVerslag(TKApiTestCase):

    def test_get_verslagen(self):
        max_items = 100
        verslagen = self.api.get_verslagen(filter=None, max_items=max_items)
        self.assertEqual(max_items, len(verslagen))
        for verslag in verslagen:
            self.assertIsNotNone(verslag.status)
            self.assertIsNotNone(verslag.soort)
            self.assertIsNotNone(verslag.vergadering)

    def test_get_verslagen_soorten(self):
        max_items = 100
        verslagen = self.api.get_verslagen(filter=None, max_items=max_items)
        self.assertEqual(max_items, len(verslagen))
        soorten = set()
        for verslag in verslagen:
            soorten.add(verslag.soort)
        self.assertGreater(len(soorten), 1)


class TestVerslagFilter(TKApiTestCase):

    def test_verslagen_soort_filter(self):
        max_items = 100
        filter = Verslag.create_filter()
        filter.filter_soort(soort=VerslagSoort.EINDPUBLICATIE)
        verslagen = self.api.get_verslagen(filter=filter, max_items=max_items)
        self.assertEqual(max_items, len(verslagen))

    def test_verslagen_status_filter(self):
        max_items = 100
        filter = Verslag.create_filter()
        filter.filter_status(status=VerslagStatus.GECORRIGEERD)
        verslagen = self.api.get_verslagen(filter=filter, max_items=max_items)
        self.assertEqual(max_items, len(verslagen))
