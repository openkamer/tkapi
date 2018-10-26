from tkapi import Api
from tkapi.actor import Fractie


def get_fractieleden_actief():
    filter = Fractie.create_filter()
    filter.filter_actief()
    fracties_actief = Api().get_fracties(filter=filter)
    leden_actief = []
    for fractie in fracties_actief:
        leden_actief += fractie.leden_actief
    return leden_actief
