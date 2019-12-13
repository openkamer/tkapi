from tkapi import Api
from tkapi.agendapunt import Agendapunt

from .core import TKApiTestCase


class TestAgendapunt(TKApiTestCase):

    def test_get_agendapunten(self):
        max_items = 10
        agendapunten = self.api.get_agendapunten(filter=None, max_items=max_items)
        self.assertEqual(len(agendapunten), max_items)
        for agendapunt in agendapunten:
            self.assertGreaterEqual(1, len(agendapunt.zaken))
            self.assertGreaterEqual(1, len(agendapunt.documenten))
            print(agendapunt.besluit)


class TestAgendapuntFilter(TKApiTestCase):

    def test_filter_agendapunten_with_activiteit(self):
        max_items = 5
        agendapunt_filter = Agendapunt.create_filter()
        agendapunt_filter.filter_has_activiteit()
        agendapunten = Api().get_agendapunten(max_items=max_items)
        for agendapunt in agendapunten:
            self.assertTrue(agendapunt.activiteit)
        self.assertEqual(len(agendapunten), max_items)
