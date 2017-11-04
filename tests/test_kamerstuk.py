import datetime
import unittest

from tkapi import api
from tkapi.kamerstuk import Kamerstuk


class TestKamerstuk(unittest.TestCase):

    def test_get_kamerstuk(self):
        ks_uid = '8d5481b7-d6b9-4452-921d-003819845c48'
        kamerstuk = api.get_item(Kamerstuk, ks_uid)
        self.assertEqual(kamerstuk.id, ks_uid)
        self.assertEqual(kamerstuk.ondernummer, '82')

    def test_get_kamerstukken(self):
        kamerstukken = api.get_kamerstukken(filter=None, max_items=100)
        for kamerstuk in kamerstukken:
            kamerstuk.print_json()

    def test_get_kamerstuk_by_ondernummer(self):
        ondernummer = '82'
        kamerstuk_filter = Kamerstuk.create_filter()
        kamerstuk_filter.filter_ondernummer(ondernummer)
        kamerstukken = api.get_kamerstukken(filter=kamerstuk_filter)
        self.assertTrue(len(kamerstukken) > 100)
        kamerstukken[0].print_json()
        for kamerstuk in kamerstukken:
            self.assertEqual(kamerstuk.ondernummer, ondernummer)

    def test_get_kamerstuk_parlementair_document(self):
        ks_uid = '8d5481b7-d6b9-4452-921d-003819845c48'
        kamerstuk = api.get_item(Kamerstuk, ks_uid)
        self.assertEqual(kamerstuk.id, ks_uid)
        self.assertEqual(kamerstuk.ondernummer, '82')
        pd = kamerstuk.parlementair_document
        pd.print_json()