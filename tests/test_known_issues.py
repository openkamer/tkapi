import datetime
import unittest

from tkapi import api
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
