import datetime
import unittest

from tkapi import api
from tkapi.besluit import Besluit


class TestBesluit(unittest.TestCase):

    def test_get_besluiten(self):
        besluit_filter = Besluit.create_filter()
        besluit_filter.filter_empty_zaak()
        besluiten = api.get_besluiten(filter=besluit_filter, max_items=10)
        for besluit in besluiten:
            if besluit.zaken:
                print('BINGO!!!!')
