from tkapi.vergadering import Vergadering
from tkapi.vergadering import VergaderingSoort

from .core import TKApiTestCase


class TestVergadering(TKApiTestCase):

    def test_get_vergaderingen(self):
        max_items = 10
        vergaderingen = self.api.get_vergaderingen(filter=None, max_items=max_items)
        self.assertEqual(max_items, len(vergaderingen))
        for vergadering in vergaderingen:
            self.assertIsNotNone(vergadering.soort)
            self.assertIsNotNone(vergadering.verslag)
            self.assertIsNotNone(vergadering.datum)
            self.assertIsNotNone(vergadering.begin)
            self.assertIsNotNone(vergadering.einde)
            self.assertIsNotNone(vergadering.nummer)

    def test_get_vergadering_soorten(self):
        max_items = 100
        vergaderingen = self.api.get_vergaderingen(filter=None, max_items=max_items)
        self.assertEqual(max_items, len(vergaderingen))
        soorten = set()
        for vergadering in vergaderingen:
            soorten.add(vergadering.soort)
        self.assertGreaterEqual(len(soorten), 1)


class TestVergaderingFilter(TKApiTestCase):

    def test_vergadering_soort_filter(self):
        max_items = 10
        filter = Vergadering.create_filter()
        filter.filter_soort(soort=VergaderingSoort.COMMISSIE)
        verslagen = self.api.get_vergaderingen(filter=filter, max_items=max_items)
        self.assertEqual(max_items, len(verslagen))
