import datetime

from orderedset import OrderedSet

from tkapi.document import Document
from tkapi.document import VerslagAlgemeenOverleg

from .core import TKApiTestCase


class TestSingleDocument(TKApiTestCase):

    def test_get_voorstel_van_wet(self):
        pds = self.api.get_documenten(max_items=1)
        self.assertEqual(1, len(pds))
        pd = pds[0]
        # pd.print_json()
        # for zaak in pd.zaken:
        #     print(zaak)
        print(pd.kamerstuk)
        for agendapunt in pd.agendapunten:
            print(agendapunt)
        for dossier in pd.dossiers:
            print(dossier)


class TestDocument(TKApiTestCase):
    start_datetime = datetime.datetime(year=2017, month=1, day=1)
    end_datetime = datetime.datetime(year=2017, month=1, day=14)

    def test_get_voorstel_van_wet(self):
        pd_filter = Document.create_filter()
        pd_filter.filter_date_range(
            TestDocument.start_datetime,
            TestDocument.end_datetime
        )
        pd_filter.filter_soort('Voorstel van wet', is_or=True)
        pd_filter.filter_soort('Voorstel van wet (initiatiefvoorstel)', is_or=True)
        pds = self.api.get_documenten(pd_filter)
        # for pd in pds:
        #     print(pd.titel)
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
        pd_filter.filter_soort('Voorstel van wet')
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
        pd_filter.filter_empty_agendapunt()
        pds = self.api.get_documenten(pd_filter)
        for pd in pds:
            print(pd.titel)
            for zaak in pd.zaken:
                print(zaak)
        print(len(pds))
        self.assertEqual(4, len(pds))


class TestDocumentSoorten(TKApiTestCase):

    def test_all_soorten(self):
        pd_filter = Document.create_filter()
        start_datetime = datetime.datetime(year=2010, month=1, day=1)
        end_datetime = datetime.datetime(year=2010, month=2, day=1)
        pd_filter.filter_date_range(start_datetime, end_datetime)
        pds = self.api.get_documenten(pd_filter)
        soorten = [pd.soort for pd in pds]
        soorten = OrderedSet(sorted(soorten))
        for soort in soorten:
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
        for verslag in verslagen:
            print(verslag.onderwerp)
            if verslag.kamerstuk:
                print(str(verslag.kamerstuk.dossier.nummer) + ', ' + str(verslag.kamerstuk.ondernummer))
                print(verslag.document_url)
            # print(verslag.document_url)
            # verslag.kamerstuk.print_json()
            # print(verslag.dossier.titel)
            # for zaak in verslag.zaken:
                # zaak.print_json()
                # print(zaak)
                # for commissie in zaak.voortouwcommissies:
                #     print(commissie.naam)
            # for activiteit in verslag.activiteiten:
            #     verslag.print_json()
                # print(activiteit.begin.isoformat())
                # print(activiteit.einde.isoformat())
