import datetime

from .core import TKApiTestCase


class TestActiviteit(TKApiTestCase):
    start_datetime = datetime.datetime(year=2017, month=1, day=1)
    end_datetime = datetime.datetime(year=2017, month=2, day=1)

    def test_get_activiteiten(self):
        activiteiten = self.api.get_activiteiten(filter=None, max_items=50)
        soorten = set()
        for activiteit in activiteiten:
            # activiteit.print_json()
            soorten.add(activiteit.soort)
        print('### Soorten Activiteiten ###')
        for soort in soorten:
            print(soort)
        self.assertGreater(len(soorten), 18)

    def test_activiteit_voortouwcommissies(self):
        activiteiten = self.api.get_activiteiten(filter=None, max_items=10)
        for activiteit in activiteiten:
            for vtcommissie in activiteit.voortouwcommissies:
                print('### ', vtcommissie.url, ' ###')
                # vtcommissie.print_json()

    def test_activiteit_documenten(self):
        activiteiten = self.api.get_activiteiten(filter=None, max_items=10)
        self.assertEqual(10, len(activiteiten))
        for activiteit in activiteiten:
            for pd in activiteit.parlementaire_documenten:
                if pd.kamerstuk:
                    print('dossier vetnummer:', pd.kamerstuk.dossier.vetnummer)
