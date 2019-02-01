import datetime

from tkapi.activiteit import Activiteit, ActiviteitSoort
from tkapi.util import queries

from .core import TKApiTestCase


class TestActiviteit(TKApiTestCase):
    start_datetime = datetime.datetime(year=2017, month=1, day=1)
    end_datetime = datetime.datetime(year=2017, month=2, day=1)

    def test_get_activiteiten(self):
        activiteiten = self.api.get_activiteiten(filter=None, max_items=500)
        soorten = set()
        for activiteit in activiteiten:
            # activiteit.print_json()
            soorten.add(activiteit.soort)
        print('### Soorten Activiteiten ###')
        for soort in soorten:
            print(soort)
        self.assertGreater(len(soorten), 5)

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
            for pd in activiteit.documenten:
                for dossier in pd.dossiers:
                    print('dossier nummer:', dossier.nummer)


class TestActiviteitFilters(TKApiTestCase):
    N_ITEMS = 15

    def test_dossier_filter(self):
        dosser_nr = 31239
        activiteiten_expected = 8
        activiteiten = queries.get_dossier_activiteiten(dosser_nr)
        print('activiteiten found:', len(activiteiten))
        for activiteit in activiteiten:
            print('Activiteit: {} ({} - {})' .format(activiteit.onderwerp, activiteit.begin, activiteit.einde))
        self.assertEqual(activiteiten_expected, len(activiteiten))

    # TODO BR: should return results
    def test_dossier_filter_2(self):
        dosser_nr = 34986
        activiteiten_expected = 8
        activiteiten = queries.get_dossier_activiteiten(dosser_nr)
        print('activiteiten found:', len(activiteiten))
        for activiteit in activiteiten:
            print('Activiteit: {} ({} - {})' .format(activiteit.onderwerp, activiteit.begin, activiteit.einde))
        self.assertEqual(activiteiten_expected, len(activiteiten))

    # TODO BR: should return results
    def test_kamerstuk_filter(self):
        dossier_nr = 34986
        volgnummer = 16
        activiteiten = queries.get_dossier_activiteiten(nummer=dossier_nr)
        print(len(activiteiten))
        for activiteit in activiteiten:
            for zaak in activiteit.zaken:
                print(zaak.volgnummer)
        activiteiten = queries.get_kamerstuk_activiteiten(nummer=dossier_nr, volgnummer=volgnummer)
        print(len(activiteiten))
        self.assertGreater(len(activiteiten), 0)
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
