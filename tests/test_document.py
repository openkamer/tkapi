import datetime

from orderedset import OrderedSet

from tkapi.document import ParlementairDocument

from .core import TKApiTestCase


class TestSingleParlementairDocument(TKApiTestCase):

    def test_get_voorstel_van_wet(self):
        pds = self.api.get_parlementaire_documenten(max_items=1)
        self.assertEqual(1, len(pds))
        pd = pds[0]
        # pd.print_json()
        for zaak in pd.zaken:
            print(zaak)
        print(pd.kamerstuk)
        for agendapunt in pd.agendapunten:
            print(agendapunt)
        for dossier in pd.dossiers:
            print(dossier)


class TestParlementairDocument(TKApiTestCase):
    start_datetime = datetime.datetime(year=2017, month=1, day=1)
    end_datetime = datetime.datetime(year=2017, month=1, day=14)

    def test_get_voorstel_van_wet(self):
        pd_filter = ParlementairDocument.create_filter()
        pd_filter.filter_date_range(
            TestParlementairDocument.start_datetime,
            TestParlementairDocument.end_datetime
        )
        pd_filter.filter_soort('Voorstel van wet', is_or=True)
        pd_filter.filter_soort('Voorstel van wet (initiatiefvoorstel)', is_or=True)
        pds = self.api.get_parlementaire_documenten(pd_filter)
        for pd in pds:
            print(pd.titel)
        self.assertGreater(len(pds), 253)


class TestParlementairDocumentFilter(TKApiTestCase):

    def test_filter_empty_zaak(self):
        pd_filter = ParlementairDocument.create_filter()
        start_datetime = datetime.datetime(year=2017, month=1, day=1)
        end_datetime = datetime.datetime(year=2017, month=2, day=1)
        pd_filter.filter_date_range(
            start_datetime,
            end_datetime
        )
        pd_filter.filter_soort('Voorstel van wet')
        pd_filter.filter_non_empty_zaak()
        pds = self.api.get_parlementaire_documenten(pd_filter)
        for pd in pds:
            print(pd.titel)
            for zaak in pd.zaken:
                print(zaak)
        print(len(pds))
        self.assertEqual(8, len(pds))

    def test_filter_empty_agendapunt(self):
        pd_filter = ParlementairDocument.create_filter()
        start_datetime = datetime.datetime(year=2017, month=1, day=1)
        end_datetime = datetime.datetime(year=2018, month=1, day=1)
        pd_filter.filter_date_range(
            start_datetime,
            end_datetime
        )
        pd_filter.filter_empty_agendapunt()
        pds = self.api.get_parlementaire_documenten(pd_filter)
        for pd in pds:
            print(pd.titel)
            for zaak in pd.zaken:
                print(zaak)
        print(len(pds))
        self.assertEqual(4, len(pds))


class TestParlementairDocumentSoorten(TKApiTestCase):

    def test_all_soorten(self):
        pd_filter = ParlementairDocument.create_filter()
        start_datetime = datetime.datetime(year=2010, month=1, day=1)
        end_datetime = datetime.datetime(year=2010, month=2, day=1)
        pd_filter.filter_date_range(start_datetime, end_datetime)
        pds = self.api.get_parlementaire_documenten(pd_filter)
        soorten = [pd.soort for pd in pds]
        soorten = OrderedSet(sorted(soorten))
        for soort in soorten:
            print(soort)


class TestParlementairDocumentTitel(TKApiTestCase):

    def test_filter_titel(self):
        titel = 'Wijziging van de Warmtewet (wijzigingen naar aanleiding van de evaluatie van de Warmtewet)'
        pd_filter = ParlementairDocument.create_filter()
        pd_filter.filter_titel(titel)
        pds = self.api.get_parlementaire_documenten(pd_filter)
        self.assertTrue(len(pds) >= 7)
        for pd in pds:
            self.assertEqual(pd.titel, titel)
        # for pd in pds:
        #     pd.print_json()
