from tkapi import Api


def get_commissie_namen():
    commissies = Api().get_commissies()
    namen = []
    for commissie in commissies:
        if commissie.naam:
            namen.append(commissie.naam)
    return sorted(set(namen))


def get_soorten(items):
    soorten = []
    for item in items:
        if item.soort:
            soorten.append(item.soort)
    return sorted(set(soorten))


def get_commissie_soorten():
    commissies = Api().get_commissies()
    return get_soorten(commissies)


def get_verslag_soorten():
    verslagen = Api().get_verslagen()
    return get_soorten(verslagen)


def get_vergadering_soorten():
    verslagen = Api().get_vergaderingen()
    return get_soorten(verslagen)
