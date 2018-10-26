import tkapi
from tkapi.fractie import Fractie

from local_settings import USER, PASSWORD

api = tkapi.Api(user=USER, password=PASSWORD, verbose=False)


def example_fracties_leden_actief():
    """Example that shows how to get all active fracties and their active members."""
    filter = Fractie.create_filter()
    filter.filter_actief()
    fracties_actief = api.get_fracties(filter=filter)
    for fractie in fracties_actief:
        print('{} ({}) ({} zetels)'.format(fractie.naam, fractie.afkorting, fractie.zetels))
        leden = fractie.leden_actief
        for lid in leden:
            print('  ', lid.persoon, lid.van)


if '__main__' == __name__:
    example_fracties_leden_actief()
