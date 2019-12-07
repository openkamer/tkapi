from collections import defaultdict
import json

import tkapi
from tkapi.util import queries
from tkapi.persoon import PersoonNevenfunctie


def example_kamerleden_nevenfuncties():
    print('BEGIN')
    kamerleden = queries.get_kamerleden_active()
    kamerleden_ids = [lid.id for lid in kamerleden]

    print('{} kamerleden found'.format(kamerleden))

    # we need to request in batches because filter params have a size limit
    batch_size = 25
    chunks = (len(kamerleden_ids) - 1) // batch_size + 1
    nevenfuncties = []
    for i in range(chunks):
        batch = kamerleden_ids[i * batch_size:(i + 1) * batch_size]
        filter = PersoonNevenfunctie.create_filter()
        filter.filter_ids(batch)
        nevenfuncties += tkapi.Api.get_items(tkitem=PersoonNevenfunctie, filter=filter)

    functies = defaultdict(list)
    for functie in nevenfuncties:
        functies[functie.persoon.achternaam].append(functie.omschrijving)

    print(json.dumps(functies, indent=4, sort_keys=True, ensure_ascii=False))
    print('END')


if '__main__' == __name__:
    example_kamerleden_nevenfuncties()
