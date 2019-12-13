import datetime

from tkapi import TKApi
from tkapi.zaak import Zaak
from tkapi.zaak import ZaakSoort


def example_kamervragen():
    """Example that shows how to get kamervragen and antwoorden for a date range."""
    filter = Zaak.create_filter()
    begin_datetime = datetime.datetime(year=2015, month=1, day=1)
    end_datetime = datetime.datetime(year=2015, month=1, day=10)
    filter.filter_date_range(begin_datetime, end_datetime)
    filter.filter_soort(ZaakSoort.SCHRIFTELIJKE_VRAGEN)
    zaken = TKApi.get_zaken(filter=filter)
    for zaak in zaken:
        for doc in zaak.documenten:
            print('{}: {}'.format(doc.soort.value, doc.onderwerp))


if '__main__' == __name__:
    example_kamervragen()
