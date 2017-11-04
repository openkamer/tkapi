"""Tests known and reported issues of the OData API, test succeed if issues still exist"""

import datetime
import unittest

from tkapi import api
from tkapi.activiteit import Activiteit
from tkapi.besluit import Besluit
from tkapi.document import ParlementairDocument


class TestWetsvoorstelWithoutDossier(unittest.TestCase):

    def test_get_wetsvoorstel_document_without_kamerstuk_and_dossier(self):
        """These documents lack a kamerstuk with dossiervetnummer"""
        pd_filter = ParlementairDocument.create_filter()
        pd_filter.filter_soort('Voorstel van wet', is_or=True)
        pd_filter.filter_soort('Voorstel van wet (initiatiefvoorstel)', is_or=True)
        pds = api.get_parlementaire_documenten(pd_filter)

        pds_no_dossier_nr = []
        for pd in pds:
            if not pd.dossier_vetnummer:
                pds_no_dossier_nr.append(pd)

        print(len(pds_no_dossier_nr))

        self.assertTrue(len(pds_no_dossier_nr) >= 28)

        for pd in pds_no_dossier_nr:
            self.assertIsNone(pd.kamerstuk)
            print(pd.id + ', ' + str(pd.nummer))
            # print(pd.nummer)
            # print(pd.onderwerp)
            # print(pd.kamerstuk)


class TestKamervragen(unittest.TestCase):

    def test_get_kamervragen_2013(self):
        """These kamervragen have no Zaak (essential to match with kamerantwoord)"""
        start_datetime = datetime.datetime(year=2013, month=1, day=1)
        end_datetime = datetime.datetime(year=2013, month=2, day=1)
        pd_filter = ParlementairDocument.create_filter()
        pd_filter.filter_date_range(start_datetime, end_datetime)
        pd_filter.filter_soort('Schriftelijke vragen')
        schriftelijke_vragen = api.get_parlementaire_documenten(pd_filter)
        kamervragen_no_zaak = []
        for kamervraag in schriftelijke_vragen:
            if not kamervraag.zaken:
                kamervragen_no_zaak.append(kamervraag)
        # for kamervraag in kamervragen_no_zaak:
            # print(kamervraag.zaken)
        print('kamervragen without zaak: ' + str(len(kamervragen_no_zaak)))
        self.assertTrue(len(kamervragen_no_zaak) >= 249)

    def test_get_kamervraag_wrong_alias(self):
        parlementair_document_id = 'f629d66b-42c1-493f-b081-c4e1ef8c99e1'
        pd = api.get_item(ParlementairDocument, parlementair_document_id)
        self.assertEqual(pd.alias, '2080904960 2080904960')  # this should simply be '2080904960'


class TestCommissies(unittest.TestCase):

    def test_commissie_info_missing(self):
        commissies = api.get_commissies()
        commissies_without_name = []
        commissies_with_name = []
        commissies_with_soort = []
        for commissie in commissies:
            if not commissie.naam:
                commissies_without_name.append(commissie)
            if not commissie.soort:
                commissies_with_soort.append(commissie)
            else:
                commissies_with_name.append(commissie)
        # for commissie in commissies_without_name:
        #     print(commissie.id)
        self.assertTrue(len(commissies_without_name) >= 130)
        self.assertTrue(len(commissies_with_soort) >= 191)


class TestBesluit(unittest.TestCase):

    def test_besluiten_without_zaak(self):
        besluit_filter = Besluit.create_filter()
        besluit_filter.filter_empty_zaak()
        besluiten = api.get_besluiten(filter=besluit_filter)
        self.assertEqual(len(besluiten), 0)  # Not a single Besluit has a Zaak


class TestActiviteit(unittest.TestCase):

    def test_activiteit_without_zaak(self):
        activiteit_filter = Activiteit.create_filter()
        activiteiten = api.get_activiteiten(filter=activiteit_filter, max_items=100)
        activiteiten_without_zaak = []
        for activiteit in activiteiten:
            if not activiteit.zaken:
                activiteiten_without_zaak.append(activiteit)
        print('Actvititeiten without zaak: ' + str(len(activiteiten_without_zaak)))
        self.assertTrue(len(activiteiten_without_zaak) >= 96)
