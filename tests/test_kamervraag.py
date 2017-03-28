import unittest
import datetime

import tkapi

from local_settings import USER, PASSWORD

api = tkapi.Api(user=USER, password=PASSWORD)


class TestRawApiKamerVraag(unittest.TestCase):

    def test_me(self):
        self.assertTrue(True)

    def test_raw_get_kamervraag_by_id(self):
        id = "fb6d90db-e4a3-44e1-97fb-6c7832504fe7"
        json = api.get_schriftelijke_vraag_json(id)
        self.assertEqual(json['Nummer'], '2007D05003')


class TestObjectKamerVraag(unittest.TestCase):

    def test_get_kamervragen_new(self):
        start_datetime = datetime.datetime(year=2015, month=1, day=1)
        end_datetime = datetime.datetime(year=2015, month=1, day=7)
        kamervragen = api.get_kamervragen(start_datetime, end_datetime)
        self.assertEqual(len(kamervragen), 11)

    def test_get_kamervragen_old(self):
        start_datetime = datetime.datetime(year=2008, month=7, day=4)
        end_datetime = datetime.datetime(year=2008, month=7, day=5)
        kamervragen = api.get_kamervragen(start_datetime, end_datetime)
        self.assertEqual(len(kamervragen), 3)


class TestObjectAntwoord(unittest.TestCase):

    def test_get_antwoorden_new(self):
        start_datetime = datetime.datetime(year=2015, month=1, day=1)
        end_datetime = datetime.datetime(year=2015, month=1, day=10)
        antwoorden = api.get_antwoorden(start_datetime, end_datetime)
        self.assertEqual(len(antwoorden), 10)

    def test_get_antwoorden_2010(self):
        start_datetime = datetime.datetime(year=2010, month=1, day=1)
        end_datetime = datetime.datetime(year=2010, month=1, day=10)
        antwoorden = api.get_antwoorden(start_datetime, end_datetime)
        self.assertEqual(len(antwoorden), 2)

    # NOTE: this test fails because there is no 'Aanhanselnummer' in the document to create the url
    # def test_get_antwoorden_2008(self):
    #     start_datetime = datetime.datetime(year=2008, month=7, day=1)
    #     end_datetime = datetime.datetime(year=2008, month=12, day=1)
    #     antwoorden = get_antwoorden(start_datetime, end_datetime)
    #     print(len(antwoorden))
    #     for antwoord in antwoorden:
    #         print(antwoord.document_url)
