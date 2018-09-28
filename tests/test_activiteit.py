import datetime
import unittest

from tkapi import api


class TestActiviteit(unittest.TestCase):
    start_datetime = datetime.datetime(year=2017, month=1, day=1)
    end_datetime = datetime.datetime(year=2017, month=2, day=1)

    def test_get_activiteiten(self):
        activiteiten = api.get_activiteiten(filter=None, max_items=50)
        soorten = set()
        for activiteit in activiteiten:
            activiteit.print_json()
            soorten.add(activiteit.soort)
        print('### Soorten Activiteiten ###')
        for soort in soorten:
            print(soort)
        self.assertGreater(len(soorten), 18)

    def test_activiteit_voortouwcommissies(self):
        activiteiten = api.get_activiteiten(filter=None, max_items=10)
        for activiteit in activiteiten:
            for vtcommissie in activiteit.voortouwcommissies:
                print('### ', vtcommissie.url, ' ###')
                vtcommissie.print_json()

    def test_activiteit_documenten(self):
        activiteiten = api.get_activiteiten(filter=None, max_items=10)
        self.assertEqual(10, len(activiteiten))
        for activiteit in activiteiten:
            for pd in activiteit.parlementaire_documenten:
                for kamerstuk in pd.kamerstukken:
                    print('dossier vetnummer:', kamerstuk.dossier.vetnummer)
