from tkapi.util import queries

from .core import TKApiTestCase


class TestUtilQueries(TKApiTestCase):

    def test_get_dossier_besluiten_with_stemmingen(self):
        nummer = 33885
        besluiten = queries.get_dossier_besluiten_with_stemmingen(nummer=nummer)
        self.assertEqual(13, len(besluiten))
        for besluit in besluiten:
            self.assertGreaterEqual(len(besluit.stemmingen), 1)

    def test_get_dossier_besluiten(self):
        nummer = 33885
        besluiten = queries.get_dossier_besluiten(nummer=nummer)
        self.assertEqual(49, len(besluiten))
        for besluit in besluiten[:5]:
            if not besluit.stemmingen:
                continue
            stemmingen = queries.do_load_stemmingen(stemmingen=besluit.stemmingen)
            for stemming in stemmingen:
                print('\t', stemming.fractie.naam, stemming.fractie_size, stemming.soort, besluit.soort)

    def test_get_kamerstuk_besluiten(self):
        nummer = 33885
        volgnummer = 16
        besluiten = queries.get_kamerstuk_besluiten(nummer=nummer, volgnummer=volgnummer)
        self.assertEqual(1, len(besluiten))
        for besluit in besluiten:
            print(besluit.tekst, besluit.soort, besluit.stemming_soort, besluit.opmerking, len(besluit.stemmingen))

    def test_get_kamerstuk_zaken(self):
        nummer = 33885
        volgnummer = 16
        zaken = queries.get_kamerstuk_zaken(nummer, volgnummer)
        print(len(zaken))

    def test_get_kamerleden_active(self):
        persons = queries.get_kamerleden_active()
        self.assertGreaterEqual(len(persons), 148)  # some seats may be open for a while

    def test_fractie_leden_actief(self):
        leden = queries.get_fractieleden_actief()
        self.assertGreaterEqual(len(leden), 100)
        for lid in leden:
            print(lid.persoon, lid.fractie)
