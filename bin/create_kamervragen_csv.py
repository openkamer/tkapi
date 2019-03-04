import datetime
import sys
import os

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parentdir)

import tkapi

from tkapi.document import Document


def main():
    print('BEGIN')
    # years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
    # years = [2017, 2018]
    years = [2019]
    month = 1

    out_dir = os.path.join(parentdir, '../ok-tk-data/kamervragen/')

    api = tkapi.Api(verbose=True)

    for year in years:
        start_datetime = datetime.datetime(year=year, month=month, day=1)
        end_datetime = datetime.datetime(year=year+1, month=month, day=1)
        kv_filter = Document.create_filter()
        kv_filter.filter_date_range(start_datetime, end_datetime)
        kamervragen = api.get_kamervragen(kv_filter)
        with open(os.path.join(out_dir, 'kamervragen_' + str(year) + '.csv'), 'w') as fileout:
            fileout.write('datum' + ',' + 'vraag nummer' + ',' + 'url' + '\n')
            for vraag in kamervragen:
                fileout.write(vraag.datum.strftime('%Y-%m-%d') + ',' + vraag.nummer + ',' + vraag.document_url + '\n')
    print('END')


if '__main__' == __name__:
    main()
