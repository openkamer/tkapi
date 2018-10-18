from tkapi.besluit import Besluit

from .core import TKApiTestCase


class TestBesluit(TKApiTestCase):

    def test_get_besluiten(self):
        besluit_filter = Besluit.create_filter()
        besluit_filter.filter_empty_zaak()
        besluiten = self.api.get_besluiten(filter=besluit_filter, max_items=10)
        for besluit in besluiten:
            if besluit.zaken:
                print('BINGO!!!!')
