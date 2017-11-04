import datetime
import unittest

from tkapi import api
from tkapi.stemming import Stemming


class TestStemming(unittest.TestCase):

    def test_get_stemmingen(self):
        stemmingen = api.get_stemmingen(filter=None, max_items=2)
        for stemming in stemmingen:
            stemming.print_json()
            # stemming.besluit.print_json()
    #
    # def test_get_dossier_by_vetnummer(self):
    #     vetnummer = 34435
    #     filter = Dossier.create_filter()
    #     filter.filter_vetnummer(vetnummer)
    #     dossiers = api.get_dossiers(filter=filter)
    #     self.assertEqual(len(dossiers), 1)
    #     dossiers[0].print_json()
    #
    # def test_dossier_filter(self):
    #     self.check_dossier_filter('2016Z16486', 34537)
    #     self.check_dossier_filter('2016Z24906', 34640)
    #
    # def check_dossier_filter(self, zaak_nr, expected_dossier_vetnummer):
    #     dossier_filter = Dossier.create_filter()
    #     dossier_filter.filter_zaak(zaak_nr)
    #     dossiers = api.get_dossiers(filter=dossier_filter)
    #     for dossier in dossiers:
    #         dossier.print_json()
    #     self.assertEqual(len(dossiers), 1)
    #     # print(dossiers[0].vetnummer)
    #     self.assertEqual(dossiers[0].vetnummer, expected_dossier_vetnummer)
    #
