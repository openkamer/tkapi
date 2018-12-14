import datetime
import sys
import os

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parentdir)

import tkapi
from tkapi.document import ParlementairDocument


def main():
    print('BEGIN')
    year = 2017
    api = tkapi.Api(verbose=True)
    start_datetime = datetime.datetime(year=year, month=1, day=1)
    end_datetime = datetime.datetime(year=year+1, month=1, day=1)
    kv_filter = ParlementairDocument.create_filter()
    kv_filter.filter_date_range(start_datetime, end_datetime)
    antwoorden = api.get_antwoorden(kv_filter)
    with open('antwoorden_' + str(year) + '.csv', 'w') as fileout:
        fileout.write('datum' + ',' + 'antwoord nummer' + ',' + 'url' + '\n')
        for antwoord in antwoorden:
            fileout.write(antwoord.datum.strftime('%Y-%m-%d') + ',' + antwoord.nummer + ',' + antwoord.document_url + '\n')
    print('END')


if '__main__' == __name__:
    main()
