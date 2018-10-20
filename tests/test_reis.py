import datetime

from tkapi.reis import Reis

from .core import TKApiTestCase


class TestReis(TKApiTestCase):

    def test_get_reizen(self):
        n_items = 20
        reizen = self.api.get_reizen(max_items=n_items)
        print('reizen:', len(reizen))
        self.assertEqual(n_items, len(reizen))
        for reis in reizen:
            print(reis.bestemming)
            print(reis.doel)
            print(reis.van, reis.tot_en_met)
            print(reis.betaald_door)
            self.assertIsNotNone(reis.bestemming)
            self.assertIsNotNone(reis.doel)
            self.assertIsNotNone(reis.van)
            self.assertIsNotNone(reis.tot_en_met)
            self.assertIsNotNone(reis.betaald_door)
