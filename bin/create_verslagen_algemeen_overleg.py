import datetime
import sys
import os

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parentdir)

import tkapi
from tkapi.document import Document

api = tkapi.Api(verbose=True)


def main():
    print('BEGIN')
    start_year = 2008
    years = []
    for year in range(start_year, datetime.date.today().year + 1):
        years.append(year)
    print(years)
    for year in years:
        create_verslagen_algemeen_overleg_csv(year)
    print('END')


def create_verslagen_algemeen_overleg_csv(year: int):
    start_datetime = datetime.datetime(year=year, month=1, day=1)
    end_datetime = datetime.datetime(year=year+1, month=1, day=1)
    pd_filter = Document.create_filter()
    pd_filter.filter_date_range(start_datetime, end_datetime)
    verslagen = api.get_verslagen_van_algemeen_overleg(pd_filter)
    with open('../ok-tk-data/verslagen/verslagen_algemeen_overleg_{}.csv'.format(year), 'w') as fileout:
        header = ','.join(['datum gepubliceerd', 'dossier nr', 'dossier toevoeging', 'kamerstuk volgnummer', 'url', 'commissie'])
        fileout.write(header + '\n')
        for verslag in verslagen:
            if not verslag.dossiers:
                print('WARNING: no dossier found for verslag', verslag.nummer)
                continue
            if not verslag.volgnummer or not verslag.dossiers:
                print('WARNING: no kamerstuk or dossier number found for verslag', verslag.nummer)
                continue
            dossier = verslag.dossiers[0]
            toevoeging = ''
            if dossier.toevoeging:
                toevoeging = dossier.toevoeging
            row = ','.join([
                verslag.datum.strftime('%Y-%m-%d'),
                str(dossier.nummer),
                toevoeging,
                str(verslag.volgnummer),
                verslag.document_url,
                '\"{}\"'.format(verslag.voortouwcommissie_namen[0]) if verslag.voortouwcommissie_namen else ''
            ])
            print(row)
            fileout.write(row + '\n')


if '__main__' == __name__:
    main()
