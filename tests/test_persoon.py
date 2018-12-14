import datetime

from tkapi.persoon import Persoon
from tkapi.persoon import PersoonReis
from tkapi.persoon import PersoonOnderwijs
from tkapi.persoon import PersoonFunctie
from tkapi.persoon import PersoonLoopbaan
from tkapi.persoon import PersoonGeschenk
from tkapi.persoon import PersoonNevenfunctie

from .core import TKApiTestCase


class TestPersoon(TKApiTestCase):

    def test_get_personen(self):
        max_items = 66
        personen = self.api.get_personen(max_items=max_items)
        for persoon in personen:
            print('Roepnaam:', persoon.roepnaam)
            print('Volledige naam:', persoon.voornamen, persoon.achternaam)
            # persoon.print_json()
            # if persoon.fractie_lid is not None:
            #     persoon.fractie_lid.print_json()
            #     if persoon.fractie_lid.fractie is not None:
            #         persoon.fractie_lid.fractie.print_json()
        self.assertEqual(max_items, len(personen))

    def test_persoon_get_fracties(self):
        uid = '96a61016-76f0-4e73-80f0-0f554d919a93'
        persoon = self.api.get_item(Persoon, id=uid)
        fractieleden = persoon.fractieleden
        print(persoon.roepnaam, persoon.achternaam)
        print('fractieleden:', len(fractieleden))
        for lid in persoon.fractieleden:
            print(lid.fractie.naam)
        for fractie in persoon.fracties:
            print(fractie.naam)
        self.assertEqual(4, len(persoon.fracties))

    def test_get_functies(self):
        uid = '20415249-f14a-4375-b2c1-36608cbf0a76'
        persoon = self.api.get_item(Persoon, id=uid)
        functies = persoon.functies
        for functie in functies:
            print(functie.omschrijving)

    def test_get_reizen(self):
        uid = '355337af-a30f-48b8-882a-002ce35f9d07'  # Fred Teeven
        persoon = self.api.get_item(Persoon, id=uid)
        print(persoon)
        reizen = persoon.reizen
        self.assertEqual(5, len(reizen))
        self.assertEqual('Duitsland', reizen[0].bestemming)
        self.assertEqual('Ministerie van Defensie.', reizen[0].betaald_door)
        for reis in reizen:
            print(reis.bestemming)


class TestPersoonFilters(TKApiTestCase):

    def test_filter_achternaam(self):
        achternaam = 'Pechtold'
        filter = Persoon.create_filter()
        filter.filter_achternaam(achternaam)
        personen = self.api.get_personen(filter=filter)
        self.assertEqual(1, len(personen))
        persoon = personen[0]
        self.assertEqual(achternaam, persoon.achternaam)

    def test_filter_is_fractielid(self):
        n_items = 10
        filter = Persoon.create_filter()
        filter.filter_is_fractielid()
        personen = self.api.get_personen(filter=filter, max_items=n_items)
        self.assertEqual(n_items, len(personen))
        for persoon in personen:
            self.assertTrue(persoon.fractieleden)


class TestPersoonReis(TKApiTestCase):

    def test_get_reis(self):
        uid = '6ccc8b93-e86e-4e42-bb94-103eef850715'
        reis = self.api.get_item(PersoonReis, id=uid)
        self.assertEqual('Duitsland', reis.bestemming)
        self.assertEqual('Bijwonen oefening.', reis.doel)
        self.assertEqual('Ministerie van Defensie.', reis.betaald_door)
        self.assertGreater(reis.tot_en_met, reis.van)
        self.assertEqual('355337af-a30f-48b8-882a-002ce35f9d07', reis.persoon.id)

    def test_get_reizen(self):
        n_items = 20
        reizen = self.api.get_reizen(max_items=n_items)
        print('reizen:', len(reizen))
        self.assertEqual(n_items, len(reizen))
        for reis in reizen:
            print(reis.bestemming)
            print(reis.doel)
            print(reis.van, reis.tot_en_met)
            print(reis.betaald_door)
            self.assertIsNotNone(reis.bestemming)
            self.assertIsNotNone(reis.doel)
            self.assertIsNotNone(reis.van)
            self.assertIsNotNone(reis.tot_en_met)
            self.assertIsNotNone(reis.betaald_door)


