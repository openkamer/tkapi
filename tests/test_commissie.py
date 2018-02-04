import unittest
from orderedset import OrderedSet

from tkapi import api
from tkapi.commissie import Commissie
from tkapi.info import get_commissie_namen
from tkapi.info import get_commissie_soorten


class TestCommissie(unittest.TestCase):

    def test_get_commissies(self):
        max_items = None
        commissies = api.get_commissies(max_items=max_items)
        soorten = set()
        commissies_without_soort = []
        commissies_without_name = []
        commissies_with_name = []
        for commissie in commissies:
            # commissie.print_json()
            if commissie.soort is not '':
                soorten.add(commissie.soort)
            else:
                commissies_without_soort.append(commissie)
            if commissie.naam is not '':
                commissies_with_name.append(commissie)
            else:
                commissies_without_name.append(commissie)
            if commissie.naam:
                print('===========')
                print(commissie)
                print(commissie.soort)
                for lid in commissie.leden:
                    if lid.persoon:
                        print('\t' + str(lid))
        print('\n=====Commissies=====')
        for commissie in commissies_with_name:
            print(commissie.naam)
        print('\n=====Commissie Soorten=====')
        for soort in soorten:
            print(soort)
        print('\n=====Commissies Incomplete=====')
        print('commissies without soort: ' + str(len(commissies_without_soort)))
        print('commissies without name: ' + str(len(commissies_without_name)))

    def test_soort_filter(self):
        soort = 'Algemeen'
        com_filter = Commissie.create_filter()
        com_filter.filter_soort(soort)
        commissies_algemeen = api.get_commissies(com_filter)
        self.assertTrue(len(commissies_algemeen) >= 5)
        for commissie in commissies_algemeen:
            self.assertEqual(commissie.soort, soort)
        print('Algemene commissies found: ' + str(len(commissies_algemeen)))

    def test_naam_filter(self):
        naam = 'Vaste commissie voor Binnenlandse Zaken'
        com_filter = Commissie.create_filter()
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


class TestCommissieActiviteit(unittest.TestCase):

    def test_get_activiteit_actor(self):
        activiteiten = api.get_activiteiten(filter=None, max_items=50)
        for activiteit in activiteiten:
            # activiteit.print_json()
            if activiteit.json['Voortouwcommissie']:
                print('has Voortouwcommissie')
                print(activiteit.json['Voortouwcommissie']['Commissie']['NaamNL'])
            if activiteit.json['ParlementairDocument']:
                print('has ParlementairDocument')
            # print(activiteit.json['Voortouwcommissie'])
            # print(activiteit.json['ParlementairDocument'])
        print(len(activiteiten))
