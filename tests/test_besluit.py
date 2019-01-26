from tkapi.besluit import Besluit

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

    def test_kamerstukdossier_filter(self):
        n_items = 4
        vetnummer = 34822
        filter = Besluit.create_filter()
        filter.filter_kamerstukdossier(vetnummer=vetnummer)
        besluiten = self.api.get_besluiten(filter=filter, max_items=n_items)
        self.assertEqual(n_items, len(besluiten))
        for besluit in besluiten:
            self.assertEqual(vetnummer, besluit.zaak.dossier.vetnummer)

    def test_kamerstuk_filter(self):
        n_items = 5
        vetnummer = 33885
        volgnummer = 16
        filter = Besluit.create_filter()
        filter.filter_kamerstuk(vetnummer=vetnummer, ondernummer=volgnummer)
        besluiten = self.api.get_besluiten(filter=filter, max_items=n_items)
        self.assertEqual(1, len(besluiten))
        for besluit in besluiten:
            self.assertEqual(vetnummer, besluit.zaken[0].dossier.vetnummer)
