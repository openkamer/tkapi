import unittest

from tkapi import api


class TestPersoon(unittest.TestCase):

    def test_get_personen(self):
        max_items = 66
        personen = api.get_personen(max_items=max_items)
        for persoon in personen:
            print(persoon)
            print(persoon['Achternaam'])
        self.assertEqual(len(personen), max_items)
