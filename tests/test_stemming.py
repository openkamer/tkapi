import datetime

from tkapi.stemming import Stemming
from tkapi.besluit import Besluit
from tkapi.zaak import Zaak
from tkapi.zaak import ZaakSoort

from tkapi.util import queries

from .core import TKApiTestCase


class TestStemming(TKApiTestCase):

    def test_get_stemmingen(self):
        stemmingen = self.api.get_stemmingen(filter=None, max_items=10)
        self.assertEqual(10, len(stemmingen))


class TestStemmingFilters(TKApiTestCase):

    def test_filter_moties(self):
        n_items = 10
        filter = Stemming.create_filter()
        filter.filter_moties()
        stemmingen = self.api.get_stemmingen(filter=filter, max_items=n_items)
        self.assertEqual(n_items, len(stemmingen))
        for stemming in stemmingen:
            self.assertEqual(ZaakSoort.MOTIE, stemming.besluit.zaken[0].soort)

    def test_filter_kamerstukdossier(self):
        dossier_nr = 33885
        zaak_filter = Zaak.create_filter()
        zaak_filter.filter_kamerstukdossier(nummer=dossier_nr)
        zaken = self.api.get_zaken(filter=zaak_filter)
        n_stemmingen = 0
        for zaak in zaken:
            print('=========================================')
            print('zaak', zaak.nummer, zaak.dossier.nummer, zaak.volgnummer)
            filter = Besluit.create_filter()
            filter.filter_zaak(zaak.nummer)
            besluiten = self.api.get_besluiten(filter=filter)
            for besluit in besluiten:
                n_stemmingen += len(besluit.stemmingen)
                print(len(besluit.stemmingen), besluit.soort, besluit.status, besluit.tekst)
                for stemming in besluit.stemmingen:
                    print('\t', stemming.soort, stemming.fractie_size)
        print('stemmingen', n_stemmingen)
        self.assertEqual(208, n_stemmingen)

    def test_filter_kamerstuk(self):
        dossier_nr = 33885
        volgnummer = 16
        stemmingen = queries.get_kamerstuk_stemmingen(nummer=dossier_nr, volgnummer=volgnummer)
        self.assertEqual(16, len(stemmingen))


class TestStemmingFractie(TKApiTestCase):

    # NOTE: this currently fails because stemming.fractie relations give empty fracties
    def test_get_stemmingen(self):
        stemmingen = queries.get_kamerstuk_stemmingen(nummer=33885, volgnummer=16)
        for stemming in stemmingen:
            print(stemming.fractie.naam)
            self.assertTrue(stemming.fractie.naam)
