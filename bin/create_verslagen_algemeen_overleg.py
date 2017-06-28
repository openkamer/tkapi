import datetime
import sys
import os

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parentdir)

from local_settings import USER, PASSWORD

import tkapi

api = tkapi.Api(user=USER, password=PASSWORD, verbose=True)


def main():
    print('BEGIN')
    year = 2011
    start_datetime = datetime.datetime(year=year, month=1, day=1)
    end_datetime = datetime.datetime(year=year+1, month=1, day=1)
    verslagen = api.get_verslagen_van_algemeen_overleg(start_datetime, end_datetime)
    with open('verslagen_algemeen_overleg_' + str(year) + '.csv', 'w') as fileout:
        header = ','.join(['datum gepubliceerd', 'begin', 'einde', 'dossier nr', 'dossier toevoeging', 'kamerstuk ondernummer', 'url'])
        fileout.write(header + '\n')
        for verslag in verslagen:
            if not verslag.kamerstuk or not verslag.dossier:
                print('WARNING: no kamerstuk or dossier number found for ' + str(verslag.datum))
                continue
            toevoeging = ''
            begin = ''
            end = ''
            if verslag.dossier['Toevoeging']:
                toevoeging = verslag.dossier['Toevoeging']
            if verslag.activiteit and verslag.activiteit.begin and verslag.activiteit.einde:
                begin = verslag.activiteit.begin.isoformat()
                end = verslag.activiteit.einde.isoformat()
            row = ','.join([
                verslag.datum.strftime('%Y-%m-%d'),
                begin,
                end,
                str(verslag.dossier['Vetnummer']),
                toevoeging,
                str(verslag.kamerstuk['Ondernummer']),
                verslag.document_url
            ])
            fileout.write(row + '\n')
    print('END')


if '__main__' == __name__:
    main()
