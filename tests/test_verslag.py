import datetime
import unittest

from tkapi import api
from tkapi.verslag import VerslagAlgemeenOverleg
from tkapi.document import ParlementairDocument


class TestVerslagAlgemeenOverleg(unittest.TestCase):

    def test_get_verslagen_algemeen_overleg(self):
        start_datetime = datetime.datetime(year=2015, month=1, day=1)
        end_datetime = datetime.datetime(year=2015, month=1, day=10)
        pd_filter = ParlementairDocument.create_filter()
        pd_filter.filter_date_range(start_datetime, end_datetime)
        verslagen = api.get_verslagen_van_algemeen_overleg(pd_filter)
        for verslag in verslagen:
            if verslag.activiteit:
                verslag.print_json()
                print(verslag.kamerstuk)
                print(verslag.dossier)
                print(verslag.activiteit.begin.isoformat())
                print(verslag.activiteit.einde.isoformat())
