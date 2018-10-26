import unittest

from tkapi.util import util


class TKApiTestCase(unittest.TestCase):
    api = None

    @classmethod
    def setUpClass(cls):
        cls.api = util.create_api(verbose=True)
        super().setUpClass()