class TestPersoonOnderwijs(TKApiTestCase):

    def test_get_onderwijs(self):
        uid = 'bb6e9fa6-f966-4ba2-9b48-4ce872d1128d'
        onderwijs = self.api.get_item(PersoonOnderwijs, id=uid)
        self.assertEqual('Master Public Management (MPM)', onderwijs.opleiding_nl)
        self.assertEqual('Master\'s degree in Public Management (MPM), University of Twente 1999-2001', onderwijs.opleiding_en)
        self.assertEqual('Universiteit Twente', onderwijs.instelling)
        self.assertEqual('', onderwijs.plaats)
        self.assertGreater(onderwijs.tot_en_met, onderwijs.van)
        self.assertEqual('355337af-a30f-48b8-882a-002ce35f9d07', onderwijs.persoon.id)


class TestPersoonFunctie(TKApiTestCase):

    def test_get_functie(self):
        uid = '310a2b85-6b99-4633-aa73-9a978cdeb3a8'
        functie = self.api.get_item(PersoonFunctie, id=uid)
        self.assertEqual('Oud Kamerlid', functie.omschrijving)
        self.assertEqual('355337af-a30f-48b8-882a-002ce35f9d07', functie.persoon.id)


class TestPersoonLoopbaan(TKApiTestCase):

    def test_get_loopbaan(self):
        uid = 'aa767276-e588-42b0-9f38-097a635081d0'
        loopbaan = self.api.get_item(PersoonLoopbaan, id=uid)
        self.assertEqual('Teamleider', loopbaan.functie)
        self.assertEqual('FIOD', loopbaan.werkgever)
        self.assertEqual('', loopbaan.omschrijving)
        self.assertEqual('Team leader, FIOD, Haarlem 1990-1993', loopbaan.omschrijving_en)
        self.assertEqual('Haarlem', loopbaan.plaats)
        self.assertGreater(loopbaan.tot_en_met, loopbaan.van)
        self.assertEqual('355337af-a30f-48b8-882a-002ce35f9d07', loopbaan.persoon.id)


class TestPersoonGeschenk(TKApiTestCase):

    def test_get_geschenk(self):
        uid = '1650fba4-5979-44d3-a591-0ff90c0736c4'
        geschenk = self.api.get_item(PersoonGeschenk, id=uid)
        self.assertEqual('Ontvangen van de Irakese ambassade een doros je wijn ter waarde van ongeveer €60,--.', geschenk.omschrijving)
        self.assertEqual(2009, geschenk.datum.year)
        self.assertEqual('355337af-a30f-48b8-882a-002ce35f9d07', geschenk.persoon.id)


class TestPersoonNevenfunctie(TKApiTestCase):

    def test_get_nevenfunctie(self):
        uid = '9ef1fb14-395c-44da-b378-089f7c1b5a1f'
        nevenfunctie = self.api.get_item(PersoonNevenfunctie, id=uid)
        self.assertEqual('Deelname in de Raad van advies van het Comité ter vervolging van oorlogsmisdadigers', nevenfunctie.omschrijving)
        self.assertEqual(None, nevenfunctie.van)
        self.assertEqual(None, nevenfunctie.tot_en_met)
        print(nevenfunctie.is_actief)
        self.assertEqual(False, nevenfunctie.is_actief)
        self.assertEqual('Onbezoldigd', nevenfunctie.soort)
        self.assertEqual('', nevenfunctie.toelichting)
        self.assertEqual('355337af-a30f-48b8-882a-002ce35f9d07', nevenfunctie.persoon.id)
