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


class TestZaakIndiener(TKApiTestCase):

    def test_get_first(self):
        ind_filter = ZaakIndiener.create_filter()
        ind_filter.filter_non_empty()
        indieners = self.api.get_items(ZaakMedeindiener, filter=ind_filter, max_items=10)
        # for indiender in indieners:
        #     indiender.print_json()
        for indiender in indieners:
            self.assertTrue(indiender.id)

    def test_get_indiener(self):
        uid = 'c52afcd8-f9b9-4c50-b3e7-e2aa95a1d8d9'
        indiener = self.api.get_item(ZaakIndiener, id=uid)
        self.assertEqual('2a6929b2-58a7-4d5e-9ede-3c877633f96a', indiener.persoon.id)
        self.assertEqual('b00c4984-06f1-44b5-b82c-bd47281ccfb1', indiener.fractie.id)
        self.assertEqual('6d4f0f5e-0ade-4bce-b3cc-9eeb3b5ff988', indiener.zaak.id)

    def test_get_medeindiener(self):
        uid = 'afd0ae9e-d181-4e57-9466-00a4353f2078'
        indiener = self.api.get_item(ZaakMedeindiener, id=uid)
        self.assertEqual('593c7e62-af83-4b59-910e-97ac667a2f49', indiener.persoon.id)
        self.assertEqual('b00c4984-06f1-44b5-b82c-bd47281ccfb1', indiener.fractie.id)
        self.assertEqual('3bdf2c95-0779-4957-be6c-ee26e2394f6c', indiener.zaak.id)


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
