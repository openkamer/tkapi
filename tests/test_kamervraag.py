import unittest
import datetime

from tkapi import api
from tkapi.kamervraag import Kamervraag
from tkapi.document import ParlementairDocument


class TestRawApiKamerVraag(unittest.TestCase):

    def test_me(self):
        self.assertTrue(True)

    def test_raw_get_kamervraag_by_id(self):
        id = "fb6d90db-e4a3-44e1-97fb-6c7832504fe7"
        kamervraag = api.get_item(Kamervraag, id, params={'$expand': 'Zaak', })
        kamervraag.print_json()
        self.assertEqual(kamervraag['Nummer'], '2007D05003')


class TestObjectKamerVraag(unittest.TestCase):

    def test_get_kamervragen_new(self):
        start_datetime = datetime.datetime(year=2015, month=1, day=1)
        end_datetime = datetime.datetime(year=2015, month=1, day=7)
        kv_filter = ParlementairDocument.create_filter()
        kv_filter.filter_date_range(start_datetime, end_datetime)
        kamervragen = api.get_kamervragen(kv_filter)
        self.assertEqual(len(kamervragen), 11)

    def test_get_kamervragen_old(self):
        start_datetime = datetime.datetime(year=2008, month=7, day=4)
        end_datetime = datetime.datetime(year=2008, month=7, day=5)
        kv_filter = ParlementairDocument.create_filter()
        kv_filter.filter_date_range(start_datetime, end_datetime)
        kamervragen = api.get_kamervragen(kv_filter)
        self.assertEqual(len(kamervragen), 3)

    def test_get_kamervragen_2013(self):
        start_datetime = datetime.datetime(year=2013, month=1, day=31)
        end_datetime = datetime.datetime(year=2013, month=2, day=1)
        kv_filter = ParlementairDocument.create_filter()
        kv_filter.filter_date_range(start_datetime, end_datetime)
        kamervragen = api.get_kamervragen(kv_filter)


class TestObjectAntwoord(unittest.TestCase):

    def test_get_antwoorden_new(self):
        start_datetime = datetime.datetime(year=2015, month=1, day=1)
        end_datetime = datetime.datetime(year=2015, month=1, day=10)
        kv_filter = ParlementairDocument.create_filter()
        kv_filter.filter_date_range(start_datetime, end_datetime)
        antwoorden = api.get_antwoorden(kv_filter)
        self.assertEqual(len(antwoorden), 10)

    def test_get_antwoorden_2010(self):
        start_datetime = datetime.datetime(year=2010, month=1, day=1)
        end_datetime = datetime.datetime(year=2010, month=1, day=10)
        kv_filter = ParlementairDocument.create_filter()
        kv_filter.filter_date_range(start_datetime, end_datetime)
        antwoorden = api.get_antwoorden(kv_filter)
        self.assertEqual(len(antwoorden), 2)

    # NOTE: this test fails because there is no 'Aanhanselnummer' in the document to create the url
    # def test_get_antwoorden_2008(self):
    #     start_datetime = datetime.datetime(year=2008, month=7, day=1)
    #     end_datetime = datetime.datetime(year=2008, month=12, day=1)
    #     antwoorden = get_antwoorden(start_datetime, end_datetime)
    #     print(len(antwoorden))
    #     for antwoord in antwoorden:
    #         print(antwoord.document_url)
