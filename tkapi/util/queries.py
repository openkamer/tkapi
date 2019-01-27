import multiprocessing as mp

from tkapi import Api
from tkapi.fractie import Fractie
from tkapi.stemming import Stemming
from tkapi.dossier import Dossier
from tkapi.besluit import Besluit
from tkapi.activiteit import Activiteit
from tkapi.zaak import Zaak


def get_fractieleden_actief():
    filter = Fractie.create_filter()
    filter.filter_actief()
    fracties_actief = Api().get_fracties(filter=filter)
    leden_actief = []
    for fractie in fracties_actief:
        leden_actief += fractie.leden_actief
    return leden_actief


def load_stemmingen(stemming, stemmingen_loaded):
    stemming.fractie
    stemmingen_loaded.append(stemming)


def do_load_stemmingen(stemmingen):
    manager = mp.Manager()
    stemmingen_loaded = manager.list()
    processes = []
    for stemming in stemmingen:
        process = mp.Process(target=load_stemmingen, args=(stemming, stemmingen_loaded))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
    return stemmingen_loaded


def get_dossier(nummer):
    filter = Dossier.create_filter()
    filter.filter_nummer(nummer)
    dossiers = Api().get_dossiers(filter=filter)
    dossier = dossiers[0]
    return dossier


def get_dossier_zaken(nummer):
    zaak_filter = Zaak.create_filter()
    zaak_filter.filter_kamerstukdossier(nummer=nummer)
    return Api().get_zaken(filter=zaak_filter)


def get_kamerstuk_zaken(nummer, volgnummer):
    zaak_filter = Zaak.create_filter()
    zaak_filter.filter_kamerstukdossier(nummer)
    zaak_filter.filter_volgnummer(volgnummer)
    return Api().get_zaken(zaak_filter)


def get_dossier_besluiten(nummer):
    zaken = get_dossier_zaken(nummer)
    besluiten = []
    for zaak in zaken:
        besluiten += zaak.besluiten
    return besluiten


def get_dossier_besluiten_with_stemmingen(nummer):
    zaken = get_dossier_zaken(nummer)
    besluiten = []
    for zaak in zaken:
        filter = Besluit.create_filter()
        filter.filter_zaak(zaak.nummer)
        filter.filter_non_empty(Stemming)
        besluiten += Api().get_besluiten(filter=filter)
    return besluiten


def get_kamerstuk_besluiten(nummer, volgnummer):
    zaken = get_kamerstuk_zaken(nummer, volgnummer)
    besluiten = []
    for zaak in zaken:
        besluiten += zaak.besluiten
    return besluiten


def get_dossier_activiteiten(nummer):
    filter = Activiteit.create_filter()
    filter.filter_kamerstukdossier(nummer=nummer)
    return Api().get_activiteiten(filter=filter)
