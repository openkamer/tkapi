import datetime

from orderedset import OrderedSet

from tkapi.zaak import Zaak, ZaakSoort
from tkapi.dossier import Dossier, DossierWetsvoorstel
from tkapi.document import Document

from .core import TKApiTestCase


class TestDossier(TKApiTestCase):

    def test_get_dossiers(self):
        dossiers = self.api.get_dossiers(filter=None, max_items=10)
        self.assertEqual(10, len(dossiers))

    def test_get_dossier_by_vetnummer(self):
        vetnummer = 34435
        filter = Dossier.create_filter()
        filter.filter_vetnummer(vetnummer)
        dossiers = self.api.get_dossiers(filter=filter)
        self.assertEqual(len(dossiers), 1)
        dossiers[0].print_json()

    def test_dossier_filter(self):
        self.check_dossier_filter('2016Z16486', 34537)
        self.check_dossier_filter('2016Z24906', 34640)

    def check_dossier_filter(self, zaak_nr, expected_dossier_vetnummer):
        dossier_filter = Dossier.create_filter()
        dossier_filter.filter_zaak(zaak_nr)
        dossiers = self.api.get_dossiers(filter=dossier_filter)
        # for dossier in dossiers:
        #     dossier.print_json()
        self.assertEqual(len(dossiers), 1)
        # print(dossiers[0].vetnummer)
        self.assertEqual(dossiers[0].vetnummer, expected_dossier_vetnummer)


class TestDossierKamerstukken(TKApiTestCase):

    def test_dossier_kamerstukken(self):
        # vetnummer = 34693
        # vetnummer = 34374
        # vetnummer = 34051
        # vetnummer = 22139
        vetnummer = 34723
        dossier_filter = Dossier.create_filter()
        dossier_filter.filter_vetnummer(vetnummer)
        dossiers = self.api.get_dossiers(filter=dossier_filter)
        self.assertEqual(len(dossiers), 1)
        dossier = dossiers[0]
        kamerstukken = dossier.kamerstukken
        for kamerstuk in kamerstukken:
            print('\n============')
            # kamerstuk.print_json()
            print(kamerstuk.ondernummer)
            document = kamerstuk.document
            # document.print_json()
            print(document.soort)
            print(document.titel)
            for agendapunt in document.agendapunten:
                self.assertTrue(agendapunt.id)
                # agendapunt.print_json()
            for zaak in document.zaken:
                if not zaak.afgedaan:
                    print('NIET GESLOTEN')
                for besluit in zaak.besluiten:
                    for stemming in besluit.stemmingen:
                        self.assertTrue(stemming.id)
                        # stemming.print_json()


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
            print('dossier.vetnummer: ', str(dossier.vetnummer))
            for pd in dossier.parlementaire_documenten:
                for zaak in pd.zaken:
                    dossier_zaak_nummers.add(zaak.nummer)
        print('dossier_zaak_nummers', dossier_zaak_nummers)
        for zaak in zaken:
            if zaak.nummer not in dossier_zaak_nummers:
                print(zaak.nummer)
                zaak.print_json()
            # self.assertTrue(zaak_nr in dossier_zaak_nummers)
        # print(zaken)


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

    def test_filter_kamerstuk(self):
        filter = Dossier.create_filter()
        filter.filter_kamerstuk(vetnummer=33885, ondernummer=16)
        dossiers = self.api.get_dossiers(filter=filter)
        for dossier in dossiers:
            print(dossier.vetnummer, len(dossier.kamerstukken))


class TestWetsvoorstelDossier(TKApiTestCase):

    def test_get_wetsvoorstellen_dossiers(self):
        max_items = 200
        wetsvoorstellen = self.api.get_items(DossierWetsvoorstel, max_items=max_items)
        self.assertEqual(max_items, len(wetsvoorstellen))

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
            print(pd.dossier_vetnummer)
            if pd.dossier_vetnummer:
                dossier_nrs.append(pd.dossier_vetnummer)
            else:
                pds_no_dossier_nr.append(pd)
        for pd in pds_no_dossier_nr:
            print(pd.nummer)
            print(pd.onderwerp)

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
