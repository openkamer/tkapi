import datetime

from tkapi.util import queries
from tkapi.zaak import Zaak, ZaakSoort
from tkapi.dossier import Dossier, DossierWetsvoorstel
from tkapi.document import Document

from .core import TKApiTestCase


class TestDossier(TKApiTestCase):

    def test_get_dossiers(self):
        dossiers = self.api.get_dossiers(filter=None, max_items=10)
        self.assertEqual(10, len(dossiers))

    def test_get_dossier_by_nummer(self):
        nummer = 34435
        filter = Dossier.create_filter()
        filter.filter_nummer(nummer)
        dossiers = self.api.get_dossiers(filter=filter)
        self.assertEqual(len(dossiers), 1)
        dossiers[0].print_json()

    def test_dossier_filter(self):
        self.check_dossier_filter('2016Z16486', 34537)
        self.check_dossier_filter('2016Z24906', 34640)

    def check_dossier_filter(self, zaak_nr, expected_dossier_nummer):
        dossier_filter = Dossier.create_filter()
        dossier_filter.filter_zaak(zaak_nr)
        dossiers = self.api.get_dossiers(filter=dossier_filter)
        # for dossier in dossiers:
        #     dossier.print_json()
        self.assertEqual(len(dossiers), 1)
        # print(dossiers[0].nummer)
        self.assertEqual(dossiers[0].nummer, expected_dossier_nummer)


class TestDossiersForZaken(TKApiTestCase):
    start_datetime = datetime.datetime(year=2016, month=1, day=1)
    end_datetime = datetime.datetime(year=2016, month=1, day=14)

    def test_get_dossiers(self):
        zaak_filter = Zaak.create_filter()
        zaak_filter.filter_date_range(
            TestDossiersForZaken.start_datetime,
            TestDossiersForZaken.end_datetime
        )
        zaak_filter.filter_soort(ZaakSoort.WETGEVING)
        zaken = self.api.get_zaken(zaak_filter)

        print('Wetgeving zaken found: ' + str(len(zaken)))

        dossier_filter = Dossier.create_filter()
        zaak_nummers = [zaak.nummer for zaak in zaken]
        print(zaak_nummers)
        dossier_filter.filter_zaken(zaak_nummers)
        dossiers = self.api.get_dossiers(filter=dossier_filter)
        dossier_zaak_nummers = set()
        for dossier in dossiers:
            print('dossier.nummer: ', str(dossier.nummer))
            for zaak in dossier.zaken:
                dossier_zaak_nummers.add(zaak.nummer)
        print('dossier_zaak_nummers', dossier_zaak_nummers)
        for zaak in zaken:
            if zaak.nummer not in dossier_zaak_nummers:
                print(zaak.nummer)
                # zaak.print_json()
            # self.assertTrue(zaak_nr in dossier_zaak_nummers)
        # print(zaken)
        for zaak_nummer in zaak_nummers:
            self.assertTrue(zaak_nummer in dossier_zaak_nummers)


class TestDossierAfgesloten(TKApiTestCase):
    start_datetime = datetime.datetime(year=2015, month=1, day=1)
    end_datetime = datetime.datetime.now()

    def test_filter_afgesloten(self):
        dossier_filter = Dossier.create_filter()
        dossier_filter.filter_afgesloten(True)
        dossiers = self.api.get_dossiers(filter=dossier_filter)
        # There are currently no afgesloten dossiers, this will hopefully change in the future
        self.assertEqual(len(dossiers), 0)


class TestDossierFilter(TKApiTestCase):

    def test_filter_dossier_nummer(self):
        nummer = 33885
        dossier = queries.get_dossier(nummer)
        self.assertEqual(nummer, dossier.nummer)

    def test_filter_dossier_nummer_toevoeging(self):
        nummer = 35300
        toevoeging = 'XVI'
        dossier = queries.get_dossier(nummer, toevoeging=toevoeging)
        self.assertEqual(nummer, dossier.nummer)
        self.assertEqual(toevoeging, dossier.toevoeging)

    def test_get_document_actors(self):
        # nummer = 35234
        nummer = 33885
        dossier = queries.get_dossier(nummer)
        for zaak in dossier.zaken:
            print('==========')
            print(zaak.soort, zaak.onderwerp, zaak.volgnummer)
            for actor in zaak.actors:
                print(actor.naam, actor.persoon.achternaam if actor.persoon else None, actor.fractie, actor.commissie)
            for doc in zaak.documenten:
                print(doc.soort, doc.onderwerp, doc.titel, doc.volgnummer)
                for actor in doc.actors:
                    print(actor.naam)


class TestWetsvoorstelDossier(TKApiTestCase):

    def test_get_wetsvoorstellen_dossiers(self):
        max_items = 200
        wetsvoorstellen = self.api.get_items(DossierWetsvoorstel, max_items=max_items)
        self.assertEqual(max_items, len(wetsvoorstellen))

    def test_get_begroting_dossiers(self):
        filter = Zaak.create_filter()
        filter.filter_date_range(datetime.date(year=2019, month=6, day=1), datetime.date.today())
        filter.filter_soort(ZaakSoort.BEGROTING, is_or=True)
        zaken = self.api.get_zaken(filter=filter)
        for zaak in zaken:
            dossier_id = str(zaak.dossier.nummer)
            print(dossier_id)

    def test_get_dossiers_via_documenten(self):
        pd_filter = Document.create_filter()
        # NOTE: this date filter does not seem to work in combination with the soort filter.
        # start_datetime = datetime.datetime(year=2016, month=1, day=1)
        # end_datetime = datetime.datetime(year=2016, month=2, day=1)
        # pd_filter.filter_date_range(start_datetime, end_datetime)
        pd_filter.filter_soort('Voorstel van wet', is_or=True)
        pd_filter.filter_soort('Voorstel van wet (initiatiefvoorstel)', is_or=True)
        pds = self.api.get_documenten(pd_filter)

        dossier_nrs = []
        pds_no_dossier_nr = []
        for pd in pds[:10]:
            print(pd.dossier_nummers)
            if pd.dossier_nummers:
                dossier_nrs += pd.dossier_nummers
            else:
                pds_no_dossier_nr.append(pd)
        for pd in pds_no_dossier_nr:
            print(pd.dossier_nummers)
            print(pd.onderwerp)

        dossier_nrs = sorted(set(dossier_nrs))
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
    #     zaken = self.api.get_zaken(zaak_filter)
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
    #         dossiers_for_zaak = self.api.get_dossiers(filter=dossier_filter)
    #         if dossiers_for_zaak:
    #             dossiers += dossiers_for_zaak
    #             print('Dossier found for zaak: ' + str(zaak_nr))
    #         else:
    #             print('WARNING: No dossier found for zaak: ' + str(zaak_nr))
    #     dossier_nummers = []
    #     for dossier in dossiers:
    #         print('\n=======')
    #         print(dossier.nummer)
    #         print(dossier.afgesloten)
    #         print(dossier.organisatie)
    #         print(dossier.titel)
    #         dossier_nummers.append(dossier.nummer)
    #         # dossier.print_json()
    #     dossier_nrs = sorted(set(dossier_nummers))
    #     print(dossier_nrs)
    #     print(len(dossier_nrs))
