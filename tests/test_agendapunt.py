from tkapi import Api
from tkapi.agendapunt import Agendapunt

from .core import TKApiTestCase


class TestAgendapunt(TKApiTestCase):

    def test_get_agendapunten(self):
        max_items = 10
        agendapunten = self.api.get_agendapunten(filter=None, max_items=max_items)
        self.assertEqual(len(agendapunten), max_items)
        # for agendapunt in agendapunten:
            # if agendapunt.documenten:
            #     agendapunt.print_json()
            # agendapunt.print_json()
            # for zaak in agendapunt.zaken:
            #     print(zaak)
            # for document in agendapunt.documenten:
            #     document.print_json()


class TestAgendapuntFilter(TKApiTestCase):

    def test_filter_agendapunten_with_activiteit(self):
        max_items = 5
        agendapunt_filter = Agendapunt.create_filter()
        agendapunt_filter.filter_has_activiteit()
        agendapunten = Api().get_agendapunten(max_items=max_items)
        for agendapunt in agendapunten:
            self.assertTrue(agendapunt.activiteit)
        self.assertEqual(len(agendapunten), max_items)
