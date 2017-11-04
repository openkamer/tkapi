import unittest

from tkapi.document import ParlementairDocumentFilter


class TestFilters(unittest.TestCase):

    def test_filter_mixin(self):
        pd_filter = ParlementairDocumentFilter()
        pd_filter.filter_soort('test soort')
        pd_filter.filter_empty_zaak()
        self.assertEqual(len(pd_filter.filters), 2)
