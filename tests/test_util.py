from tkapi.util import queries

from .core import TKApiTestCase


class TestUtilQueries(TKApiTestCase):

    def test_get_dossier_activiteiten(self):
        nummer = 31239
        activiteiten_expected = 24
        activiteiten = queries.get_dossier_activiteiten(nummer)
        self.assertGreaterEqual(activiteiten_expected, len(activiteiten))

    def test_get_dossier_activiteiten_inc_agenda(self):
        dosser_nr = 34986
        activiteiten_expected = 18
        activiteiten = queries.get_dossier_activiteiten(dosser_nr, include_agendapunten=True)
        self.assertEqual(activiteiten_expected, len(activiteiten))

    def test_get_dossier_activiteiten_toevoeging(self):
        nummer = 33000
        toevoeging = 'XV'
        activiteiten_expected = 1
        activiteiten = queries.get_dossier_activiteiten(nummer, toevoeging=toevoeging)
        self.assertEqual(activiteiten_expected, len(activiteiten))

    def test_get_dossier_besluiten_with_stemmingen(self):
        nummer = 33885
        besluiten = queries.get_dossier_besluiten_with_stemmingen(nummer=nummer)
        self.assertEqual(13, len(besluiten))
        for besluit in besluiten:
            self.assertGreaterEqual(len(besluit.stemmingen), 1)

    def test_get_dossier_besluiten_with_stemmingen_toevoeging(self):
        nummer = 33000
        toevoeging = 'XV'
        besluiten = queries.get_dossier_besluiten_with_stemmingen(nummer=nummer, toevoeging=toevoeging)
        self.assertEqual(43, len(besluiten))
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

    def test_get_dossier_besluiten_toevoeging(self):
        nummer = 33000
        toevoeging = 'XV'
        besluiten = queries.get_dossier_besluiten(nummer=nummer, toevoeging=toevoeging)
        self.assertEqual(238, len(besluiten))

    def test_get_kamerstuk_besluiten(self):
        nummer = 33885
        volgnummer = 16
        besluiten = queries.get_kamerstuk_besluiten(nummer=nummer, volgnummer=volgnummer)
        self.assertEqual(1, len(besluiten))
        for besluit in besluiten:
            print(besluit.tekst, besluit.soort, besluit.stemming_soort, besluit.opmerking, len(besluit.stemmingen))

    def test_get_kamerstuk_besluiten_toevoeging(self):
        nummer = 33000
        volgnummer = 10
        toevoeging = 'XV'
        besluiten = queries.get_kamerstuk_besluiten(nummer=nummer, volgnummer=volgnummer)
        self.assertEqual(52, len(besluiten))
        besluiten = queries.get_kamerstuk_besluiten(nummer=nummer, volgnummer=volgnummer, toevoeging=toevoeging)
        self.assertEqual(2, len(besluiten))

    def test_get_kamerstuk_zaken(self):
        nummer = 33885
        volgnummer = '16'
        zaken = queries.get_kamerstuk_zaken(nummer, volgnummer)
        self.assertEqual(1, len(zaken))
        zaak = zaken[0]
        self.assertEqual(nummer, zaak.dossier.nummer)
        self.assertEqual(volgnummer, zaak.volgnummer)

    def test_get_kamerstuk_begroting_zaken(self):
        nummer = 33000
        toevoeging = 'XV'
        volgnummer = 10
        zaken = queries.get_kamerstuk_zaken(nummer, volgnummer)
        self.assertEqual(16, len(zaken))
        zaken = queries.get_kamerstuk_zaken(nummer, volgnummer, toevoeging)
        self.assertEqual(1, len(zaken))

    def test_get_kamerleden_active(self):
        persons = queries.get_kamerleden_active()
        self.assertGreaterEqual(len(persons), 148)  # some seats may be open for a while

    def test_fractie_leden_actief(self):
        leden = queries.get_fractieleden_actief()
        self.assertGreaterEqual(len(leden), 100)
        for lid in leden:
            print(lid.persoon, lid.fractie)

    def test_get_dossier_zaken(self):
        nummer = 33885
        zaken = queries.get_dossier_zaken(nummer)
        self.assertEqual(27, len(zaken))

    def test_get_dossier_zaken_toevoeging(self):
        nummer = 33000
        toevoeging = 'XV'
        zaken = queries.get_dossier_zaken(nummer, toevoeging)
        self.assertEqual(76, len(zaken))

    def test_filter_dossier(self):
        nummer = 31239
        expected = 262
        documenten = queries.get_dossier_documenten(nummer)
        self.assertGreaterEqual(len(documenten), expected)

    def test_filter_dossier_toevoeging(self):
        nummer = 33000
        toevoeging = 'XV'
        documenten = queries.get_dossier_documenten(nummer)
        self.assertEqual(1704, len(documenten))
        documenten = queries.get_dossier_documenten(nummer, toevoeging=toevoeging)
        self.assertEqual(79, len(documenten))

    def test_filter_dossier_with_activiteit(self):
        nummer = 31239
        expected = 10
        documenten = queries.get_dossier_documenten_with_activiteit(nummer)
        self.assertGreaterEqual(len(documenten), expected)

    def test_filter_dossier_with_activiteit_toevoeging(self):
        nummer = 35300
        toevoeging = 'XVI'
        documenten = queries.get_dossier_documenten_with_activiteit(nummer)
        self.assertEqual(34, len(documenten))
        documenten = queries.get_dossier_documenten_with_activiteit(nummer, toevoeging=toevoeging)
        self.assertEqual(2, len(documenten))
