from tkapi import Api
from orderedset import OrderedSet


def get_commissie_namen():
    commissies = Api().get_commissies()
    namen = []
    for commissie in commissies:
        if commissie.naam:
            namen.append(commissie.naam)
    return OrderedSet(sorted(namen))


def get_commissie_soorten():
    commissies = Api().get_commissies()
    soorten = []
    for commissie in commissies:
        if commissie.soort:
            soorten.append(commissie.soort)
    return OrderedSet(sorted(soorten))
