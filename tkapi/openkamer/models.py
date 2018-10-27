from tkapi.util import queries


class OKDossier(object):

    def __init__(self, vetnummer):
        self.vetnummer = vetnummer
        self.kamerstukdossier = None
        self.kamerstukken = None
        self.zaken = None
        self.besluiten = None
        self.besluiten_with_stemmingen = None
        self.activiteiten = None

    def load(self):
        self.kamerstukdossier = self.load_kamerstukdossier()
        self.kamerstukken = self.kamerstukdossier.kamerstukken
        self.zaken = self.kamerstukdossier.zaken
        self.besluiten = self.load_besluiten()
        self.besluiten_with_stemmingen = self.load_besluiten_with_stemmingen()
        self.activiteiten = self.load_activiteiten()

    def load_kamerstukdossier(self):
        return queries.get_dossier(vetnummer=self.vetnummer)

    def load_besluiten(self):
        return queries.get_dossier_besluiten(vetnummer=self.vetnummer)

    def load_besluiten_with_stemmingen(self):
        return queries.get_dossier_besluiten_with_stemmingen(vetnummer=self.vetnummer)

    def load_activiteiten(self):
        return queries.get_dossier_activiteiten(vetnummer=self.vetnummer)

    def __str__(self):
        return 'OKDossier {} | kamerstukken ({}) | zaken ({}) | besluiten ({}) | besluiten with stemmingen ({})' \
            ' | activiteiten ({})'\
            .format(self.vetnummer, len(self.kamerstukken), len(self.zaken), len(self.besluiten),
                    len(self.besluiten_with_stemmingen), len(self.activiteiten))



