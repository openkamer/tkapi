import datetime
import unittest

import tkapi.verslag
import tkapi.util


class TestRawApiVerslagAlgemeenOverleg(unittest.TestCase):

    def test_raw_get_verslagen_algemeen_overleg_page(self):
        start_datetime = datetime.datetime(year=2015, month=1, day=1)
        end_datetime = datetime.datetime(year=2015, month=3, day=1)
        page = tkapi.verslag.get_verslag_algemeen_overleg_first_page_json(start_datetime, end_datetime)
        # tkapi.util.print_pretty(page)

    def test_get_verslagen_algemeen_overleg(self):
        start_datetime = datetime.datetime(year=2015, month=1, day=1)
        end_datetime = datetime.datetime(year=2015, month=1, day=10)
        verslagen = tkapi.verslag.get_verslagen_van_algemeen_overleg(start_datetime, end_datetime)
        for verslag in verslagen:
            if verslag.activiteit:
                print(verslag.activiteit.begin.isoformat())
                print(verslag.activiteit.end.isoformat())