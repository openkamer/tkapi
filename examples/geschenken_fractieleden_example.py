from tkapi.util import queries


def example_geschenken_fractieleden_actief():
    leden_actief = queries.get_fractieleden_actief()
    for lid in leden_actief:
        persoon = lid.persoon
        print('{} ({})'.format(persoon, lid.fractie.afkorting))
        for geschenk in lid.persoon.geschenken:
            print('\t', geschenk.omschrijving)


if '__main__' == __name__:
    example_geschenken_fractieleden_actief()
