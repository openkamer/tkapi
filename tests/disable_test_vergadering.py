import datetime

from .core import TKApiTestCase
from tkapi.vergadering import Vergadering
from tkapi.info import get_vergadering_soorten


class TestVergadering(TKApiTestCase):
    n_items = 10

    def test_get_vergadering(self):
        uid = '1699235c-f64b-46fe-bce4-e059c2802c29'
        vergadering = self.api.get_item(Vergadering, id=uid)
        self.assertEqual('Plenair', vergadering.soort)
        self.assertEqual('81e vergadering, woensdag 16 mei 2018', vergadering.titel)
        self.assertEqual('Plenaire zaal', vergadering.zaal)
        self.assertEqual(81, vergadering.nummer)
        self.assertIsNotNone(vergadering.begin)
        self.assertIsNotNone(vergadering.einde)
        self.assertEqual('Tweede Kamer', vergadering.samenstelling)
        self.assertEqual(1, len(vergadering.verslagen))
        self.assertEqual(0, len(vergadering.activiteiten))

    def test_get_vergaderingen(self):
        vergaderingen = self.api.get_vergaderingen(max_items=self.n_items)
        self.assertEqual(self.n_items, len(vergaderingen))

    def test_vergadering_filter_soort(self):
        soort = 'Plenair'
        filter = Vergadering.create_filter()
        filter.filter_soort(soort)
        vergaderingen = self.api.get_vergaderingen(filter=filter, max_items=self.n_items)
        self.assertEqual(self.n_items, len(vergaderingen))
        for vergadering in vergaderingen:
            self.assertEqual(soort, vergadering.soort)

    def test_vergadering_filter_date_range(self):
        filter = Vergadering.create_filter()
        begin_datetime = datetime.datetime(year=2017, month=2, day=1)
        end_datetime = datetime.datetime(year=2017, month=3, day=1)
        filter.filter_date_range(begin_datetime=begin_datetime, end_datetime=end_datetime)
        vergaderingen = self.api.get_vergaderingen(filter=filter)
        self.assertEqual(69, len(vergaderingen))

    # def test_get_soorten(self):
    #     soorten = get_vergadering_soorten()
    #     for soort in soorten:
    #         print(soort)
