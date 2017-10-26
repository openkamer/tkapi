import datetime
import unittest

from tkapi import api
from tkapi.document import ParlementairDocument
from tkapi.document import ParlementairDocumentFilter

class TestActiviteit(unittest.TestCase):
    start_datetime = datetime.datetime(year=2017, month=1, day=1)
    end_datetime = datetime.datetime(year=2017, month=2, day=1)

    def test_get_activiteiten(self):
        activiteiten = api.get_activiteiten(max_items=50)
        soorten = set()
        for activiteit in activiteiten:
            # activiteit.print_json()
            soorten.add(activiteit.soort)
        for soort in soorten:
            print(soort)
