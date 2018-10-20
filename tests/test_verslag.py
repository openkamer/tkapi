import datetime

from tkapi.verslag import VerslagAlgemeenOverleg

from .core import TKApiTestCase
from tkapi.verslag import Verslag
from tkapi.info import get_verslag_soorten


class TestVerslag(TKApiTestCase):
    n_items = 10

    def test_get_verslag(self):
        uid = '28f7d21d-79f1-4591-a0f7-64bb13996a05'
        verslag = self.api.get_item(Verslag, id=uid)
        self.assertEqual('Eindpublicatie', verslag.soort)
        self.assertEqual('Gecorrigeerd', verslag.status)
        self.assertIsNotNone(verslag.vergadering)

    def test_get_verslagen(self):
        verslagen = self.api.get_verslagen(max_items=self.n_items)
        self.assertEqual(self.n_items, len(verslagen))

    def test_verslag_filter_soort(self):
        soort = 'Eindpublicatie'
        filter = Verslag.create_filter()
        filter.filter_soort(soort)
        verslagen = self.api.get_verslagen(filter=filter, max_items=self.n_items)
        self.assertEqual(self.n_items, len(verslagen))
        for verslag in verslagen:
            self.assertEqual(soort, verslag.soort)

    # def test_get_soorten(self):
    #     soorten = get_verslag_soorten()
    #     for soort in soorten:
    #         print(soort)


class TestVerslagAlgemeenOverleg(TKApiTestCase):

    def test_get_verslagen_algemeen_overleg(self):
        start_datetime = datetime.datetime(year=2015, month=1, day=1)
        end_datetime = datetime.datetime(year=2015, month=1, day=20)
        v_filter = VerslagAlgemeenOverleg.create_filter()
        v_filter.filter_date_range(start_datetime, end_datetime)
        verslagen = self.api.get_verslagen_van_algemeen_overleg(v_filter)
        print('verslagen found:',  len(verslagen))
        self.assertEqual(13, len(verslagen))
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
