import tkapi
from tkapi.util import queries


api = tkapi.Api()


def example_kamerleden_actief():
    """Example that shows how to get all active kamerleden."""
    print('BEGIN')
    persons = queries.get_kamerleden_active()
    for person in persons:
        print(person)
    print('END: {} kamerleden gevonden'.format(len(persons)))


if '__main__' == __name__:
    example_kamerleden_actief()
