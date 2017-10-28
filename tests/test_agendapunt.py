import datetime
import unittest

from tkapi import api
from tkapi.agendapunt import Agendapunt


class TestAgendapunt(unittest.TestCase):

    def test_get_agendapunten(self):
        agendapunten = api.get_agendapunten(filter=None, max_items=1000)
        for agendapunt in agendapunten:
            if agendapunt.parlementaire_documenten:
                agendapunt.print_json()
            # agendapunt.print_json()
            # for zaak in agendapunt.zaken:
            #     print(zaak)
            # for document in agendapunt.parlementaire_documenten:
            #     document.print_json()