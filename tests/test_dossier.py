import datetime
import unittest

from orderedset import OrderedSet

from tkapi import api
from tkapi.zaak import Zaak
from tkapi.dossier import Dossier
from tkapi.document import ParlementairDocument


class TestDossier(unittest.TestCase):

    def test_get_dossiers(self):
        dossiers = api.get_dossiers(filter=None, max_items=10)
        for dossier in dossiers:
            dossier.print_json()

    def test_get_dossier_by_vetnummer(self):
        vetnummer = 34435
        filter = Dossier.create_filter()
        filter.filter_vetnummer(vetnummer)
        dossiers = api.get_dossiers(filter=filter)
        self.assertEqual(len(dossiers), 1)
        dossiers[0].print_json()

    def test_dossier_filter(self):
        self.check_dossier_filter('2016Z16486', 34537)
        self.check_dossier_filter('2016Z24906', 34640)

    def check_dossier_filter(self, zaak_nr, expected_dossier_vetnummer):
        dossier_filter = Dossier.create_filter()
        dossier_filter.filter_zaak(zaak_nr)
        dossiers = api.get_dossiers(filter=dossier_filter)
        for dossier in dossiers:
            dossier.print_json()
        self.assertEqual(len(dossiers), 1)
        # print(dossiers[0].vetnummer)
        self.assertEqual(dossiers[0].vetnummer, expected_dossier_vetnummer)


class TestDossierKamerstukken(unittest.TestCase):

    def test_dossier_kamerstukken(self):
        # vetnummer = 34693
        # vetnummer = 34374
        # vetnummer = 34051
        # vetnummer = 22139
        vetnummer = 34723
        dossier_filter = Dossier.create_filter()
        dossier_filter.filter_vetnummer(vetnummer)
        dossiers = api.get_dossiers(filter=dossier_filter)
        self.assertEqual(len(dossiers), 1)
        dossier = dossiers[0]
        kamerstukken = dossier.kamerstukken
        for kamerstuk in kamerstukken:
            print('\n============')
            # kamerstuk.print_json()
            print(kamerstuk.ondernummer)
            document = kamerstuk.parlementair_document
            # document.print_json()
            print(document.soort)
            print(document.titel)
            [print(zaak) for zaak in document.zaken]
            # [zaak.print_json() for zaak in document.zaken]
            for zaak in document.zaken:
                if not zaak.afgedaan:
                    print('NIET GESLOTEN')
            for agendapunt in document.agendapunten:
                agendapunt.print_json()
            for zaak in document.zaken:
                if zaak['Besluit']:
                    zaak.print_json()
                # for activiteit in zaak.activiteiten:
                #     activiteit.print_json()
                for besluit in zaak.besluiten:
                    # besluit.print_json()
                    besluit.stemming.print_json()
            # for activiteit in document.activiteiten:
            #     activiteit.print_json()


class TestDossiersForZaken(unittest.TestCase):
    start_datetime = datetime.datetime(year=2016, month=1, day=1)
    end_datetime = datetime.datetime(year=2016, month=4, day=1)

    def test_get_dossiers(self):
        zaak_filter = Zaak.create_filter()
        zaak_filter.filter_date_range(
            TestDossiersForZaken.start_datetime,
            TestDossiersForZaken.end_datetime
        )
        zaak_filter.filter_soort('Wetgeving')
        zaken = api.get_zaken(zaak_filter)

        print('Wetgeving zaken found: ' + str(len(zaken)))

        dossier_filter = Dossier.create_filter()
        zaak_nummers = [zaak.nummer for zaak in zaken]
        print(zaak_nummers)
        dossier_filter.filter_zaken(zaak_nummers)
        dossiers = api.get_dossiers(filter=dossier_filter)
        dossier_zaak_nummers = set()
        for dossier in dossiers:
            print('dossier.vetnummer: ', str(dossier.vetnummer))
            # print(dossier.kamerstukken)
            # pds = dossier.parlementaire_documenten
            # print(dossier.parlementaire_documenten)
            for pd in dossier.parlementaire_documenten:
                for zaak in pd.zaken:
                    dossier_zaak_nummers.add(zaak.nummer)
        for zaak in zaken:
            if zaak.nummer not in dossier_zaak_nummers:
                print(zaak.nummer)
                zaak.print_json()
            # self.assertTrue(zaak_nr in dossier_zaak_nummers)
        # print(zaken)


