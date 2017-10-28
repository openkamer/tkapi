import datetime
import unittest

from tkapi import api
from tkapi.besluit import BesluitFilter


class TestBesluit(unittest.TestCase):

    def test_get_besluiten(self):
        besluit_filter = BesluitFilter()
        besluit_filter.filter_empty_zaak()
        besluiten = api.get_besluiten(filter=besluit_filter, max_items=1000)
        for besluit in besluiten:
            if besluit['Zaak']:
                print('BINGO!!!!')
            # besluit.print_json()
            # for stemming in besluit.stemmingen:
            #     stemming.print_json()
