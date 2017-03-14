import datetime
import sys

sys.path.append("..")
from tkapi.kamervraag import get_kamervragen


def main():
    print('BEGIN')
    year = 2013
    start_datetime = datetime.datetime(year=year, month=1, day=1)
    end_datetime = datetime.datetime(year=year+1, month=1, day=1)
    kamervragen = get_kamervragen(start_datetime, end_datetime)
    with open('kamervragen_' + str(year) + '.csv', 'w') as fileout:
        fileout.write('datum' + ',' + 'vraag nummer' + ',' + 'url' + '\n')
        for vraag in kamervragen:
            fileout.write(vraag.document.datum.strftime('%Y-%m-%d') + ',' + vraag.document.nummer + ',' + vraag.document_url + '\n')
    print('END')


if '__main__' == __name__:
    main()
