import unittest
import datetime

from tkapi.kamervraag import KamerVraag
from tkapi.kamervraag import get_kamervragen
from tkapi.kamervraag import get_schriftelijke_vraag_json
from tkapi.kamervraag import get_schriftelijke_vragen_first_page_json
from tkapi.kamervraag import get_antwoorden
from tkapi.kamervraag import get_antwoorden_first_page_json
from tkapi import util


class TestRawApiKamerVraag(unittest.TestCase):

    def test_me(self):
        self.assertTrue(True)

    def test_raw_get_kamervraag_by_id(self):
        id = "fb6d90db-e4a3-44e1-97fb-6c7832504fe7"
        json = get_schriftelijke_vraag_json(id)
        self.assertEqual(json['Nummer'], '2007D05003')

    def test_raw_get_kamervragen(self):
        start_datetime = datetime.datetime(year=2015, month=1, day=1)
        end_datetime = datetime.datetime(year=2015, month=3, day=1)
        json = get_schriftelijke_vragen_first_page_json(start_datetime, end_datetime)
        vragen_metdata = json["value"]
        # print(vragen_metdata)
        self.assertEqual(len(vragen_metdata), 50)
        # print(util.print_pretty(vragen_metdata[1]))


class TestObjectKamerVraag(unittest.TestCase):

    def test_get_kamervraag_by_id(self):
        id = "fb6d90db-e4a3-44e1-97fb-6c7832504fe7"
        kamervraag = KamerVraag.create_from_id(id)
        self.assertEqual(kamervraag.document.onderwerp, "Het kunstmatig verkorten van de wachtlijsten voor de jeugdzorg")
        self.assertEqual(kamervraag.document.nummer, "2007D05003")

    def test_get_kamervragen_new(self):
        start_datetime = datetime.datetime(year=2015, month=1, day=1)
        end_datetime = datetime.datetime(year=2015, month=1, day=7)
        kamervragen = get_kamervragen(start_datetime, end_datetime)
        self.assertEqual(len(kamervragen), 11)

    def test_get_kamervragen_old(self):
        start_datetime = datetime.datetime(year=2008, month=7, day=4)
        end_datetime = datetime.datetime(year=2008, month=7, day=5)
        kamervragen = get_kamervragen(start_datetime, end_datetime)
        self.assertEqual(len(kamervragen), 3)


class TestRawApiAntwoord(unittest.TestCase):

    def test_raw_get_antwoorden(self):
        start_datetime = datetime.datetime(year=2015, month=1, day=1)
        end_datetime = datetime.datetime(year=2015, month=2, day=1)
        antwoorden_json = get_antwoorden_first_page_json(start_datetime, end_datetime)


class TestObjectAntwoord(unittest.TestCase):

    def test_get_antwoorden_new(self):
        start_datetime = datetime.datetime(year=2015, month=1, day=1)
        end_datetime = datetime.datetime(year=2015, month=1, day=10)
        antwoorden = get_antwoorden(start_datetime, end_datetime)
        self.assertEqual(len(antwoorden), 10)

    def test_get_antwoorden_2010(self):
        start_datetime = datetime.datetime(year=2010, month=1, day=1)
        end_datetime = datetime.datetime(year=2010, month=1, day=10)
        antwoorden = get_antwoorden(start_datetime, end_datetime)
        self.assertEqual(len(antwoorden), 2)

    # NOTE: this test fails because there is no 'Aanhanselnummer' in the document to create the url
    # def test_get_antwoorden_2008(self):
    #     start_datetime = datetime.datetime(year=2008, month=7, day=1)
    #     end_datetime = datetime.datetime(year=2008, month=12, day=1)
    #     antwoorden = get_antwoorden(start_datetime, end_datetime)
    #     print(len(antwoorden))
    #     for antwoord in antwoorden:
    #         print(antwoord.document_url)
