import datetime
import unittest

from tkapi import api
from tkapi.zaak import ZaakFilter
from tkapi.dossier import Dossier
from tkapi.dossier import DossierFilter


class TestDossier(unittest.TestCase):

    def test_get_dossiers(self):
        dossiers = api.get_dossiers(filter=None, max_items=10)
        for dossier in dossiers:
            dossier.print_json()

    def test_get_dossier_by_vetnummer(self):
        vetnummer = 34435
        filter = DossierFilter()
        filter.filter_vetnummer(vetnummer)
        dossiers = api.get_dossiers(filter=filter)
        self.assertEqual(len(dossiers), 1)
        dossiers[0].print_json()

    def test_dossier_filter(self):
        self.check_dossier_filter('2016Z16486', 34537)
        self.check_dossier_filter('2016Z24906', 34640)

    def check_dossier_filter(self, zaak_nr, expected_dossier_vetnummer):
        dossier_filter = DossierFilter()
        dossier_filter.filter_zaak(zaak_nr)
        dossiers = api.get_dossiers(filter=dossier_filter)
        for dossier in dossiers:
            dossier.print_json()
        self.assertEqual(len(dossiers), 1)
        # print(dossiers[0].vetnummer)
        self.assertEqual(dossiers[0].vetnummer, expected_dossier_vetnummer)


class TestDossiersForZaken(unittest.TestCase):
    start_datetime = datetime.datetime(year=2016, month=1, day=1)
    end_datetime = datetime.datetime(year=2016, month=4, day=1)

    def test_get_dossiers(self):
        zaak_filter = ZaakFilter()
        zaak_filter.filter_date_range(
            TestDossiersForZaken.start_datetime,
            TestDossiersForZaken.end_datetime
        )
        zaak_filter.filter_soort('Wetgeving')
        zaken = api.get_zaken(zaak_filter)

        print('Wetgeving zaken found: ' + str(len(zaken)))

        dossier_filter = DossierFilter()
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
        dossier_filter = DossierFilter()
        dossier_filter.filter_afgesloten(True)
        dossiers = api.get_dossiers(filter=dossier_filter)
        self.assertEqual(len(dossiers), 0)  # There are currently no afgesloten dossiers, this will hopefully change in the future
