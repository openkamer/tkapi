import datetime

from tkapi.zaak import Zaak
from tkapi.zaak import ZaakIndiener
from tkapi.zaak import ZaakMedeindiener
from tkapi.zaak import ZaakSoort
from tkapi.zaak import ZaakMotie
from tkapi.zaak import ZaakAmendement

from .core import TKApiTestCase


class TestZaak(TKApiTestCase):
    start_datetime = datetime.datetime(year=2016, month=1, day=1)
    end_datetime = datetime.datetime(year=2016, month=4, day=1)

    def test_zaak_filters(self):
        zaak_filter = Zaak.create_filter()
        zaak_filter.filter_date_range(TestZaak.start_datetime, TestZaak.end_datetime)
        zaak_filter.filter_soort(ZaakSoort.WETGEVING)
        zaken = self.api.get_zaken(zaak_filter)
        # for zaak in zaken:
        #     zaak.print_json()
        self.assertEqual(len(zaken), 28)

        zaak_filter.filter_afgedaan(True)
        zaken_afgedaan = self.api.get_zaken(zaak_filter)
        # for zaak in zaken_afgedaan:
        #     zaak.print_json()

        zaak_filter.update_afgedaan(False)
        zaken_aanhangig = self.api.get_zaken(zaak_filter)
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
        zaken = self.api.get_zaken(zaak_filter)
        self.assertEqual(len(zaken), 1)
        self.assertEqual(zaken[0].onderwerp, onderwerp)
        zaken[0].print_json()

    def test_zaken_for_date_range(self):
        zaak_filter = Zaak.create_filter()
        zaak_filter.filter_date_range(TestZaak.start_datetime, TestZaak.end_datetime)
        zaken = self.api.get_zaken(zaak_filter)
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
        zaken = self.api.get_zaken(zaak_filter)
        self.assertEqual(len(zaken), 1)
        zaak = zaken[0]
        self.assertEqual(zaak.nummer, zaak_nummer)
        zaak.print_json()


class TestZaakRelations(TKApiTestCase):

    # def test_zaak_filter_empty_besluiten(self):
    #     zaak_filter = Zaak.create_filter()
    #     zaak_filter.filter_empty_besluit()
    #     zaken = self.api.get_zaken(zaak_filter)
    #     self.assertEqual(len(zaken), 0)

    def test_zaak_filter_empty_activiteit(self):
        start_datetime = datetime.datetime(year=2016, month=1, day=1)
        end_datetime = datetime.datetime(year=2016, month=2, day=1)
        zaak_filter = Zaak.create_filter()
        zaak_filter.filter_date_range(start_datetime, end_datetime)
        zaak_filter.filter_empty_activiteit()
        # zaak_filter.filter_soort('Wetgeving')
        zaken = self.api.get_zaken(zaak_filter)
        print('Zaken without activiteit', len(zaken))
        self.assertTrue(len(zaken) > 50)

    def test_zaak_filter_empty_agendapunt(self):
        start_datetime = datetime.datetime(year=2016, month=1, day=1)
        end_datetime = datetime.datetime(year=2016, month=1, day=10)
        zaak_filter = Zaak.create_filter()
        zaak_filter.filter_date_range(start_datetime, end_datetime)
        zaak_filter.filter_empty_agendapunt()
        # zaak_filter.filter_soort('Wetgeving')
        zaken = self.api.get_zaken(zaak_filter)
        print('Zaken without agendapunt', len(zaken))
        self.assertTrue(len(zaken) > 50)

    # TODO BR: update with v2 (OData V4) uid
    # def test_zaak_vervangen_door(self):
    #     uid = 'bee46617-c7e0-43e1-b6a3-0001a8d402eb'
    #     zaak = self.api.get_item(Zaak, id=uid)
    #     vervangen_zaak = zaak.vervangen_door
    #     self.assertEqual('c4621bc4-5972-4440-beb0-473709846885', vervangen_zaak.id)
    #     self.assertEqual('2016Z04909', vervangen_zaak.nummer)

# TODO BR: update uids
# class TestZaakIndiener(TKApiTestCase):
#
#     def test_get_first(self):
#         indieners = self.api.get_items(ZaakIndiener, max_items=10)
#         for ind in indieners:
#             print(ind.persoon)
#
#     def test_get_indiener(self):
#         uid = '01f9aa67-ee5d-4fcb-a8f3-961d31164977'
#         indiener = self.api.get_item(ZaakIndiener, id=uid)
#         self.assertEqual('287b1e1b-8d2c-405c-828f-2f1405671c2f', indiener.persoon.id)
#         self.assertEqual('8266ae85-5e77-44e9-a8d4-b399b96ca4b2', indiener.fractie.id)
#         self.assertEqual('e8f337b7-ffbc-4fcd-a62c-00079510a0e9', indiener.zaak.id)
#
#     def test_get_medeindiener(self):
#         uid = 'f5a27871-856e-4a15-bce4-5d61460bf5cc'
#         indiener = self.api.get_item(ZaakMedeindiener, id=uid)
#         self.assertEqual('ad21ebf6-352c-4411-a110-95205bfa3126', indiener.persoon.id)
#         self.assertEqual('8266ae85-5e77-44e9-a8d4-b399b96ca4b2', indiener.fractie.id)
#         self.assertEqual('e8f337b7-ffbc-4fcd-a62c-00079510a0e9', indiener.zaak.id)


class TestZaakSoort(TKApiTestCase):

    def test_zaak_soorten_enum(self):
        max_items = 1
        for soort in ZaakSoort:
            zaak_filter = Zaak.create_filter()
            zaak_filter.filter_soort(soort)
            zaken = self.api.get_zaken(filter=zaak_filter, max_items=max_items)
            self.assertEqual(max_items, len(zaken))


class TestZaakMotie(TKApiTestCase):

    def test_get_motie_zaken(self):
        max_items = 10
        zaak_filter = ZaakMotie.create_filter()
        zaak_filter.filter_empty_besluit()
        motie_zaken = self.api.get_items(ZaakMotie, filter=zaak_filter, max_items=max_items)
        for zaak in motie_zaken:
            self.assertEqual(zaak.soort, ZaakSoort.MOTIE.value)
            print(zaak.besluit_text)
            if zaak.stemmingen:
                print('number of stemmingen:', len(zaak.stemmingen))


class TestZaakAmendement(TKApiTestCase):

    def test_get_amendement_zaken(self):
        max_items = 10
        zaak_filter = ZaakAmendement.create_filter()
        zaak_filter.filter_empty_besluit()
        motie_zaken = self.api.get_items(ZaakAmendement, filter=zaak_filter, max_items=max_items)
        for zaak in motie_zaken:
            self.assertEqual(zaak.soort, ZaakSoort.AMENDEMENT.value)
            print(zaak.besluit_text)
            if zaak.stemmingen:
                print('number of stemmingen:', len(zaak.stemmingen))
