import datetime

from tkapi.kamervraag import Kamervraag
from tkapi.document import Document
from tkapi.document import DocumentSoort
from tkapi.zaak import ZaakSoort
from tkapi.util.document import get_overheidnl_url

from .core import TKApiTestCase


class TestRawApiKamerVraag(TKApiTestCase):

    def test_me(self):
        self.assertTrue(True)

    def test_kamervraag_first(self):
        kamervraag = self.api.get_items(Kamervraag, max_items=1)[0]
        kamervraag.print_json()
        self.assertTrue(kamervraag.onderwerp)


class TestKamervragen(TKApiTestCase):

    def test_get_kamervragen_2013(self):
        start_datetime = datetime.datetime(year=2013, month=1, day=1)
        end_datetime = datetime.datetime(year=2013, month=1, day=7)
        pd_filter = Document.create_filter()
        pd_filter.filter_date_range(start_datetime, end_datetime)
        pd_filter.filter_soort(ZaakSoort.SCHRIFTELIJKE_VRAGEN.value)
        schriftelijke_vragen = self.api.get_documenten(pd_filter)
        kamervragen_no_zaak = []
        for kamervraag in schriftelijke_vragen:
            print(kamervraag.id)
            # kamervraag.print_json()
            if not kamervraag.zaken:
                kamervragen_no_zaak.append(kamervraag)
        print('kamervragen without zaak: ' + str(len(kamervragen_no_zaak)))
        self.assertEqual(0, len(kamervragen_no_zaak))

    def test_get_kamervraag_antwoord(self):
        begin_datetime = datetime.datetime(year=2015, month=1, day=1)
        end_datetime = datetime.datetime(year=2015, month=1, day=5)
        kv_filter = Document.create_filter()
        kv_filter.filter_date_range(begin_datetime, end_datetime)
        kamervragen = self.api.get_kamervragen(kv_filter)
        for kamervraag in kamervragen:
            self.assertEqual(DocumentSoort.ANTWOORD_SCHRIFTELIJKE_VRAGEN, kamervraag.antwoord.soort)
            if kamervraag.mededeling_uitstel:
                self.assertEqual(DocumentSoort.MEDEDELING_UITSTEL_ANTWOORD, kamervraag.mededeling_uitstel.soort)
        content_html_url = get_overheidnl_url(kamervragen[0])
        self.assertTrue(content_html_url)
        content_html_url = get_overheidnl_url(kamervragen[0].antwoord)
        self.assertTrue(content_html_url)


class TestKamervraagItem(TKApiTestCase):

    def test_get_kamervragen_new(self):
        start_datetime = datetime.datetime(year=2015, month=1, day=1)
        end_datetime = datetime.datetime(year=2015, month=1, day=7)
        kv_filter = Document.create_filter()
        kv_filter.filter_date_range(start_datetime, end_datetime)
        kamervragen = self.api.get_kamervragen(kv_filter)
        self.assertEqual(17, len(kamervragen))

    def test_get_kamervragen_old(self):
        start_datetime = datetime.datetime(year=2008, month=7, day=1)
        end_datetime = datetime.datetime(year=2008, month=7, day=10)
        kv_filter = Document.create_filter()
        kv_filter.filter_date_range(start_datetime, end_datetime)
        kamervragen = self.api.get_kamervragen(kv_filter)
        self.assertEqual(20, len(kamervragen))

    def test_get_kamervragen_2013(self):
        start_datetime = datetime.datetime(year=2013, month=1, day=31)
        end_datetime = datetime.datetime(year=2013, month=2, day=1)
        kv_filter = Document.create_filter()
        kv_filter.filter_date_range(start_datetime, end_datetime)
        kamervragen = self.api.get_kamervragen(kv_filter)
        self.assertEqual(23, len(kamervragen))


class TestAntwoordItem(TKApiTestCase):

    def test_get_antwoorden_new(self):
        start_datetime = datetime.datetime(year=2015, month=1, day=1)
        end_datetime = datetime.datetime(year=2015, month=1, day=10)
        kv_filter = Document.create_filter()
        kv_filter.filter_date_range(start_datetime, end_datetime)
        antwoorden = self.api.get_antwoorden(kv_filter)
        self.assertEqual(10, len(antwoorden))

    def test_get_antwoorden_2010(self):
        start_datetime = datetime.datetime(year=2010, month=1, day=1)
        end_datetime = datetime.datetime(year=2010, month=1, day=10)
        kv_filter = Document.create_filter()
        kv_filter.filter_date_range(start_datetime, end_datetime)
        antwoorden = self.api.get_antwoorden(kv_filter)
        self.assertEqual(2, len(antwoorden))
