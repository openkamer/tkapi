import unittest
import datetime

from tkapi import api
from tkapi.zaak import Zaak


class TestZaak(unittest.TestCase):
    start_datetime = datetime.datetime(year=2016, month=1, day=1)
    end_datetime = datetime.datetime(year=2016, month=4, day=1)

    def test_zaak_filters(self):
        zaak_filter = Zaak.create_filter()
        zaak_filter.filter_date_range(TestZaak.start_datetime, TestZaak.end_datetime)
        zaak_filter.filter_soort('Wetgeving')
        zaken = api.get_zaken(zaak_filter)
        # for zaak in zaken:
        #     zaak.print_json()
        self.assertEqual(len(zaken), 27)

        zaak_filter.add_afgedaan(True)
        zaken_afgedaan = api.get_zaken(zaak_filter)
        # for zaak in zaken_afgedaan:
        #     zaak.print_json()

        zaak_filter.update_afgedaan(False)
        zaken_aanhangig = api.get_zaken(zaak_filter)
        # for zaak in zaken_aanhangig:
        #     zaak.print_json()

        n_afgedaan = len(zaken_afgedaan)
        n_aanhangig = len(zaken_aanhangig)
        print('aanhangig: ' + str(n_aanhangig))
        print('afgedaan: ' + str(n_afgedaan))
        self.assertEqual(n_aanhangig + n_afgedaan, len(zaken))

    def test_zaak_for_onderwerp(self):
        onderwerp = "Selectie aan de poort bij steeds meer universitaire studies"
        zaak_filter = Zaak.create_filter()
        zaak_filter.filter_onderwerp(onderwerp)
        zaken = api.get_zaken(zaak_filter)
        self.assertEqual(len(zaken), 1)
        self.assertEqual(zaken[0].onderwerp, onderwerp)
        zaken[0].print_json()

    def test_zaken_for_date_range(self):
        zaak_filter = Zaak.create_filter()
        zaak_filter.filter_date_range(TestZaak.start_datetime, TestZaak.end_datetime)
        zaken = api.get_zaken(zaak_filter)
        soorten = set()
        for zaak in zaken:
            # zaak.print_json()
            soorten.add(zaak.soort)
            # print(zaak.soort)
        for soort in soorten:
            print(soort)

    def test_zaak_nummer(self):
        zaak_nummer = '2007Z01002'
        zaak_filter = Zaak.create_filter()
        zaak_filter.filter_nummer(zaak_nummer)
        zaken = api.get_zaken(zaak_filter)
        self.assertEqual(len(zaken), 1)
        zaak = zaken[0]
        self.assertEqual(zaak.nummer, zaak_nummer)
        zaak.print_json()


class TestZaakRelations(unittest.TestCase):

    # def test_zaak_filter_empty_besluiten(self):
    #     zaak_filter = Zaak.create_filter()
    #     zaak_filter.filter_empty_besluit()
    #     zaken = api.get_zaken(zaak_filter)
    #     self.assertEqual(len(zaken), 0)

    def test_zaak_filter_empty_activiteit(self):
        start_datetime = datetime.datetime(year=2016, month=1, day=1)
        end_datetime = datetime.datetime(year=2016, month=2, day=1)
        zaak_filter = Zaak.create_filter()
        zaak_filter.filter_date_range(start_datetime, end_datetime)
        zaak_filter.filter_empty_activiteit()
        # zaak_filter.filter_soort('Wetgeving')
        zaken = api.get_zaken(zaak_filter)
        print('Zaken without activiteit', len(zaken))
        self.assertTrue(len(zaken) > 50)

    def test_zaak_filter_empty_agendapunt(self):
        start_datetime = datetime.datetime(year=2016, month=1, day=1)
        end_datetime = datetime.datetime(year=2016, month=1, day=10)
        zaak_filter = Zaak.create_filter()
        zaak_filter.filter_date_range(start_datetime, end_datetime)
        zaak_filter.filter_empty_agendapunt()
        # zaak_filter.filter_soort('Wetgeving')
        zaken = api.get_zaken(zaak_filter)
        print('Zaken without agendapunt', len(zaken))
        self.assertTrue(len(zaken) > 50)
