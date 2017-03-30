import datetime
import sys

sys.path.append("..")
import tkapi

from local_settings import USER, PASSWORD


def main():
    print('BEGIN')
    year = 2017
    api = tkapi.Api(user=USER, password=PASSWORD, verbose=True)
    start_datetime = datetime.datetime(year=year, month=1, day=1)
    end_datetime = datetime.datetime(year=year+1, month=1, day=1)
    antwoorden = api.get_antwoorden(start_datetime, end_datetime)
    with open('antwoorden_' + str(year) + '.csv', 'w') as fileout:
        fileout.write('datum' + ',' + 'antwoord nummer' + ',' + 'url' + '\n')
        for antwoord in antwoorden:
            fileout.write(antwoord.datum.strftime('%Y-%m-%d') + ',' + antwoord.nummer + ',' + antwoord.document_url + '\n')
    print('END')


if '__main__' == __name__:
    main()
