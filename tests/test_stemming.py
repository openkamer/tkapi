import datetime

from tkapi.stemming import Stemming
from tkapi.dossier import Dossier
from tkapi.besluit import Besluit
from tkapi.document import Document
from tkapi.zaak import Zaak

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
            self.assertEqual('Motie', stemming.besluit.zaken[0].soort)

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

    # TODO BR: disabled because only 1 nested query allowed
    # def test_filter_kamerstuk(self):
    #     filter = Stemming.create_filter()
    #     filter.filter_kamerstuk(nummer=33885, volgnummer=16)
    #     stemmingen = self.api.get_stemmingen(filter=filter)
    #     self.assertEqual(16, len(stemmingen))
