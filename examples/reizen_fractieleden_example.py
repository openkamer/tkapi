from tkapi.util import queries


def example_reizen_fractieleden_actief():
    leden_actief = queries.get_fractieleden_actief()
    for lid in leden_actief:
        persoon = lid.persoon
        print('{} ({})'.format(persoon, lid.fractie.afkorting))
        for reis in lid.persoon.reizen:
            print('\t', reis.bestemming, '|', reis.doel, '|', reis.van)


if '__main__' == __name__:
    example_reizen_fractieleden_actief()
