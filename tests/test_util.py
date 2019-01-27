from tkapi.util import queries
from tkapi.besluit import Besluit
from tkapi.dossier import Dossier

from .core import TKApiTestCase


class TestUtilQueries(TKApiTestCase):
    pass

    # TODO BR: disabled because only 1 nested query allowed
    # def test_get_kamerstuk_stemmingen(self):
    #     nummer = 33885
    #     ondernummer = 16
    #     stemmingen = queries.get_kamerstuk_stemmingen(nummer=nummer, ondernummer=ondernummer)
    #     total_votes = 0
    #     for stemming in stemmingen:
    #         print(stemming.fractie.naam, stemming.fractie_size, stemming.soort, stemming.besluit.soort)
    #         total_votes += stemming.fractie_size
    #     print('total votes', total_votes)

    # TODO BR: disabled because kamerstukken are removed
    # def test_get_dossier_stemmingen(self):
    #     nummer = 33885
    #     dossier = queries.get_dossier(nummer=nummer)
    #     print('kamerstukken', len(dossier.kamerstukken))
    #     for kamerstuk in dossier.kamerstukken:
    #         print(kamerstuk.ondernummer, kamerstuk.document.onderwerp)
    #         stemmingen = queries.get_kamerstuk_stemmingen(nummer=nummer, ondernummer=kamerstuk.ondernummer)
    #         total_votes = 0
    #         for stemming in stemmingen:
    #             # print('\t', stemming.fractie.naam, stemming.fractie_size, stemming.soort, stemming.besluit.soort)
    #             total_votes += stemming.fractie_size
    #         print('total votes', total_votes)

    # TODO BR: disabled because only 1 nested query allowed
    # def test_get_dossier_besluiten(self):
    #     nummer = 33885
    #     besluiten = queries.get_dossier_besluiten_with_stemmingen(nummer=nummer)
    #     besluiten = besluiten[:5]
    #     for besluit in besluiten:
    #         if not besluit.stemmingen:
    #             continue
    #         print(besluit.zaken[0].onderwerp)
    #         stemmingen = queries.do_load_stemmingen(stemmingen=besluit.stemmingen)
    #         for stemming in stemmingen:
    #             print('\t', stemming.fractie.naam, stemming.fractie_size, stemming.soort, besluit.soort)
