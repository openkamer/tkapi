import datetime
import unittest

from tkapi import api


class TestActiviteit(unittest.TestCase):
    start_datetime = datetime.datetime(year=2017, month=1, day=1)
    end_datetime = datetime.datetime(year=2017, month=2, day=1)

    def test_get_activiteiten(self):
        activiteiten = api.get_activiteiten(filter=None, max_items=50)
        soorten = set()
        for activiteit in activiteiten:
            # activiteit.print_json()
            soorten.add(activiteit.soort)
        for soort in soorten:
            print(soort)

    def test_activiteit_voortouwcommissies(self):
        activiteiten = api.get_activiteiten(filter=None, max_items=1000)
        for activiteit in activiteiten:
            if 'Voortouwcommissie' in activiteit.json and activiteit.json['Voortouwcommissie'] is not None:
                if 'Commissie' in activiteit.json['Voortouwcommissie']:
                    print(activiteit.json['Voortouwcommissie']['Commissie']['Id'])
                    print(activiteit.json['Voortouwcommissie']['Commissie']['NaamNL'])

    def test_activiteit_documenten(self):
        activiteiten = api.get_activiteiten(filter=None, max_items=200)
        for activiteit in activiteiten:
            for pd in activiteit.parlementaire_documenten:
                if pd.kamerstuk:
                    print(pd.kamerstuk.dossier.vetnummer)
                print(pd.onderwerp)
