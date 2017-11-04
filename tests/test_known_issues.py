"""Tests known and reported issues of the OData API, test succeed if issues still exist"""

import datetime
import unittest

from tkapi import api
from tkapi.document import ParlementairDocument
from tkapi.document import ParlementairDocumentFilter


class TestWetsvoorstelWithoutDossier(unittest.TestCase):

    def test_get_wetsvoorstel_document_without_kamerstuk_and_dossier(self):
        """These documents lack a kamerstuk with dossiervetnummer"""
        pd_filter = ParlementairDocumentFilter()
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
        start_datetime = datetime.datetime(year=2014, month=1, day=1)
        end_datetime = datetime.datetime(year=2014, month=2, day=1)
        pd_filter = ParlementairDocumentFilter()
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
