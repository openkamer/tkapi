import datetime

from tkapi.kamervraag import Kamervraag
from tkapi.document import Document

from .core import TKApiTestCase


class TestRawApiKamerVraag(TKApiTestCase):

    def test_me(self):
        self.assertTrue(True)

    def test_raw_get_kamervraag_by_id(self):
        id = "0d7cf75c-8bcc-40f5-ab12-ba856141160d"
        kamervraag = self.api.get_item(Kamervraag, id, params={'$expand': 'Zaak', })
        kamervraag.print_json()
        self.assertEqual('2013D00041', kamervraag.nummer)


class TestKamervragen(TKApiTestCase):

    def test_get_kamervragen_2013(self):
        start_datetime = datetime.datetime(year=2013, month=1, day=1)
        end_datetime = datetime.datetime(year=2013, month=1, day=7)
        pd_filter = Document.create_filter()
        pd_filter.filter_date_range(start_datetime, end_datetime)
        pd_filter.filter_soort('Schriftelijke vragen')
        schriftelijke_vragen = self.api.get_documenten(pd_filter)
        kamervragen_no_zaak = []
        for kamervraag in schriftelijke_vragen:
            print(kamervraag.id)
            # kamervraag.print_json()
            if not kamervraag.zaken:
                kamervragen_no_zaak.append(kamervraag)
        print('kamervragen without zaak: ' + str(len(kamervragen_no_zaak)))
        self.assertEqual(0, len(kamervragen_no_zaak))


class TestKamervraagItem(TKApiTestCase):

    def test_get_kamervragen_new(self):
        start_datetime = datetime.datetime(year=2015, month=1, day=1)
        end_datetime = datetime.datetime(year=2015, month=1, day=7)
        kv_filter = Document.create_filter()
        kv_filter.filter_date_range(start_datetime, end_datetime)
        kamervragen = self.api.get_kamervragen(kv_filter)
        self.assertEqual(len(kamervragen), 17)

    def test_get_kamervragen_old(self):
        start_datetime = datetime.datetime(year=2008, month=7, day=1)
        end_datetime = datetime.datetime(year=2008, month=7, day=10)
        kv_filter = Document.create_filter()
        kv_filter.filter_date_range(start_datetime, end_datetime)
        kamervragen = self.api.get_kamervragen(kv_filter)
        self.assertEqual(len(kamervragen), 20)

    def test_get_kamervragen_2013(self):
        start_datetime = datetime.datetime(year=2013, month=1, day=31)
        end_datetime = datetime.datetime(year=2013, month=2, day=1)
        kv_filter = Document.create_filter()
        kv_filter.filter_date_range(start_datetime, end_datetime)
        kamervragen = self.api.get_kamervragen(kv_filter)


class TestAntwoordItem(TKApiTestCase):

    def test_get_antwoorden_new(self):
        start_datetime = datetime.datetime(year=2015, month=1, day=1)
        end_datetime = datetime.datetime(year=2015, month=1, day=10)
        kv_filter = Document.create_filter()
        kv_filter.filter_date_range(start_datetime, end_datetime)
        antwoorden = self.api.get_antwoorden(kv_filter)
        self.assertEqual(len(antwoorden), 10)

    def test_get_antwoorden_2010(self):
        start_datetime = datetime.datetime(year=2010, month=1, day=1)
        end_datetime = datetime.datetime(year=2010, month=1, day=10)
        kv_filter = Document.create_filter()
        kv_filter.filter_date_range(start_datetime, end_datetime)
        antwoorden = self.api.get_antwoorden(kv_filter)
        self.assertEqual(len(antwoorden), 2)

    # NOTE: this test fails because there is no 'Aanhanselnummer' in the document to create the url
    # def test_get_antwoorden_2008(self):
    #     start_datetime = datetime.datetime(year=2008, month=7, day=1)
    #     end_datetime = datetime.datetime(year=2008, month=12, day=1)
    #     antwoorden = get_antwoorden(start_datetime, end_datetime)
    #     print(len(antwoorden))
    #     for antwoord in antwoorden:
    #         print(antwoord.document_url)
