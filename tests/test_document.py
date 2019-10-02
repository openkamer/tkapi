import datetime

from orderedset import OrderedSet

from tkapi.document import Document
from tkapi.document import DocumentSoort
from tkapi.document import VerslagAlgemeenOverleg
from tkapi.util import queries

from .core import TKApiTestCase


class TestSingleDocument(TKApiTestCase):

    def test_get_voorstel_van_wet(self):
        pds = self.api.get_documenten(max_items=1)
        self.assertEqual(1, len(pds))
        pd = pds[0]
        print(pd.bestand_url)
        for agendapunt in pd.agendapunten:
            print(agendapunt)
        for dossier in pd.dossiers:
            print(dossier)


class TestDocumentResource(TKApiTestCase):

    def test_get_resource_url(self):
        pds = self.api.get_documenten(max_items=1)
        self.assertEqual(1, len(pds))
        pd = pds[0]
        self.assertTrue('TK.DA.GGM.OData.Resource()' in pd.bestand_url)


class TestDocument(TKApiTestCase):
    start_datetime = datetime.datetime(year=2017, month=1, day=1)
    end_datetime = datetime.datetime(year=2017, month=1, day=14)

    def test_get_voorstel_van_wet(self):
        pd_filter = Document.create_filter()
        pd_filter.filter_date_range(
            TestDocument.start_datetime,
            TestDocument.end_datetime
        )
        pd_filter.filter_soort(DocumentSoort.VOORSTEL_VAN_WET, is_or=True)
        pd_filter.filter_soort(DocumentSoort.VOORSTEL_VAN_WET_INITIATIEFVOORSTEL, is_or=True)
        pds = self.api.get_documenten(pd_filter)
        for pd in pds:
            print(pd.titel)
        self.assertGreater(len(pds), 253)


class TestDocumentFilter(TKApiTestCase):

    def test_filter_empty_zaak(self):
        pd_filter = Document.create_filter()
        start_datetime = datetime.datetime(year=2017, month=1, day=1)
        end_datetime = datetime.datetime(year=2017, month=2, day=1)
        pd_filter.filter_date_range(
            start_datetime,
            end_datetime
        )
        pd_filter.filter_soort(DocumentSoort.VOORSTEL_VAN_WET)
        pd_filter.filter_non_empty_zaak()
        pds = self.api.get_documenten(pd_filter)
        for pd in pds:
            print(pd.titel)
            for zaak in pd.zaken:
                self.assertTrue(zaak.id)
                # print(zaak)
        print(len(pds))
        self.assertEqual(10, len(pds))

    def test_filter_empty_agendapunt(self):
        pd_filter = Document.create_filter()
        start_datetime = datetime.datetime(year=2017, month=1, day=1)
        end_datetime = datetime.datetime(year=2018, month=1, day=1)
        pd_filter.filter_date_range(
            start_datetime,
            end_datetime
        )
        pd_filter.filter_has_agendapunt()
        pds = self.api.get_documenten(pd_filter)
        for pd in pds:
            print(pd.titel)
            for zaak in pd.zaken:
                print(zaak)
        print(len(pds))
        self.assertEqual(4, len(pds))

    def test_filter_dossier(self):
        dossier_nummer = 31239
        expected = 262
        documenten = queries.get_dossier_documenten(dossier_nummer)
        self.assertGreaterEqual(len(documenten), expected)

    def test_filter_dossier_with_activiteit(self):
        dossier_nummer = 31239
        expected = 10
        documenten = queries.get_dossier_documenten_with_activiteit(dossier_nummer)
        self.assertGreaterEqual(len(documenten), expected)


class TestDocumentSoorten(TKApiTestCase):

    def test_all_soorten(self):
        pd_filter = Document.create_filter()
        start_datetime = datetime.datetime(year=2010, month=1, day=1)
        end_datetime = datetime.datetime(year=2010, month=2, day=1)
        pd_filter.filter_date_range(start_datetime, end_datetime)
        pds = self.api.get_documenten(pd_filter)
        soorten = set([pd.soort for pd in pds])
        for soort in soorten:
            self.assertIn(soort, DocumentSoort)
            print(soort)


class TestDocumentTitel(TKApiTestCase):

    def test_filter_titel(self):
        titel = 'Wijziging van de Warmtewet (wijzigingen naar aanleiding van de evaluatie van de Warmtewet)'
        pd_filter = Document.create_filter()
        pd_filter.filter_titel(titel)
        pds = self.api.get_documenten(pd_filter)
        self.assertGreater(len(pds), 35)
        for pd in pds:
            self.assertEqual(pd.titel, titel)
        # for pd in pds:
        #     pd.print_json()


class TestVerslagAlgemeenOverleg(TKApiTestCase):

    def test_get_verslagen_algemeen_overleg(self):
        start_datetime = datetime.datetime(year=2015, month=1, day=1)
        end_datetime = datetime.datetime(year=2015, month=1, day=20)
        v_filter = VerslagAlgemeenOverleg.create_filter()
        v_filter.filter_date_range(start_datetime, end_datetime)
        verslagen = self.api.get_verslagen_van_algemeen_overleg(v_filter)
        print('verslagen found:',  len(verslagen))
        self.assertEqual(18, len(verslagen))

    def test_get_verslagen_algemeen_overleg_commissie_namen(self):
        expected_verslagen = 6
        start_datetime = datetime.datetime(year=2018, month=1, day=1)
        end_datetime = datetime.datetime(year=2018, month=1, day=10)
        filter = VerslagAlgemeenOverleg.create_filter()
        filter.filter_date_range(start_datetime, end_datetime)
        verslagen = self.api.get_verslagen_van_algemeen_overleg(filter)
        print('verslagen gevonden:', len(verslagen))
        self.assertEqual(expected_verslagen, len(verslagen))
        for verslag in verslagen:
            self.assertEqual(1, len(verslag.voortouwcommissie_namen))
            for naam in verslag.voortouwcommissie_namen:
                print(naam)
                self.assertNotEqual('', naam)
                self.assertNotEqual(None, naam)
