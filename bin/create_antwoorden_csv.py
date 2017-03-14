import datetime
import sys

sys.path.append("..")
from tkapi.kamervraag import get_antwoorden


def main():
    print('BEGIN')
    year = 2013
    start_datetime = datetime.datetime(year=year, month=1, day=1)
    end_datetime = datetime.datetime(year=year+1, month=1, day=1)
    antwoorden = get_antwoorden(start_datetime, end_datetime)
    with open('antwoorden_' + str(year) + '.csv', 'w') as fileout:
        fileout.write('datum' + ',' + 'antwoord nummer' + ',' + 'url' + '\n')
        for antwoord in antwoorden:
            fileout.write(antwoord.document.datum.strftime('%Y-%m-%d') + ',' + antwoord.document.nummer + ',' + antwoord.document_url + '\n')
    print('END')


if '__main__' == __name__:
    main()
