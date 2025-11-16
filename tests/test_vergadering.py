import datetime

from tkapi.vergadering import Vergadering
from tkapi.vergadering import VergaderingSoort

from .core import TKApiTestCase


class TestVergadering(TKApiTestCase):

    def test_get_vergaderingen(self):
        max_items = 10
        vergaderingen = self.api.get_vergaderingen(filter=None, max_items=max_items)
        self.assertEqual(max_items, len(vergaderingen))
        for vergadering in vergaderingen:
            self.assertIsNotNone(vergadering.soort)
            self.assertIsNotNone(vergadering.verslag)
            self.assertIsNotNone(vergadering.datum)
            self.assertIsNotNone(vergadering.begin)
            self.assertIsNotNone(vergadering.nummer)

    def test_get_vergadering_soorten(self):
        max_items = 100
        vergaderingen = self.api.get_vergaderingen(filter=None, max_items=max_items)
        self.assertEqual(max_items, len(vergaderingen))
        soorten = set()
        for vergadering in vergaderingen:
            soorten.add(vergadering.soort)
        self.assertGreaterEqual(len(soorten), 1)


class TestVergaderingFilter(TKApiTestCase):

    def test_vergadering_soort_filter(self):
        max_items = 10
        filter = Vergadering.create_filter()
        filter.filter_soort(soort=VergaderingSoort.COMMISSIE)
        vergaderingen = self.api.get_vergaderingen(filter=filter, max_items=max_items)
        self.assertEqual(max_items, len(vergaderingen))
        self.assertTrue(
            all([VergaderingSoort.COMMISSIE == vergadering.soort for vergadering in vergaderingen])
        )

    def test_veradering_changed_since_filter(self):
        max_items = 10
        filter_dt = datetime.datetime(2023, 1, 1, 00, 00, tzinfo=datetime.timezone.utc)
        filter = Vergadering.create_filter()
        filter.filter_changed_since(filter_dt)
        vergaderingen = self.api.get_vergaderingen(filter=filter, max_items=max_items)
        self.assertTrue(
            all([vergadering.gewijzigd_op >= filter_dt for vergadering in vergaderingen])
        )

    def test_vergadering_date_range_filter(self):
        max_items = 10
        begin_datetime = datetime.datetime(2023, 1, 1, 00, 00, tzinfo=datetime.timezone.utc)
        end_datetime = datetime.datetime(2023, 12, 31, 23, 59, tzinfo=datetime.timezone.utc)
        filter = Vergadering.create_filter()
        filter.filter_date_range(begin_datetime, end_datetime)
        vergaderingen = self.api.get_vergaderingen(filter=filter, max_items=max_items)
        self.assertTrue(
            all([vergadering.begin >= begin_datetime for vergadering in vergaderingen if vergadering.begin])
        )
        self.assertTrue(
            all([vergadering.einde < end_datetime for vergadering in vergaderingen if vergadering.einde])
        )
