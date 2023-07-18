import datetime

from tkapi.activiteit import Activiteit
from tkapi.activiteit import ActiviteitActor
from tkapi.activiteit import ActiviteitSoort
from tkapi.activiteit import ActiviteitRelatieSoort
from tkapi.activiteit import ActiviteitStatus
from tkapi.activiteit import Reservering
from tkapi.activiteit import Zaal
from tkapi.filter import PropertyFilter
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
                print('### ', vtcommissie.type, ' ###')
                # vtcommissie.print_json()

    def test_activiteit_documenten(self):
        activiteiten = self.api.get_activiteiten(filter=None, max_items=10)
        self.assertEqual(10, len(activiteiten))
        for activiteit in activiteiten:
            for pd in activiteit.documenten:
                for dossier in pd.dossiers:
                    print('dossier nummer:', dossier.nummer)

    def test_activiteit_status(self):
        activiteiten = self.api.get_activiteiten(filter=None, max_items=10)
        self.assertEqual(10, len(activiteiten))
        for activiteit in activiteiten:
            self.assertIn(activiteit.status, ActiviteitStatus)


class TestActiviteitFilters(TKApiTestCase):
    N_ITEMS = 15

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
            ActiviteitSoort.PLENAIR_DEBAT_WETGEVING,
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
            # No results available at the moment for the soorten below (or enum is wrong?)
            ingore_soorten = [
                ActiviteitSoort.HOORZITTING, ActiviteitSoort.MEDEDELINGEN, ActiviteitSoort.OPENING, ActiviteitSoort.OVERIG,
                ActiviteitSoort.RONDETAFELGESPREK, ActiviteitSoort.SLUITING, ActiviteitSoort.HOORZITTING_RONDETAFELGESPREK,
                ActiviteitSoort.INTERPELLATIEDEBAT, ActiviteitSoort.PLENAIR_DEBAT
            ]
            if soort in ingore_soorten:
                continue
            self.assertEqual(max_items, len(activiteiten))
            self.assertEqual(soort, activiteiten[0].soort)


class TestReservering(TKApiTestCase):

    def test_get_item(self):
        res = self.api.get_items(Reservering, max_items=1)
        self.assertEqual(1, len(res))
        res = res[0]
        self.assertIsNotNone(res.activiteit)
        self.assertEqual(res.activiteit_nummer, res.activiteit.nummer)
        print(res.status_code, res.status_naam, res.activiteit.id, res.activiteit_nummer)


class TestZaal(TKApiTestCase):

    def test_get_item(self):
        zalen = self.api.get_items(Zaal, max_items=1)
        self.assertEqual(1, len(zalen))
        zaal = zalen[0]
        self.assertTrue(zaal.naam)


class TestActiviteitActor(TKApiTestCase):

    def test_get_item(self):
        actors = self.api.get_items(ActiviteitActor, max_items=1)
        self.assertEqual(1, len(actors))
        actor = actors[0]
        self.assertIsNotNone(actor.volgorde)
        self.assertIn(actor.relatie, ActiviteitRelatieSoort)
        print(actor.activiteit.id, actor.persoon, actor.fractie, actor.commissie, actor.fractie_naam, actor.naam, actor.spreektijd)


class TestActiviteitActorRelatieSoort(TKApiTestCase):

    def test_activiteit_actor_relatie_soort_enum(self):
        max_items = 1
        for soort in ActiviteitRelatieSoort:
            filter = PropertyFilter()
            filter.filter_property(property_name='relatie', value=soort, is_or=False)
            actors = self.api.get_items(ActiviteitActor, filter=filter, max_items=max_items)
            self.assertEqual(max_items, len(actors))
            self.assertEqual(soort, actors[0].relatie)

    def test_get_items(self):
        actors = self.api.get_items(ActiviteitActor, max_items=500)
        for actor in actors:
            self.assertIn(actor.relatie, ActiviteitRelatieSoort)

