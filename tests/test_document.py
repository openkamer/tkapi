import datetime
import unittest

from orderedset import OrderedSet

from tkapi import api
from tkapi.document import ParlementairDocument


class TestParlementairDocument(unittest.TestCase):
    start_datetime = datetime.datetime(year=2017, month=1, day=1)
    end_datetime = datetime.datetime(year=2017, month=6, day=1)

    def test_get_voorstel_van_wet(self):
        pd_filter = ParlementairDocument.create_filter()
        pd_filter.filter_date_range(
            TestParlementairDocument.start_datetime,
            TestParlementairDocument.end_datetime
        )
        pd_filter.filter_soort('Voorstel van wet', is_or=True)
        pd_filter.filter_soort('Voorstel van wet (initiatiefvoorstel)', is_or=True)
        # print(pd_filter.filter_str)
        pds = api.get_parlementaire_documenten(pd_filter)
        for pd in pds:
            print(pd.titel)
            print(pd.activiteit)
            # pd.print_json()
            # print('\t' + str(pd.dossier.vetnummer))
            # print('\t dossier afgesloten: ' + str(pd.dossier.afgesloten))
            # pd.dossier.print_json()
            # print(pd.dossier.afgesloten)
            # print(pd.dossier.kamerstukken)
            # for zaak in pd.dossier.zaken:
            #     print('\t zaak afgedaan: ' + str(zaak.afgedaan))
            #     print('\t zaak soort: ' + str(zaak.soort))
            #     print('\t zaak soort: ' + str(zaak.nummer))


class TestParlementairDocumentFilter(unittest.TestCase):

    def test_filter_empty_zaak(self):
        pd_filter = ParlementairDocument.create_filter()
        start_datetime = datetime.datetime(year=2017, month=1, day=1)
        end_datetime = datetime.datetime(year=2017, month=2, day=1)
        pd_filter.filter_date_range(
            start_datetime,
            end_datetime
        )
        pd_filter.filter_soort('Voorstel van wet')
        pd_filter.filter_empty_zaak()
        pds = api.get_parlementaire_documenten(pd_filter)
        for pd in pds:
            print('\n============')
            print(pd.titel)
            for zaak in pd.zaken:
                print(zaak)
        print(len(pds))

    def test_filter_empty_agendapunt(self):
        pd_filter = ParlementairDocument.create_filter()
        start_datetime = datetime.datetime(year=2005, month=1, day=1)
        end_datetime = datetime.datetime.now()
        pd_filter.filter_date_range(
            start_datetime,
            end_datetime
        )
        pd_filter.filter_empty_agendapunt()
        pds = api.get_parlementaire_documenten(pd_filter)
        for pd in pds:
            print('\n============')
            print(pd.titel)
            for zaak in pd.zaken:
                print(zaak)
        print(len(pds))


class TestParlementairDocumentSoorten(unittest.TestCase):

    def test_all_soorten(self):
        pd_filter = ParlementairDocument.create_filter()
        start_datetime = datetime.datetime(year=2010, month=1, day=1)
        end_datetime = datetime.datetime(year=2010, month=2, day=1)
        pd_filter.filter_date_range(
            start_datetime,
            end_datetime
        )
        pds = api.get_parlementaire_documenten(pd_filter)
        soorten = []
        for pd in pds:
            soorten.append(pd.soort)
        soorten = OrderedSet(sorted(soorten))
        for soort in soorten:
            print(soort)


class TestParlementairDocumentTitel(unittest.TestCase):

    def test_filter_titel(self):
        titel = 'Wijziging van de Warmtewet (wijzigingen naar aanleiding van de evaluatie van de Warmtewet)'
        pd_filter = ParlementairDocument.create_filter()
        pd_filter.filter_titel(titel)
        pds = api.get_parlementaire_documenten(pd_filter)
        self.assertTrue(len(pds) >= 7)
        for pd in pds:
            self.assertEqual(pd.titel, titel)
        # for pd in pds:
        #     pd.print_json()
