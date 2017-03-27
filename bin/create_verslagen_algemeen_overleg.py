import datetime
import sys

sys.path.append("..")
from tkapi.verslag import get_verslagen_van_algemeen_overleg


def main():
    print('BEGIN')
    year = 2015
    start_datetime = datetime.datetime(year=year, month=1, day=1)
    end_datetime = datetime.datetime(year=year+1, month=1, day=1)
    verslagen = get_verslagen_van_algemeen_overleg(start_datetime, end_datetime)
    with open('verslagen_algemeen_overleg_' + str(year) + '.csv', 'w') as fileout:
        header = ','.join(['datum gepubliceerd', 'begin', 'einde', 'dossier nr', 'dossier toevoeging', 'kamerstuk ondernummer', 'url'])
        fileout.write(header + '\n')
        for verslag in verslagen:
            if not verslag.kamerstuk or not verslag.dossier:
                print('WARNING: no kamerstuk or dossier number found for ' + str(verslag.document.datum))
                continue
            toevoeging = ''
            begin = ''
            end = ''
            if verslag.dossier['Toevoeging']:
                toevoeging = verslag.dossier['Toevoeging']
            if verslag.activiteit:
                begin = verslag.activiteit.begin.isoformat()
                end = verslag.activiteit.end.isoformat()
            row = ','.join([
                verslag.document.datum.strftime('%Y-%m-%d'),
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
