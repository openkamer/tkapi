import unittest

import tkapi.persoon
import tkapi.util


class TestPersoon(unittest.TestCase):

    def test_get_personen(self):
        max_items = 100
        personen = tkapi.persoon.get_personen(max_items=max_items)
        for persoon in personen:
            print(persoon)
        self.assertEqual(len(personen), 100)
