import tkapi

from tkapi.util import queries

api = tkapi.Api(verbose=False)


def example_stemming():
    stemmingen = queries.get_kamerstuk_stemmingen(nummer=33885, volgnummer=16)
    print('stemmingen', len(stemmingen))
    total_votes = 0
    for stemming in stemmingen:
        print('\t', stemming.actor_naam, stemming.fractie_size, stemming.soort)
        total_votes += stemming.fractie_size
    print('totaal stemmen:', total_votes)


if '__main__' == __name__:
    example_stemming()
