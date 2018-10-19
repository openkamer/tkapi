"""Tests known and reported issues of the ODataself.api, test succeed if issues still exist"""
from tkapi.besluit import Besluit

from .core import TKApiTestCase


# class TestCommissies(TKApiTestCase):
#
#     def test_commissie_info_missing(self):
#         commissies = self.api.get_commissies()
#         commissies_without_name = []
#         commissies_with_name = []
#         commissies_with_soort = []
#         for commissie in commissies:
#             if not commissie.naam:
#                 commissies_without_name.append(commissie)
#             if not commissie.soort:
#                 commissies_with_soort.append(commissie)
#             else:
#                 commissies_with_name.append(commissie)
#         # for commissie in commissies_without_name:
#         #     print(commissie.id)
#         print('commissies without name: ' + str(len(commissies_with_name)))
#         print('commissies without soort: ' + str(len(commissies_with_soort)))
#         self.assertGreater(len(commissies_without_name), 41)
#         self.assertGreater(len(commissies_with_soort), 100)


# class TestBesluit(TKApiTestCase):
#
#     def test_besluiten_without_zaak(self):
#         besluit_filter = Besluit.create_filter()
#         besluit_filter.filter_empty_zaak()
#         besluiten = self.api.get_besluiten(filter=besluit_filter)
#         self.assertEqual(len(besluiten), 0)  # Not a single Besluit has a Zaak


# class TestActiviteit(TKApiTestCase):
#
#     def test_activiteit_without_zaak(self):
#         activiteit_filter = Activiteit.create_filter()
#         activiteiten = self.api.get_activiteiten(filter=activiteit_filter, max_items=100)
#         activiteiten_without_zaak = []
#         for activiteit in activiteiten:
#             if not activiteit.zaken:
#                 activiteiten_without_zaak.append(activiteit)
#         print('Actvititeiten without zaak: ' + str(len(activiteiten_without_zaak)))
#         self.assertTrue(len(activiteiten_without_zaak) >= 90)
