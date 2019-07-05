import multiprocessing as mp
from typing import List

from tkapi import Api
from tkapi.agendapunt import Agendapunt
from tkapi.activiteit import Activiteit
from tkapi.document import Document
from tkapi.fractie import Fractie
from tkapi.stemming import Stemming
from tkapi.dossier import Dossier
from tkapi.besluit import Besluit
from tkapi.zaak import Zaak


def filter_duplicates(items):
    # NOTE: this must be a python default function
    items_ids = set()
    items_unique = []
    for item in items:
        if item.id not in items_ids:
            items_unique.append(item)
            items_ids.add(item.id)
    return items_unique


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


def get_dossier_zaken(nummer) -> List[Zaak]:
    zaak_filter = Zaak.create_filter()
    zaak_filter.filter_kamerstukdossier(nummer=nummer)
    return Api().get_zaken(filter=zaak_filter)


def get_dossier_documenten(nummer) -> List[Document]:
    document_filter = Document.create_filter()
    document_filter.filter_dossier(nummer)
    return Api().get_documenten(document_filter)


def get_dossier_documenten_with_activiteit(nummer) -> List[Document]:
    document_filter = Document.create_filter()
    document_filter.filter_dossier(nummer)
    document_filter.filter_has_activiteit()
    return Api().get_documenten(document_filter)


def get_kamerstuk_zaken(nummer, volgnummer) -> List[Zaak]:
    zaak_filter = Zaak.create_filter()
    zaak_filter.filter_kamerstukdossier(nummer)
    zaak_filter.filter_document(volgnummer)
    return Api().get_zaken(zaak_filter)


def get_dossier_besluiten(nummer) -> List[Besluit]:
    zaken = get_dossier_zaken(nummer)
    besluiten = []
    for zaak in zaken:
        besluiten += zaak.besluiten
    return filter_duplicates(besluiten)


def get_dossier_besluiten_with_stemmingen(nummer) -> List[Besluit]:
    zaken = get_dossier_zaken(nummer)
    besluiten = []
    for zaak in zaken:
        filter = Besluit.create_filter()
        filter.filter_zaak(zaak.nummer)
        filter.filter_non_empty(Stemming)
        besluiten += Api().get_besluiten(filter=filter)
    return filter_duplicates(besluiten)


def get_kamerstuk_besluiten(nummer, volgnummer) -> List[Besluit]:
    zaken = get_kamerstuk_zaken(nummer, volgnummer)
    besluiten = []
    for zaak in zaken:
        besluiten += zaak.besluiten
    return filter_duplicates(besluiten)


def get_dossier_zaken_with_activiteit(nummer) -> List[Zaak]:
    zaak_filter = Zaak.create_filter()
    zaak_filter.filter_has_activiteit()
    zaak_filter.filter_kamerstukdossier(nummer=nummer)
    return Api().get_zaken(filter=zaak_filter)


def get_dossier_zaken_with_agendapunt(nummer) -> List[Zaak]:
    zaak_filter = Zaak.create_filter()
    zaak_filter.filter_has_agendapunt()
    zaak_filter.filter_kamerstukdossier(nummer=nummer)
    return Api().get_zaken(filter=zaak_filter)


def get_kamerstuk_activiteiten(nummer, volgnummer, include_agendapunten=False) -> List[Activiteit]:
    zaken = get_kamerstuk_zaken(nummer, volgnummer)
    activiteiten = get_zaken_activiteiten(zaken)
    documenten = get_dossier_documenten_with_activiteit(nummer)
    for document in documenten:
        activiteiten += document.activiteiten
    if include_agendapunten:
        activiteiten += get_zaken_agendapunten_activiteiten(zaken)
    return filter_duplicates(activiteiten)


def get_dossier_activiteiten(nummer, include_agendapunten=False) -> List[Activiteit]:
    zaken = get_dossier_zaken_with_activiteit(nummer)
    activiteiten = get_zaken_activiteiten(zaken)
    documenten = get_dossier_documenten_with_activiteit(nummer)
    for document in documenten:
        activiteiten += document.activiteiten
    if include_agendapunten:
        zaken_dossier = get_dossier_zaken(nummer)
        activiteiten += get_zaken_agendapunten_activiteiten(zaken_dossier)
    return filter_duplicates(activiteiten)


def get_zaken_activiteiten(zaken) -> List[Activiteit]:
    activiteiten = []
    for zaak in zaken:
        for activiteit in zaak.activiteiten:
            activiteiten.append(activiteit)
    return filter_duplicates(activiteiten)


def get_zaken_agendapunten(zaken) -> List[Agendapunt]:
    agendapunten = []
    for zaak in zaken:
        for agendapunt in zaak.agendapunten:
            agendapunten.append(agendapunt)
    return filter_duplicates(agendapunten)


# TODO BR: improve performance, this is slow
def get_zaken_agendapunten_activiteiten(zaken) -> List[Activiteit]:
    activiteiten = []
    agendapunten = get_zaken_agendapunten(zaken)
    for agendapunt in agendapunten:
        if agendapunt.activiteit:
            activiteiten.append(agendapunt.activiteit)
    return activiteiten


def get_kamerstuk_stemmingen(nummer, volgnummer) -> List[Stemming]:
    besluiten = get_kamerstuk_besluiten(nummer, volgnummer)
    stemmingen = []
    for besluit in besluiten:
        stemmingen += besluit.stemmingen
    return filter_duplicates(stemmingen)