class TestDossierAfgesloten(unittest.TestCase):
    start_datetime = datetime.datetime(year=2015, month=1, day=1)
    end_datetime = datetime.datetime(year=2015, month=1, day=10)

    def test_filter_afgesloten(self):
        dossier_filter = Dossier.create_filter()
        dossier_filter.filter_afgesloten(True)
        dossiers = api.get_dossiers(filter=dossier_filter)
        self.assertEqual(len(dossiers), 0)  # There are currently no afgesloten dossiers, this will hopefully change in the future


class TestWetsvoorstelDossier(unittest.TestCase):

    def test_get_dossiers(self):
        pd_filter = ParlementairDocument.create_filter()
        # start_datetime = datetime.datetime(year=2016, month=1, day=1)
        # end_datetime = datetime.datetime(year=2017, month=6, day=1)
        # pd_filter.filter_date_range(start_datetime, end_datetime)
        pd_filter.filter_soort('Voorstel van wet', is_or=True)
        pd_filter.filter_soort('Voorstel van wet (initiatiefvoorstel)', is_or=True)
        pds = api.get_parlementaire_documenten(pd_filter)

        dossier_nrs = []
        pds_no_dossier_nr = []
        for pd in pds:
            print(pd.dossier_vetnummer)
            if pd.dossier_vetnummer:
                dossier_nrs.append(pd.dossier_vetnummer)
            else:
                pds_no_dossier_nr.append(pd)
        for pd in pds_no_dossier_nr:
            print(pd.nummer)
            print(pd.onderwerp)
            try:
                dossier_nr = int(pd.onderwerp.split('Voorstel van wet')[0].strip())
                dossier_nrs.append(dossier_nr)
            except TypeError:
                continue

        dossier_nrs = OrderedSet(sorted(dossier_nrs))
        print(dossier_nrs)
        for dossier_nr in dossier_nrs:
            print(dossier_nr)
        print(len(dossier_nrs))


    # def test_get_dossiers(self):
    #     zaak_filter = Zaak.create_filter()
    #     start_datetime = datetime.datetime(year=2005, month=1, day=1)
    #     end_datetime = datetime.datetime.now()
    #     zaak_filter.filter_date_range(start_datetime, end_datetime)
    #     zaak_filter.filter_soort('Wetgeving')
    #     zaken = api.get_zaken(zaak_filter)
    #     print('Wetgeving zaken found: ' + str(len(zaken)))
    #     zaak_nummers = [zaak.nummer for zaak in zaken]
    #     print(zaak_nummers)
    #     dossiers = []
    #     nrs_batch = set()
    #     for zaak_nr in zaak_nummers:
    #         nrs_batch.add(zaak_nr)
    #         if len(nrs_batch) < 10:
    #             continue
    #         dossier_filter = Dossier.create_filter()
    #         dossier_filter.filter_zaken(nrs_batch)
    #         nrs_batch = set()
    #         dossiers_for_zaak = api.get_dossiers(filter=dossier_filter)
    #         if dossiers_for_zaak:
    #             dossiers += dossiers_for_zaak
    #             print('Dossier found for zaak: ' + str(zaak_nr))
    #         else:
    #             print('WARNING: No dossier found for zaak: ' + str(zaak_nr))
    #     dossier_vetnummers = []
    #     for dossier in dossiers:
    #         print('\n=======')
    #         print(dossier.vetnummer)
    #         print(dossier.afgesloten)
    #         print(dossier.organisatie)
    #         print(dossier.titel)
    #         dossier_vetnummers.append(dossier.vetnummer)
    #         # dossier.print_json()
    #     dossier_nrs = OrderedSet(sorted(dossier_vetnummers))
    #     print(dossier_nrs)
    #     print(len(dossier_nrs))
