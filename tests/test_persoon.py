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

    def get_fred_teeven(self):
        filter = Persoon.create_filter()
        filter.filter_achternaam('Teeven')
        return self.api.get_personen(filter=filter)[0]

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
        persoon = self.get_fred_teeven()
        fractieleden = persoon.fractieleden
        print(persoon.roepnaam, persoon.achternaam)
        print('fractieleden:', len(fractieleden))
        for lid in persoon.fractieleden:
            print(lid.fractie.naam)
        for fractie in persoon.fracties:
            print(fractie.naam)
        self.assertEqual(4, len(persoon.fracties))

    def test_get_functies(self):
        persoon = self.get_fred_teeven()
        functies = persoon.functies
        for functie in functies:
            print(functie.omschrijving)

    # TODO BR: enable if available in v2 (OData v4)
    # def test_get_reizen(self):
    #     persoon = self.get_fred_teeven()
    #     print(persoon)
    #     reizen = persoon.reizen
    #     self.assertEqual(5, len(reizen))
    #     self.assertEqual('Duitsland', reizen[0].bestemming)
    #     self.assertEqual('Ministerie van Defensie.', reizen[0].betaald_door)
    #     for reis in reizen:
    #         print(reis.bestemming)


class TestPersoonFilters(TKApiTestCase):

    def test_filter_achternaam(self):
        achternaam = 'Pechtold'
        filter = Persoon.create_filter()
        filter.filter_achternaam(achternaam)
        personen = self.api.get_personen(filter=filter)
        self.assertEqual(1, len(personen))
        persoon = personen[0]
        self.assertEqual(achternaam, persoon.achternaam)

    def test_filter_is_fractiezetel(self):
        n_items = 10
        filter = Persoon.create_filter()
        filter.filter_is_fractiezetel()
        personen = self.api.get_personen(filter=filter, max_items=n_items)
        self.assertEqual(n_items, len(personen))
        for persoon in personen:
            self.assertTrue(persoon.fractieleden)


class TestPersoonReis(TKApiTestCase):

    def test_get_reis(self):
        uid = '78cda327-8ab0-4cce-96ed-4de669356fc6'
        reis = self.api.get_item(PersoonReis, id=uid)
        self.assertEqual('Katowice, Polen', reis.bestemming)
        self.assertEqual('Werkbezoek aan de 24ste Klimaatconferentie met de vaste commissie voor Economische Zaken en Klimaat', reis.doel)
        self.assertEqual('Tweede Kamer der Staten-Generaal', reis.betaald_door)
        self.assertGreater(reis.tot_en_met, reis.van)
        self.assertEqual('046383b9-4c9e-4037-ad9f-ad8925cf75c4', reis.persoon.id)

    def test_get_reizen(self):
        n_items = 20
        reizen = self.api.get_reizen(max_items=n_items)
        print('reizen:', len(reizen))
        self.assertEqual(n_items, len(reizen))
        for reis in reizen:
            print(reis.id)
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

    def test_get_first(self):
        onderwijs = self.api.get_items(PersoonOnderwijs, max_items=1)[0]
        self.assertTrue(onderwijs.opleiding_nl)
        self.assertTrue(onderwijs.instelling)
        self.assertGreaterEqual(onderwijs.tot_en_met, onderwijs.van)
        self.assertTrue(onderwijs.persoon.id)


# TODO BR: enable if available in v2 (OData v4) or remove
# class TestPersoonFunctie(TKApiTestCase):
#
#     def test_get_functie(self):
#         functie = self.api.get_items(PersoonFunctie, max_items=1)[0]
#         self.assertTrue(functie.omschrijving)
#         self.assertTrue(functie.persoon.id)


class TestPersoonLoopbaan(TKApiTestCase):

    def test_get_loopbaan(self):
        loopbaan = self.api.get_items(PersoonLoopbaan, max_items=1)[0]
        self.assertTrue(loopbaan.functie)
        # self.assertTrue(loopbaan.werkgever)
        # self.assertTrue(loopbaan.omschrijving)
        # self.assertTrue(loopbaan.omschrijving_en)
        self.assertTrue(loopbaan.plaats)
        print(loopbaan.van, loopbaan.tot_en_met, loopbaan.werkgever, loopbaan.omschrijving)
        # self.assertGreater(loopbaan.tot_en_met, loopbaan.van)
        self.assertTrue(loopbaan.persoon.id)


# class TestPersoonGeschenk(TKApiTestCase):
#
#     def test_get_geschenk(self):
#         uid = '1650fba4-5979-44d3-a591-0ff90c0736c4'
#         geschenk = self.api.get_item(PersoonGeschenk, id=uid)
#         self.assertEqual('Ontvangen van de Irakese ambassade een doros je wijn ter waarde van ongeveer €60,--.', geschenk.omschrijving)
#         self.assertEqual(2009, geschenk.datum.year)
#         self.assertEqual('355337af-a30f-48b8-882a-002ce35f9d07', geschenk.persoon.id)
#
#
# class TestPersoonNevenfunctie(TKApiTestCase):
#
#     def test_get_nevenfunctie(self):
#         uid = '9ef1fb14-395c-44da-b378-089f7c1b5a1f'
#         nevenfunctie = self.api.get_item(PersoonNevenfunctie, id=uid)
#         self.assertEqual('Deelname in de Raad van advies van het Comité ter vervolging van oorlogsmisdadigers', nevenfunctie.omschrijving)
#         self.assertEqual(None, nevenfunctie.van)
#         self.assertEqual(None, nevenfunctie.tot_en_met)
#         print(nevenfunctie.is_actief)
#         self.assertEqual(False, nevenfunctie.is_actief)
#         self.assertEqual('Onbezoldigd', nevenfunctie.soort)
#         self.assertEqual('', nevenfunctie.toelichting)
#         self.assertEqual('355337af-a30f-48b8-882a-002ce35f9d07', nevenfunctie.persoon.id)
