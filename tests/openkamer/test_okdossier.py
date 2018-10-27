from tests.core import TKApiTestCase

from tkapi.openkamer.models import OKDossier


class TestOKDossier(TKApiTestCase):

    def test_load_dossier(self):
        vetnummer = 33885
        dossier = OKDossier(vetnummer=vetnummer)
        dossier.load()
        print(dossier)

        # print('Zaken')
        # for zaak in dossier.zaken:
        #     print('\t', zaak.soort, '|', zaak.onderwerp)
        #
        # print('Activiteiten')
        # for activiteit in dossier.activiteiten:
        #     print('\t', activiteit.soort, '|', activiteit.onderwerp, '|')
        #
        # print('Besluiten')
        # for besluit in dossier.besluiten:
        #     print('\t', besluit.soort, '|', besluit.slottekst)
        #     for zaak in besluit.zaken:
        #         print(zaak.soort, '|', zaak.onderwerp)

        print('Kamerstukken')
        for kamerstuk in dossier.kamerstukken:
            print('\t', kamerstuk.ondernummer, '|', kamerstuk.parlementair_document.soort, '|', kamerstuk.parlementair_document.datum)
            for zaak in kamerstuk.parlementair_document.zaken:
                print('\t\t', zaak.soort, '|', zaak.onderwerp, '|')
                for agendapunt in zaak.agendapunten:
                    print('\t\t\t', agendapunt.activiteit.soort, '|', agendapunt.activiteit.onderwerp, '|', agendapunt.besluit.slottekst)

        # for besluit in dossier.besluiten_with_stemmingen:
        #     print(besluit.slottekst)
        #     for stemming in besluit.stemmingen:
        #         print(stemming.fractie, stemming.fractie_size, stemming.soort)
