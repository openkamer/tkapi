import datetime

from tkapi.stemming import Stemming

from .core import TKApiTestCase


class TestStemming(TKApiTestCase):

    def test_get_stemmingen(self):
        stemmingen = self.api.get_stemmingen(filter=None, max_items=10)
        self.assertEqual(10, len(stemmingen))


class TestStemmingFilters(TKApiTestCase):

    def test_filter_moties(self):
        n_items = 10
        filter = Stemming.create_filter()
        filter.filter_moties()
        stemmingen = self.api.get_stemmingen(filter=filter, max_items=n_items)
        self.assertEqual(n_items, len(stemmingen))
        for stemming in stemmingen:
            self.assertEqual('Motie', stemming.besluit.zaken[0].soort)

    def test_filter_kamerstukdossier(self):
        filter = Stemming.create_filter()
        filter.filter_kamerstukdossier(nummer=33885)
        stemmingen = self.api.get_stemmingen(filter=filter)
        self.assertEqual(208, len(stemmingen))

    def test_filter_kamerstuk(self):
        filter = Stemming.create_filter()
        filter.filter_kamerstuk(nummer=33885, ondernummer=16)
        stemmingen = self.api.get_stemmingen(filter=filter)
        self.assertEqual(16, len(stemmingen))
