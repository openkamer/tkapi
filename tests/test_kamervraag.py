import unittest
import datetime

from tkapi.kamervraag import KamerVraag
from tkapi.kamervraag import KamerVragen
from tkapi.kamervraag import get_schriftelijke_vraag
from tkapi.kamervraag import get_schriftelijke_vragen
from tkapi import util


class TestRawApiKamerVraag(unittest.TestCase):

    def test_me(self):
        self.assertTrue(True)

    def test_raw_get_kamervraag_by_id(self):
        id = "fb6d90db-e4a3-44e1-97fb-6c7832504fe7"
        json = get_schriftelijke_vraag(id)
        self.assertEqual(json['Nummer'], '2007D05003')

    def test_raw_get_kamervragen(self):
        start_datetime = datetime.datetime(year=2015, month=1, day=1)
        end_datetime = datetime.datetime(year=2015, month=3, day=1)
        json = get_schriftelijke_vragen(start_datetime, end_datetime)
        vragen_metdata = json["value"]
        # print(vragen_metdata)
        self.assertEqual(len(vragen_metdata), 5)
        # print(util.print_pretty(vragen_metdata[1]))


class TestObjectKamerVraag(unittest.TestCase):

    def test_get_kamervraag_by_id(self):
        id = "fb6d90db-e4a3-44e1-97fb-6c7832504fe7"
        kamervraag = KamerVraag.create_from_id(id)
        self.assertEqual(kamervraag.document.onderwerp, "Het kunstmatig verkorten van de wachtlijsten voor de jeugdzorg")
        self.assertEqual(kamervraag.document.nummer, "2007D05003")

    def test_get_kamervragen(self):
        start_datetime = datetime.datetime(year=2015, month=1, day=1)
        end_datetime = datetime.datetime(year=2015, month=3, day=1)
        kamervragen = KamerVragen(start_datetime, end_datetime)
        self.assertEqual(len(kamervragen.vragen), 5)
        for vraag in kamervragen.vragen:
            vraag.print_info()

    def test_get_kamervragen_old(self):
        start_datetime = datetime.datetime(year=2008, month=7, day=3)
        end_datetime = datetime.datetime(year=2008, month=7, day=5)
        kamervragen = KamerVragen(start_datetime, end_datetime)
        self.assertEqual(len(kamervragen.vragen), 3)
        self.assertEqual(kamervragen.vragen[0].document_url, 'https://zoek.officielebekendmakingen.nl/kv-2070824590')
        self.assertEqual(kamervragen.vragen[1].document_url, 'https://zoek.officielebekendmakingen.nl/kv-2070824570')
        self.assertEqual(kamervragen.vragen[2].document_url, 'https://zoek.officielebekendmakingen.nl/kv-2070824650')
