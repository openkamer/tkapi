import unittest
from orderedset import OrderedSet

from tkapi import api
from tkapi.commissie import Commissie
from tkapi.commissie import CommissieFilter
from tkapi.info import get_commissie_namen
from tkapi.info import get_commissie_soorten


class TestCommissie(unittest.TestCase):

    def test_get_commissies(self):
        max_items = None
        commissies = api.get_commissies(max_items=max_items)
        for commissie in commissies:
            print('===========')
            # commissie.print_json()
            print(commissie)
            print(commissie.soort)
            for lid in commissie.leden:
                if lid.persoon:
                    print('\t' + str(lid))

    def test_soort_filter(self):
        soort = 'Algemeen'
        com_filter = CommissieFilter()
        com_filter.filter_soort(soort)
        commissies_algemeen = api.get_commissies(com_filter)
        self.assertTrue(len(commissies_algemeen) > 4)
        for commissie in commissies_algemeen:
            self.assertEqual(commissie.soort, soort)

    def test_naam_filter(self):
        naam = 'Vaste commissie voor Binnenlandse Zaken'
        com_filter = CommissieFilter()
        com_filter.filter_naam(naam)
        commissies_algemeen = api.get_commissies(com_filter)
        commissies_algemeen[0].print_json()
        self.assertTrue(len(commissies_algemeen), 1)
        for commissie in commissies_algemeen:
            self.assertEqual(commissie.naam, naam)


class TestCommissieInfo(unittest.TestCase):

    def test_commissie_namen(self):
        namen = get_commissie_namen()
        print('\n=== NAMEN ===')
        for naam in OrderedSet(sorted(namen)):
            print(naam)

    def test_commissie_soorten(self):
        namen = get_commissie_soorten()
        print('\n=== SOORTEN ===')
        for naam in OrderedSet(sorted(namen)):
            print(naam)
