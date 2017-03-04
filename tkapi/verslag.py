from tkapi.util import get_json


def get_verslag(id):
    url = "Verslag(guid'" + id + "')"
    return get_json(url)


def get_verslag_handeling():
    url = "VerslagHandeling"
    return get_json(url)
