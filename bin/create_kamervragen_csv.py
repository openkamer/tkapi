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
    kamervragen = api.get_kamervragen(start_datetime, end_datetime)
    with open('kamervragen_' + str(year) + '.csv', 'w') as fileout:
        fileout.write('datum' + ',' + 'vraag nummer' + ',' + 'url' + '\n')
        for vraag in kamervragen:
            fileout.write(vraag.datum.strftime('%Y-%m-%d') + ',' + vraag.nummer + ',' + vraag.document_url + '\n')
    print('END')


if '__main__' == __name__:
    main()
