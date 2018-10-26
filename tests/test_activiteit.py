import datetime

from tkapi.activiteit import Activiteit, ActiviteitSoort

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


class TestActiviteitFilters(TKApiTestCase):
    N_ITEMS = 15

    def test_kamerstuk_dossier_filter(self):
        filter = Activiteit.create_filter()
        filter.filter_kamerstukdossier(vetnummer=31239)
        activiteiten = self.api.get_activiteiten(filter=filter, max_items=self.N_ITEMS)
        print(len(activiteiten))
        self.assertEqual(self.N_ITEMS, len(activiteiten))
        ids = set()
        for activiteit in activiteiten:
            ids.add(activiteit.id)
            print(
                'Activiteit: {} ({} - {})'
                .format(activiteit.onderwerp, activiteit.begin, activiteit.einde)
            )
        self.assertEqual(len(activiteiten), len(ids))

    def test_kamerstuk_filter(self):
        filter = Activiteit.create_filter()
        filter.filter_kamerstuk(vetnummer=31239, ondernummer=16)
        activiteiten = self.api.get_activiteiten(filter=filter, max_items=self.N_ITEMS)
        print(len(activiteiten))
        self.assertEqual(self.N_ITEMS, len(activiteiten))
        ids = set()
        for activiteit in activiteiten:
            ids.add(activiteit.id)
            print(
                'Activiteit: {} ({} - {})'
                .format(activiteit.onderwerp, activiteit.begin, activiteit.einde)
            )
        self.assertEqual(len(activiteiten), len(ids))

    def test_soort_filter(self):
        soorten = [
            ActiviteitSoort.STEMMINGEN,
            ActiviteitSoort.VERGADERING,
            ActiviteitSoort.VRAGENUUR,
            ActiviteitSoort.PLENAIR_DEBAT,
            ActiviteitSoort.ALGEMEEN_OVERLEG,
            ActiviteitSoort.WETSVOORSTEL_INBRENG_VERSLAG,
            ActiviteitSoort.WETGEVINGSOVERLEG,
        ]
        for soort in soorten:
            filter = Activiteit.create_filter()
            filter.filter_soort(soort)
            activiteiten = self.api.get_activiteiten(filter=filter, max_items=self.N_ITEMS)
            print(len(activiteiten))
            ids = set()
            for activiteit in activiteiten:
                ids.add(activiteit.id)
                # print(
                #     'Activiteit: {} ({} - {})'
                #     .format(activiteit.soort, activiteit.begin, activiteit.einde)
                # )
            self.assertEqual(self.N_ITEMS, len(activiteiten))
            self.assertEqual(len(activiteiten), len(ids))
