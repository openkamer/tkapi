from tkapi.document import Document

from .core import TKApiTestCase
from tkapi.persoon import Persoon


class TestFilters(TKApiTestCase):

    def test_filter_mixin(self):
        pd_filter = Document.create_filter()
        pd_filter.filter_soort('test soort')
        pd_filter.filter_non_empty_zaak()
        self.assertEqual(len(pd_filter._filters), 2)

    # TODO BR: update with new uid
    # def test_filter_non_deleted(self):
    #     uid = '20415249-f14a-4375-b2c1-36608cbf0a76'
    #     persoon = self.api.get_item(Persoon, id=uid)
    #     functies = persoon.functies
    #     self.assertEqual(1, len(functies))
