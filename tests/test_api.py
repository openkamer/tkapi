from .core import TKApiTestCase
from tkapi.zaak import Zaak


class TestGetItems(TKApiTestCase):

    def test_max_items(self):
        max_items = 400
        zaken = self.api.get_items(Zaak, max_items=max_items)
        self.assertEqual(len(zaken), max_items)
