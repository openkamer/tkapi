import tkapi
from tkapi.util import queries

api = tkapi.Api(verbose=False)


def example_geschenken_fractieleden_actief():
    leden_actief = queries.get_fractieleden_actief()
    for lid in leden_actief:
        persoon = lid.persoon
        print('{} ({})'.format(persoon, lid.fractie.afkorting))
        geschenken = lid.persoon.geschenken
        for geschenk in geschenken:
            print('\t', geschenk.omschrijving)


if '__main__' == __name__:
    example_geschenken_fractieleden_actief()
