import datetime
import sys
import os

from orderedset import OrderedSet

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parentdir)

import tkapi
from tkapi.document import ParlementairDocument

from local_settings import USER, PASSWORD

api = tkapi.Api(user=USER, password=PASSWORD, verbose=True)


def main():
    print('BEGIN')
    pd_filter = ParlementairDocument.create_filter()
    # start_datetime = datetime.datetime(year=2016, month=1, day=1)
    # end_datetime = datetime.datetime(year=2017, month=6, day=1)
    # pd_filter.filter_date_range(start_datetime, end_datetime)
    pd_filter.filter_soort('Voorstel van wet', is_or=True)
    pd_filter.filter_soort('Voorstel van wet (initiatiefvoorstel)', is_or=True)
    pds = api.get_parlementaire_documenten(pd_filter)

    dossier_nrs = []
    pds_no_dossier_nr = []
    for pd in pds:
        if pd.dossier_vetnummer:
            dossier_nrs.append(pd.dossier_vetnummer)
        else:
            pds_no_dossier_nr.append(pd)
    for pd in pds_no_dossier_nr:
        try:
            dossier_nr = int(pd.onderwerp.split('Voorstel van wet')[0].strip())
            dossier_nrs.append(dossier_nr)
        except TypeError:
            continue

    dossier_nrs = OrderedSet(sorted(dossier_nrs))
    print(dossier_nrs)
    for dossier_nr in dossier_nrs:
        print(dossier_nr)
    print(len(dossier_nrs))

    with open('wetsvoorstellen_dossier_ids' + '.txt', 'w') as fileout:
        for dossier_nr in dossier_nrs:
            fileout.write(str(dossier_nr) + '\n')
    print('END')


if '__main__' == __name__:
    main()
