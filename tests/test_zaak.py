import datetime

from tkapi.zaak import Zaak
from tkapi.zaak import ZaakActor
from tkapi.zaak import ZaakActorRelatieSoort
from tkapi.zaak import ZaakSoort
from tkapi.zaak import ZaakMotie
from tkapi.zaak import ZaakAmendement
from tkapi.zaak import KabinetsAppreciatie

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

    def test_zaak_attributes(self):
        onderwerp = "Selectie aan de poort bij steeds meer universitaire studies"
        zaak_filter = Zaak.create_filter()
        zaak_filter.filter_onderwerp(onderwerp)
        zaken = self.api.get_zaken(zaak_filter)
        self.assertGreaterEqual(len(zaken), 1)
        zaak = zaken[0]
        self.assertEqual(zaak.onderwerp, onderwerp)
        self.assertGreaterEqual(len(zaak.documenten), 3)
        self.assertTrue(zaak.actors)
        self.assertEqual('', zaak.alias)
        self.assertIsNone(zaak.vervangen_door)

    def test_zaak_filter_onderwerp(self):
        onderwerp = "Selectie aan de poort bij steeds meer universitaire studies"
        zaak_filter = Zaak.create_filter()
        zaak_filter.filter_onderwerp(onderwerp)
        zaken = self.api.get_zaken(zaak_filter)
        self.assertEqual(len(zaken), 1)
        self.assertEqual(zaken[0].onderwerp, onderwerp)
        zaken[0].print_json()

    def test_zaak_filter_volgnummer(self):
        volgnummer = 60
        zaak_filter = Zaak.create_filter()
        zaak_filter.filter_volgnummer(volgnummer=volgnummer)
        zaken = self.api.get_zaken(zaak_filter)
        self.assertGreaterEqual(len(zaken), 368)
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

    def test_zaak_filter_empty_activiteit(self):
        start_datetime = datetime.datetime(year=2016, month=1, day=1)
        end_datetime = datetime.datetime(year=2016, month=2, day=1)
        zaak_filter = Zaak.create_filter()
        zaak_filter.filter_date_range(start_datetime, end_datetime)
        zaak_filter.filter_has_activiteit()
        # zaak_filter.filter_soort('Wetgeving')
        zaken = self.api.get_zaken(zaak_filter)
        print('Zaken without activiteit', len(zaken))
        self.assertTrue(len(zaken) > 50)

    def test_zaak_filter_empty_agendapunt(self):
        start_datetime = datetime.datetime(year=2016, month=1, day=1)
        end_datetime = datetime.datetime(year=2016, month=1, day=10)
        zaak_filter = Zaak.create_filter()
        zaak_filter.filter_date_range(start_datetime, end_datetime)
        zaak_filter.filter_has_agendapunt()
        # zaak_filter.filter_soort('Wetgeving')
        zaken = self.api.get_zaken(zaak_filter)
        print('Zaken without agendapunt', len(zaken))
        self.assertTrue(len(zaken) > 50)


class TestZaakActor(TKApiTestCase):

    def test_get_item(self):
        max_items = 1
        actors = self.api.get_items(ZaakActor, max_items=max_items)
        self.assertEqual(max_items, len(actors))
        actor = actors[0]
        self.assertIsNotNone(actor.id)
        self.assertTrue(actor.naam)
        self.assertTrue(actor.zaak.id)

    def test_filter(self):
        max_items = 10
        ind_filter = ZaakActor.create_filter()
        actors = self.api.get_items(ZaakActor, filter=ind_filter, max_items=max_items)

    def test_get_items(self):
        max_items = 10
        actors = self.api.get_items(ZaakActor, max_items=max_items)
        self.assertEqual(max_items, len(actors))
        actor = actors[0]
        self.assertEqual(max_items, len(actors))
        for actor in actors:
            self.assertIn(actor.relatie, ZaakActorRelatieSoort)
            print(' | '.join([actor.naam, actor.afkorting, str(actor.relatie)]))


class TestZaakSoort(TKApiTestCase):

    def test_zaak_soorten_enum(self):
        max_items = 1
        for soort in ZaakSoort:
            zaak_filter = Zaak.create_filter()
            zaak_filter.filter_soort(soort)
            zaken = self.api.get_zaken(filter=zaak_filter, max_items=max_items)
            self.assertEqual(max_items, len(zaken))
            self.assertEqual(soort, zaken[0].soort)


class TestZaakMotie(TKApiTestCase):

    def test_get_motie_zaken(self):
        max_items = 10
        zaak_filter = ZaakMotie.create_filter()
        zaak_filter.filter_has_besluit()
        motie_zaken = self.api.get_items(ZaakMotie, filter=zaak_filter, max_items=max_items)
        for zaak in motie_zaken:
            self.assertEqual(zaak.soort, ZaakSoort.MOTIE)
            print(zaak.besluit_text)
            if zaak.stemmingen:
                print('number of stemmingen:', len(zaak.stemmingen))


class TestZaakAmendement(TKApiTestCase):

    def test_get_amendement_zaken(self):
        max_items = 10
        zaak_filter = ZaakAmendement.create_filter()
        zaak_filter.filter_has_besluit()
        motie_zaken = self.api.get_items(ZaakAmendement, filter=zaak_filter, max_items=max_items)
        for zaak in motie_zaken:
            self.assertEqual(zaak.soort, ZaakSoort.AMENDEMENT)
            print(zaak.besluit_text)
            if zaak.stemmingen:
                print('number of stemmingen:', len(zaak.stemmingen))


class TestZaakKabinetsappreciatie(TKApiTestCase):

    def test_get_zaak_with_kabinetsappreciatie(self):
        max_items = 10
        zaak_filter = ZaakMotie.create_filter()
        begin_datetime = datetime.datetime(year=2019, month=4, day=1)
        end_datetime = datetime.datetime(year=2019, month=6, day=1)
        zaak_filter.filter_date_range(start_datetime=begin_datetime, end_datetime=end_datetime)
        zaken = self.api.get_items(ZaakMotie, filter=zaak_filter, max_items=max_items)
        self.assertEqual(max_items, len(zaken))
        for zaak in zaken:
            self.assertIsNotNone(zaak.kabinetsappreciatie)

    def test_filter_zaak_kabinetsappreciatie(self):
        max_items = 10
        zaak_filter = ZaakMotie.create_filter()
        begin_datetime = datetime.datetime(year=2019, month=4, day=1)
        end_datetime = datetime.datetime(year=2019, month=6, day=1)
        zaak_filter.filter_date_range(start_datetime=begin_datetime, end_datetime=end_datetime)
        zaak_filter.filter_kabinetsappreciatie(KabinetsAppreciatie.ONTRADEN)
        zaken = self.api.get_items(ZaakMotie, filter=zaak_filter, max_items=max_items)
        self.assertEqual(max_items, len(zaken))
        for zaak in zaken:
            self.assertIsNotNone(zaak.kabinetsappreciatie)
            self.assertEqual(zaak.kabinetsappreciatie, KabinetsAppreciatie.ONTRADEN)
