import unittest

from tkapi import api
from tkapi.document import ParlementairDocument
from tkapi.kamerstuk import Kamerstuk


class TestKamerstuk(unittest.TestCase):

    def test_get_kamerstuk(self):
        ks_uid = '79471b03-156c-4124-9203-0041dee38963'
        kamerstuk = api.get_item(Kamerstuk, ks_uid)
        self.assertEqual(kamerstuk.id, ks_uid)
        self.assertEqual(kamerstuk.ondernummer, '2135')

    def test_get_kamerstukken(self):
        kamerstukken = api.get_kamerstukken(filter=None, max_items=100)
        for kamerstuk in kamerstukken:
            kamerstuk.print_json()

    def test_get_kamerstuk_by_ondernummer(self):
        ondernummer = '82'
        kamerstuk_filter = Kamerstuk.create_filter()
        kamerstuk_filter.filter_ondernummer(ondernummer)
        kamerstukken = api.get_kamerstukken(filter=kamerstuk_filter)
        self.assertTrue(len(kamerstukken) > 100)
        kamerstukken[0].print_json()
        for kamerstuk in kamerstukken:
            self.assertEqual(kamerstuk.ondernummer, ondernummer)
        self.assertGreater(kamerstukken, 0)

    def test_get_kamerstuk_parlementair_document(self):
        ks_uid = '79471b03-156c-4124-9203-0041dee38963'
        kamerstuk = api.get_item(Kamerstuk, ks_uid)
        self.assertEqual(kamerstuk.id, ks_uid)
        self.assertEqual(kamerstuk.ondernummer, '2135')
        pd = kamerstuk.parlementair_document
        pd.print_json()


class TestWetsvoorstellenDossier(unittest.TestCase):

    def test_get_wetsvoorstel_document_without_kamerstuk_and_dossier(self):
        pd_filter = ParlementairDocument.create_filter()
        pd_filter.filter_soort('Voorstel van wet', is_or=True)
        pd_filter.filter_soort('Voorstel van wet (initiatiefvoorstel)', is_or=True)
        pds = api.get_parlementaire_documenten(pd_filter)

        # pds_no_dossier_nr = []
        # for pd in pds:
        #     if not pd.dossier_vetnummer:
        #         pds_no_dossier_nr.append(pd)
        #
        # print('wetsvoorstellen without dossier: ' + str(len(pds_no_dossier_nr)))
        # self.assertEqual(len(pds_no_dossier_nr), 0)
