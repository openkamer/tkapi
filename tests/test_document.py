import datetime

from tkapi.document import Document
from tkapi.document import DocumentSoort
from tkapi.document import VerslagAlgemeenOverleg
from tkapi.document import DocumentActor
from tkapi.document import DocumentVersie

from .core import TKApiTestCase


class TestSingleDocument(TKApiTestCase):

    def test_get_voorstel_van_wet(self):
        pds = self.api.get_documenten(max_items=1)
        self.assertEqual(1, len(pds))
        pd = pds[0]
        print(pd.bestand_url)
        for agendapunt in pd.agendapunten:
            print(agendapunt.id)
        for dossier in pd.dossiers:
            print(dossier.id)
        self.assertGreaterEqual(len(pd.versies), 1)
        for versie in pd.versies:
            self.assertIsNotNone(versie.nummer)

    def test_document_actors(self):
        max_items = 10
        docs = self.api.get_documenten(max_items=max_items)
        self.assertEqual(max_items, len(docs))
        for doc in docs:
            for actor in doc.actors:
                print(actor.naam)
                print('persoon', actor.persoon)
                print('fractie', actor.fractie)


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

    def test_filter_aanghangselnummer(self):
        aanhangselnummer = '171800824'
        filter = Document.create_filter()
        filter.filter_aanhangselnummer(aanhangselnummer)
        docs = self.api.get_documenten(filter=filter, max_items=10)
        self.assertEqual(1, len(docs))
        self.assertEqual(aanhangselnummer, docs[0].aanhangselnummer)

    def test_filter_nummer(self):
        documentnummer = '2017D38932'
        filter = Document.create_filter()
        filter.filter_nummer(documentnummer)
        docs = self.api.get_documenten(filter=filter, max_items=10)
        self.assertEqual(1, len(docs))
        self.assertEqual(documentnummer, docs[0].nummer)

    def test_filter_alias(self):
        alias = '2060719420'
        filter = Document.create_filter()
        filter.filter_alias(alias)
        docs = self.api.get_documenten(filter=filter, max_items=10)
        self.assertEqual(1, len(docs))
        self.assertEqual(alias, docs[0].alias)

    def test_filter_vergaderjaar(self):
        vergaderjaar = '2006-2007'
        filter = Document.create_filter()
        filter.filter_vergaderjaar(vergaderjaar)
        max_items = 10
        docs = self.api.get_documenten(filter=filter, max_items=max_items)
        self.assertEqual(max_items, len(docs))
        for doc in docs:
            self.assertEqual(vergaderjaar, doc.vergaderjaar)

    def test_filter_volgnummer(self):
        volgnummer = -1
        filter = Document.create_filter()
        filter.filter_volgnummer(volgnummer)
        max_items = 10
        docs = self.api.get_documenten(filter=filter, max_items=max_items)
        self.assertEqual(max_items, len(docs))
        for doc in docs:
            self.assertEqual(volgnummer, doc.volgnummer)


class TestDocumentSoorten(TKApiTestCase):

    def test_all_soorten_2010(self):
        pd_filter = Document.create_filter()
        start_datetime = datetime.datetime(year=2010, month=1, day=1)
        end_datetime = datetime.datetime(year=2010, month=2, day=1)
        pd_filter.filter_date_range(start_datetime, end_datetime)
        pds = self.api.get_documenten(pd_filter)
        soorten = set([pd.soort for pd in pds])
        for soort in soorten:
            self.assertIn(soort, DocumentSoort)
            print(soort)

    def test_all_soorten_2025(self):
        pd_filter = Document.create_filter()
        start_datetime = datetime.datetime(year=2025, month=1, day=1)
        end_datetime = datetime.datetime(year=2025, month=2, day=1)
        pd_filter.filter_date_range(start_datetime, end_datetime)
        pds = self.api.get_documenten(pd_filter)
        exceptions = []
        soorten_list = []
        for pd in pds:
            try:
                soorten_list.append(pd.soort)
            except Exception as e:
                exceptions.append((pd, e))
        soorten = set(soorten_list)
        if exceptions:
            print(f"Caught {len(exceptions)} exception(s) during set creation:")
            for pd, exc in exceptions:
                print(f"  Exception for document {pd}: {type(exc).__name__}: {exc}")
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


class TestDocumentActor(TKApiTestCase):

    def test_get_item(self):
        max_items = 1
        actors = self.api.get_items(DocumentActor, max_items=max_items)
        actor = actors[0]
        print(actor.naam, actor.naam_fractie, actor.functie)
        self.assertEqual(max_items, len(actors))

    def test_get_items(self):
        max_items = 10
        actors = self.api.get_items(DocumentActor, max_items=max_items)
        self.assertEqual(max_items, len(actors))
        for actor in actors:
            print(actor.naam, actor.naam_fractie)
            print(actor.persoon.achternaam)
            print(actor.fractie)


class TestDocumentVersie(TKApiTestCase):

    def test_get_item(self):
        max_items = 1
        versions = self.api.get_items(DocumentVersie, max_items=max_items)
        self.assertEqual(max_items, len(versions))
        version = versions[0]
        print(version.status, version.nummer, version.bestandsgrootte, version.datum, version.document.onderwerp)
