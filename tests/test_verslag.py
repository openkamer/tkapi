import datetime
import unittest

from tkapi import api
from tkapi.verslag import VerslagAlgemeenOverleg
from tkapi.document import ParlementairDocument


class TestVerslagAlgemeenOverleg(unittest.TestCase):

    def test_get_verslagen_algemeen_overleg(self):
        start_datetime = datetime.datetime(year=2015, month=1, day=1)
        end_datetime = datetime.datetime(year=2016, month=1, day=1)
        v_filter = VerslagAlgemeenOverleg.create_filter()
        v_filter.filter_date_range(start_datetime, end_datetime)
        verslagen = api.get_verslagen_van_algemeen_overleg(v_filter)
        print('verslagen found: ' + str(len(verslagen)))
        for verslag in verslagen:
            print(verslag.onderwerp)
            if verslag.kamerstuk:
                print(str(verslag.kamerstuk.dossier.vetnummer) + ', ' + str(verslag.kamerstuk.ondernummer))
                print(verslag.document_url)
            # print(verslag.document_url)
            # verslag.kamerstuk.print_json()
            # print(verslag.dossier.titel)
            # for zaak in verslag.zaken:
                # zaak.print_json()
                # print(zaak)
                # for commissie in zaak.voortouwcommissies:
                #     print(commissie.naam)
            # for activiteit in verslag.activiteiten:
            #     verslag.print_json()
                # print(activiteit.begin.isoformat())
                # print(activiteit.einde.isoformat())
