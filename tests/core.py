import unittest

from tkapi.util import create_api


class TKApiTestCase(unittest.TestCase):
    api = None

    @classmethod
    def setUpClass(cls):
        cls.api = create_api(verbose=True)
        super().setUpClass()
