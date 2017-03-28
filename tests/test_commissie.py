import unittest

import tkapi

from local_settings import USER, PASSWORD

api = tkapi.Api(user=USER, password=PASSWORD)


class TestCommissie(unittest.TestCase):

    def test_get_commissies(self):
        max_items = None
        commissies = api.get_commissies(max_items=max_items)
        for commissie in commissies:
            print('===========')
            print(commissie)
            for lid in commissie.leden:
                if lid.persoon:
                    print('\t' + str(lid))
