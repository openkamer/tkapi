import datetime

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
