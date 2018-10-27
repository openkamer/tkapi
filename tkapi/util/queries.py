import multiprocessing as mp

from tkapi import Api
from tkapi.fractie import Fractie
from tkapi.stemming import Stemming
from tkapi.dossier import Dossier
from tkapi.besluit import Besluit
from tkapi.activiteit import Activiteit


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


def get_kamerstuk_stemmingen(vetnummer, ondernummer):
    filter = Stemming.create_filter()
    filter.filter_kamerstuk(vetnummer=vetnummer, ondernummer=ondernummer)
    stemmingen = Api().get_stemmingen(filter=filter)
    stemmingen = do_load_stemmingen(stemmingen)
    return stemmingen


def get_dossier(vetnummer):
    filter = Dossier.create_filter()
    filter.filter_vetnummer(vetnummer)
    dossiers = Api().get_dossiers(filter=filter)
    dossier = dossiers[0]
    return dossier


def get_dossier_besluiten(vetnummer):
    filter = Besluit.create_filter()
    filter.filter_kamerstukdossier(vetnummer=vetnummer)
    return Api().get_besluiten(filter=filter)


def get_dossier_besluiten_with_stemmingen(vetnummer):
    filter = Besluit.create_filter()
    filter.filter_kamerstukdossier(vetnummer=vetnummer)
    filter.filter_non_empty(Stemming)
    return Api().get_besluiten(filter=filter)


def get_dossier_activiteiten(vetnummer):
    filter = Activiteit.create_filter()
    filter.filter_kamerstukdossier(vetnummer=vetnummer)
    return Api().get_activiteiten(filter=filter)
