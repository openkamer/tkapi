from tkapi.commissie import Commissie
from tkapi.commissie import CommissieZetel
from tkapi.commissie import CommissieZetelVastPersoon
from tkapi.commissie import CommissieZetelVervangerPersoon
from tkapi.commissie import CommissieFunctie
from tkapi.commissie import CommissieZetelVastVacature
from tkapi.commissie import CommissieZetelVervangerVacature
from tkapi.commissie import CommissieContactinformatie
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
            if commissie.soort != '':
                soorten.add(commissie.soort)
            else:
                commissies_without_soort.append(commissie)
            if commissie.naam != '':
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
        self.assertEqual(0, len(commissies_without_name))
        self.assertGreaterEqual(len(commissies_without_soort), 60)

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
        self.assertGreaterEqual(len(commissies_algemeen), 4)
        for commissie in commissies_algemeen:
            self.assertEqual(commissie.soort, soort)
        print('Algemene commissies found: ' + str(len(commissies_algemeen)))

    def test_naam_filter(self):
        naam = 'Vaste commissie voor Binnenlandse Zaken'
        filter = Commissie.create_filter()
        filter.filter_naam(naam)
        commissies = self.api.get_commissies(filter=filter)
        self.assertTrue(len(commissies), 1)
        commissie = commissies[0]
        self.assertEqual(naam, commissie.naam)

    def test_get_commissies_zetels(self):
        max_items = 5
        commissies = self.api.get_commissies(max_items=max_items)
        self.assertEqual(max_items, len(commissies))
        for commissie in commissies:
            print(len(commissie.zetels))
            self.assertNotEqual(0, len(commissie.zetels))


class TestCommissieInfo(TKApiTestCase):

    def test_commissie_namen(self):
        namen = get_commissie_namen()
        print('\n=== NAMEN ===')
        self.assertGreater(len(namen), 50)
        for naam in sorted(set(namen)):
            print(naam)

    def test_commissie_soorten(self):
        namen = get_commissie_soorten()
        self.assertGreater(len(namen), 6)
        print('\n=== SOORTEN ===')
        for naam in sorted(set(namen)):
            print(naam)


class TestCommissieZetel(TKApiTestCase):

    def get_commissie_binnenlandse_zaken(self):
        naam = 'Vaste commissie voor Binnenlandse Zaken'
        com_filter = Commissie.create_filter()
        com_filter.filter_naam(naam)
        commissies = self.api.get_commissies(com_filter)
        self.assertEqual(1, len(commissies))
        return commissies[0]

    def test_get_commissie_zetels(self):
        max_items = 10
        zetels = self.api.get_items(CommissieZetel, max_items=max_items)
        self.assertEqual(max_items, len(zetels))
        for zetel in zetels:
            self.assertIsNotNone(zetel.commissie)

    def test_get_commissie_zetels_active(self):
        commissie = self.get_commissie_binnenlandse_zaken()
        filter = CommissieZetel.create_filter()
        filter.filter_commissie(commissie)
        filter.filter_active()
        zetels = self.api.get_items(CommissieZetel, filter=filter)
        personen = set()
        for zetel in zetels:
            for persoon in zetel.personen_vast_active:
                self.assertIsNone(persoon.tot_en_met)
                if persoon.persoon is not None:
                    print('vast: {} | tot en met: {}'.format(persoon.persoon.achternaam, persoon.tot_en_met))
                    personen.add(persoon.persoon.achternaam)
            for persoon in zetel.personen_vervangend_active:
                self.assertIsNone(persoon.tot_en_met)
                print('vervangend: {} | tot en met: {}'.format(persoon.persoon.achternaam, persoon.tot_en_met))
                personen.add(persoon.persoon.achternaam)
        self.assertGreater(len(zetels), 10)
        self.assertGreater(len(personen), 20)
        print('zetels: {}'.format(len(zetels)))
        print('personen: {}'.format(len(personen)))

    def test_filter_commissie(self):
        max_items = 10
        commissie = self.get_commissie_binnenlandse_zaken()
        filter = CommissieZetel.create_filter()
        filter.filter_commissie(commissie)
        zetels = self.api.get_items(CommissieZetel, filter=filter, max_items=max_items)
        self.assertEqual(len(zetels), max_items)
        for zetel in zetels:
            self.assertEqual(commissie.id, zetel.commissie.id)


