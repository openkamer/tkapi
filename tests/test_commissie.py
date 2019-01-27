from orderedset import OrderedSet

from tkapi.commissie import Commissie
from tkapi.info import get_commissie_namen
from tkapi.info import get_commissie_soorten

from .core import TKApiTestCase


class TestCommissie(TKApiTestCase):

    def test_get_commissies(self):
        max_items = None
        commissies = self.api.get_commissies(max_items=max_items)
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
        print('\n=====Commissies=====')
        for commissie in commissies_with_name:
            print(commissie.naam)
        print('\n=====Commissie Soorten=====')
        for soort in soorten:
            print(soort)
        print('\n=====Commissies Incomplete=====')
        print('commissies without soort: ' + str(len(commissies_without_soort)))
        print('commissies without name: ' + str(len(commissies_without_name)))

    #TODO BR: update uid
    # def test_get_leden(self):
    #     uid = '1349488c-8474-4704-bdad-26fa54ea9789'
    #     commissie = self.api.get_item(Commissie, id=uid)
    #     zetels = commissie.zetels_aantal
    #     self.assertEqual(319, len(zetels))
    #     self.assertEqual(2, len(zetels[1].personen_vast))
    #     self.assertEqual('Oosten', zetels[1].personen_vast[0].persoon.achternaam)

    def test_soort_filter(self):
        soort = 'Algemeen'
        com_filter = Commissie.create_filter()
        com_filter.filter_soort(soort)
        commissies_algemeen = self.api.get_commissies(com_filter)
        self.assertTrue(len(commissies_algemeen) >= 5)
        for commissie in commissies_algemeen:
            self.assertEqual(commissie.soort, soort)
        print('Algemene commissies found: ' + str(len(commissies_algemeen)))

    def test_naam_filter(self):
        naam = 'Vaste commissie voor Binnenlandse Zaken'
        com_filter = Commissie.create_filter()
        com_filter.filter_naam(naam)
        commissies_algemeen = self.api.get_commissies(com_filter)
        commissies_algemeen[0].print_json()
        self.assertTrue(len(commissies_algemeen), 1)
        for commissie in commissies_algemeen:
            self.assertEqual(commissie.naam, naam)


class TestCommissieInfo(TKApiTestCase):

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


# class TestCommissieActiviteit(TKApiTestCase):
#
#     def test_get_activiteit_actor(self):
#         activiteiten = self.api.get_activiteiten(filter=None, max_items=50)
#         for activiteit in activiteiten:
#             # activiteit.print_json()
#             if activiteit.json['Voortouwcommissie']:
#                 print('has Voortouwcommissie')
#                 print(activiteit.json['Voortouwcommissie']['Commissie']['NaamNL'])
#             if activiteit.json['Document']:
#                 print('has Document')
#             # print(activiteit.json['Voortouwcommissie'])
#             # print(activiteit.json['Document'])
#         print(len(activiteiten))
