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
        activiteiten_expected = 18
        activiteiten = queries.get_dossier_activiteiten(dosser_nr)
        print('activiteiten found:', len(activiteiten))
        self.assertEqual(activiteiten_expected, len(activiteiten))

    def test_dossier_filter_2(self):
        dosser_nr = 34986
        activiteiten_expected = 17
        activiteiten = queries.get_dossier_activiteiten(dosser_nr, include_agendapunten=True)
        print('activiteiten found:', len(activiteiten))
        self.assertEqual(activiteiten_expected, len(activiteiten))

    def test_kamerstuk_filter(self):
        dossier_nr = 34986
        volgnummer = 9
        activiteiten_expected = 11
        activiteiten = queries.get_kamerstuk_activiteiten(nummer=dossier_nr, volgnummer=volgnummer, include_agendapunten=True)
        self.assertGreaterEqual(len(activiteiten), activiteiten_expected)

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
            self.assertEqual(self.N_ITEMS, len(activiteiten))
            self.assertEqual(len(activiteiten), len(ids))

    def test_activiteit_soort_enum(self):
        max_items = 1
        for soort in ActiviteitSoort:
            filter = Activiteit.create_filter()
            filter.filter_soort(soort)
            activiteiten = self.api.get_activiteiten(filter=filter, max_items=max_items)
            if not activiteiten:
                print('No activiteit found for soort enum: {}'.format(soort))
            ignor_soorten = [
                ActiviteitSoort.HOORZITTING, ActiviteitSoort.MEDEDELINGEN, ActiviteitSoort.OPENING, ActiviteitSoort.OVERIG,
                ActiviteitSoort.RONDETAFELGESPREK, ActiviteitSoort.SLUITING
            ]
            if soort in ignor_soorten:
                # No results available at the moment (or enum is wrong?)
                continue
            self.assertEqual(max_items, len(activiteiten))
            self.assertEqual(soort, activiteiten[0].soort)