class TestCommissieZetelPersoon(TKApiTestCase):

    def get_commissie_binnenlandse_zaken(self):
        naam = 'Vaste commissie voor Binnenlandse Zaken'
        com_filter = Commissie.create_filter()
        com_filter.filter_naam(naam)
        commissies = self.api.get_commissies(com_filter)
        self.assertEqual(1, len(commissies))
        return commissies[0]

    def test_get_items_vast(self):
        max_items = 5
        vasts = self.api.get_items(CommissieZetelVastPersoon, max_items=max_items)
        self.assertEqual(max_items, len(vasts))
        for vast in vasts:
            self.assertIsNotNone(vast.persoon.achternaam)
            self.assertIsNotNone(vast.van)
            self.assertIsNotNone(vast.functie)

    def test_get_items_vervangend(self):
        max_items = 5
        vervangend = self.api.get_items(CommissieZetelVervangerPersoon, max_items=max_items)
        self.assertEqual(max_items, len(vervangend))

    def test_filter_active(self):
        max_items = 20
        filter = CommissieZetelVastPersoon.create_filter()
        filter.filter_active()
        vast_personen = self.api.get_items(CommissieZetelVastPersoon, filter=filter, max_items=max_items)
        self.assertEqual(max_items, len(vast_personen))
        for vast_persoon in vast_personen:
            self.assertIsNone(vast_persoon.tot_en_met)

    def test_filter_functie(self):
        max_items = 20
        functie_expected = CommissieFunctie.VOORZITTER
        filter = CommissieZetelVastPersoon.create_filter()
        filter.filter_functie(functie_expected)
        vast_personen = self.api.get_items(CommissieZetelVastPersoon, filter=filter, max_items=max_items)
        self.assertEqual(max_items, len(vast_personen))
        for vast_persoon in vast_personen:
            self.assertEqual(functie_expected, vast_persoon.functie)

    def test_filter_commissie(self):
        max_items = 5
        commissie = self.get_commissie_binnenlandse_zaken()
        filter = CommissieZetelVastPersoon.create_filter()
        filter.filter_commissie(commissie)
        vast_personen = self.api.get_items(CommissieZetelVastPersoon, filter=filter, max_items=max_items)
        for vast_persoon in vast_personen:
            self.assertEqual(commissie.id, vast_persoon.zetel.commissie.id)


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


class TestCommissieZetelVastVacature(TKApiTestCase):

    def test_get_items(self):
        max_items = 5
        vacs = self.api.get_items(CommissieZetelVastVacature, max_items=max_items)
        self.assertEqual(max_items, len(vacs))
        fracties = set()
        for vac in vacs:
            self.assertIn(vac.functie, CommissieFunctie)
            if vac.fractie:
                fracties.add(vac.fractie)
            self.assertIsNotNone(vac.zetel)
            self.assertTrue(vac.van)
        self.assertGreater(len(fracties), 1)


class TestCommissieZetelVervangerVacature(TKApiTestCase):

    def test_get_items(self):
        max_items = 5
        vacs = self.api.get_items(CommissieZetelVervangerVacature, max_items=max_items)
        self.assertEqual(max_items, len(vacs))
        for vac in vacs:
            self.assertIn(vac.functie, CommissieFunctie)
            self.assertIsNotNone(vac.fractie)
            self.assertIsNotNone(vac.zetel)
            self.assertTrue(vac.van)


class TestCommissieContactinformatie(TKApiTestCase):

    def test_get_items(self):
        max_items = 5
        infos = self.api.get_items(CommissieContactinformatie, max_items=max_items)
        self.assertEqual(max_items, len(infos))
        for info in infos:
            self.assertIsNotNone(info.commissie)
            self.assertTrue(info.soort)
            self.assertTrue(info.waarde)
            print(info.commissie.naam, info.soort, info.waarde)
