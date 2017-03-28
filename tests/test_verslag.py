import datetime
import unittest

import tkapi

from local_settings import USER, PASSWORD

api = tkapi.Api(user=USER, password=PASSWORD)


class TestRawApiVerslagAlgemeenOverleg(unittest.TestCase):

    def test_get_verslagen_algemeen_overleg(self):
        start_datetime = datetime.datetime(year=2015, month=1, day=1)
        end_datetime = datetime.datetime(year=2015, month=1, day=10)
        verslagen = api.get_verslagen_van_algemeen_overleg(start_datetime, end_datetime)
        for verslag in verslagen:
            if verslag.activiteit:
                print(verslag.activiteit.begin.isoformat())
                print(verslag.activiteit.einde.isoformat())
