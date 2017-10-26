import datetime
import unittest

from tkapi import api
from tkapi.document import ParlementairDocumentFilter


class TestParlementairDocument(unittest.TestCase):
    start_datetime = datetime.datetime(year=2017, month=1, day=1)
    end_datetime = datetime.datetime(year=2017, month=6, day=1)

    def test_get_voorstel_van_wet(self):
        pd_filter = ParlementairDocumentFilter()
        pd_filter.filter_date_range(
            TestParlementairDocument.start_datetime,
            TestParlementairDocument.end_datetime
        )
        pd_filter.filter_soort('Voorstel van wet')
        # print(pd_filter.filter_str)
        pds = api.get_parlementaire_documenten(pd_filter)
        for pd in pds:
            print(pd.titel)
            print(pd.activiteit)
            # pd.print_json()
            # print('\t' + str(pd.dossier.vetnummer))
            # print('\t dossier afgesloten: ' + str(pd.dossier.afgesloten))
            # pd.dossier.print_json()
            # print(pd.dossier.afgesloten)
            # print(pd.dossier.kamerstukken)
            # for zaak in pd.dossier.zaken:
            #     print('\t zaak afgedaan: ' + str(zaak.afgedaan))
            #     print('\t zaak soort: ' + str(zaak.soort))
            #     print('\t zaak soort: ' + str(zaak.nummer))

