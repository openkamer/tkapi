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
    year = 2016
    start_datetime = datetime.datetime(year=year, month=1, day=1)
    end_datetime = datetime.datetime(year=year+1, month=1, day=1)
    pd_filter = Document.create_filter()
    pd_filter.filter_date_range(start_datetime, end_datetime)
    verslagen = api.get_verslagen_van_algemeen_overleg(pd_filter)
    with open('verslagen_algemeen_overleg_' + str(year) + '.csv', 'w') as fileout:
        header = ','.join(['datum gepubliceerd', 'dossier nr', 'dossier toevoeging', 'kamerstuk ondernummer', 'url'])
        fileout.write(header + '\n')
        for verslag in verslagen:
            if not verslag.kamerstuk or not verslag.dossier:
                print('WARNING: no kamerstuk or dossier number found for ' + str(verslag.datum))
                continue
            toevoeging = ''
            if verslag.dossier.toevoeging:
                toevoeging = verslag.dossier.toevoeging
            row = ','.join([
                verslag.datum.strftime('%Y-%m-%d'),
                str(verslag.dossier.vetnummer),
                toevoeging,
                str(verslag.kamerstuk.ondernummer),
                verslag.document_url
            ])
            fileout.write(row + '\n')
    print('END')


if '__main__' == __name__:
    main()
