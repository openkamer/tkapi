import datetime
import sys
import os

from orderedset import OrderedSet

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parentdir)

import tkapi
from tkapi.zaak import Zaak, ZaakSoort

api = tkapi.Api(verbose=True)

out_dir = os.path.join(parentdir, '../ok-tk-data/wetsvoorstellen/')


def main():
    filter = Zaak.create_filter()
    filter.filter_soort(ZaakSoort.WETGEVING, is_or=True)
    filter.filter_soort(ZaakSoort.INITIATIEF_WETGEVING, is_or=True)
    # TODO BR: enable when dossier toevoeging is possible
    # filter.filter_soort('Begroting', is_or=True)
    zaken = api.get_zaken(filter=filter)
    dossier_nrs = set()
    for zaak in zaken:
        dossier_nr = str(zaak.dossier.vetnummer)
        if zaak.dossier.toevoeging:
            dossier_nr += '-' + str(zaak.dossier.toevoeging)
            # TODO BR: for now we cannot handle these
            continue
        print(dossier_nr)
        dossier_nrs.add(dossier_nr)

    dossier_nrs = OrderedSet(sorted(dossier_nrs))
    print(dossier_nrs)
    for dossier_nr in dossier_nrs:
        print(dossier_nr)
    print(len(dossier_nrs))

    with open(os.path.join(out_dir, 'wetsvoorstellen_dossier_ids' + '.txt'), 'w') as fileout:
        for dossier_nr in dossier_nrs:
            fileout.write(str(dossier_nr) + '\n')
    print('END')


if '__main__' == __name__:
    main()
