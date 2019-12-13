from tkapi.besluit import Besluit

from tkapi.util import queries

from .core import TKApiTestCase


class TestBesluit(TKApiTestCase):

    def test_get_besluiten(self):
        n_items = 5
        besluit_filter = Besluit.create_filter()
        besluit_filter.filter_non_empty_zaak()
        besluiten = self.api.get_besluiten(filter=besluit_filter, max_items=n_items)
        for besluit in besluiten:
            self.assertEqual(1, len(besluit.zaken))
            self.assertIsNotNone(besluit.agendapunt.activiteit)
        self.assertEqual(n_items, len(besluiten))


class TestBesluitFilters(TKApiTestCase):

    def test_kamerstukdossier_filter_34822(self):
        nummer = 34822
        expected_besluiten = 13
        expected_with_stemmen = 1
        self.check_dossier_besluiten(nummer, expected_besluiten, expected_with_stemmen)

    def test_kamerstukdossier_filter_34819(self):
        nummer = 34819
        expected_besluiten = 36
        expected_with_stemmen = 7
        self.check_dossier_besluiten(nummer, expected_besluiten, expected_with_stemmen)

    def test_kamerstukdossier_filter_34792(self):
        nummer = 34792
        expected_besluiten = 14
        expected_with_stemmen = 6
        self.check_dossier_besluiten(nummer, expected_besluiten, expected_with_stemmen)

    def test_kamerstuk_filter_33885(self):
        nummer = 33885
        volgnummer = 16
        besluiten = queries.get_kamerstuk_besluiten(nummer=nummer, volgnummer=volgnummer)
        self.assertEqual(1, len(besluiten))
        for besluit in besluiten:
            self.assertEqual(nummer, besluit.zaken[0].dossier.nummer)

    def test_kamerstuk_filter_35300(self):
        nummer = 35300
        toevoeging = 'VIII'
        volgnummer = 78
        besluiten = queries.get_kamerstuk_besluiten(nummer=nummer, toevoeging=toevoeging, volgnummer=volgnummer)
        self.assertEqual(2, len(besluiten))
        for besluit in besluiten:
            for stemming in besluit.stemmingen:
                print(stemming['Verwijderd'])

    def check_dossier_besluiten(self, nummer, expected_besluiten, expected_with_stemmen):
        besluiten = queries.get_dossier_besluiten(nummer=nummer)
        besluiten_with_stemmen = queries.get_dossier_besluiten_with_stemmingen(nummer=nummer)
        self.assertEqual(expected_besluiten, len(besluiten))
        self.assertEqual(expected_with_stemmen, len(besluiten_with_stemmen))
        # for besluit in besluiten:
        #     print(besluit.status, besluit.soort, len(besluit.stemmingen))
        #     self.assertEqual(nummer, besluit.zaak.dossier.nummer)
        for besluit in besluiten_with_stemmen:
            print(besluit.status, besluit.soort, len(besluit.stemmingen))
            self.assertEqual(nummer, besluit.zaak.dossier.nummer)
