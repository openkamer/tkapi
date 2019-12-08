import requests

from tkapi.document import Document
from tkapi.document import DocumentSoort


def get_overheidnl_id(document: Document) -> str or None:
    if document.soort == DocumentSoort.SCHRIFTELIJKE_VRAGEN:
        return get_kamervraag_overheidnl_id(document)
    if document.soort in [DocumentSoort.ANTWOORD_SCHRIFTELIJKE_VRAGEN, DocumentSoort.MEDEDELING_UITSTEL_ANTWOORD]:
        return get_kamerantwoord_overheidnl_id(document)
    return None


def get_overheidnl_url(document: Document):
    overheidnl_id = get_overheidnl_id(document)
    if not overheidnl_id:
        return None
    return get_overheidnl_url_for_id(overheidnl_id)


def get_overheidnl_url_for_id(overheidnl_id: str):
    if not overheidnl_id:
        return None
    return 'https://zoek.officielebekendmakingen.nl/{}'.format(overheidnl_id)


def get_kamervraag_overheidnl_id(document: Document) -> str or None:
    assert document.soort == DocumentSoort.SCHRIFTELIJKE_VRAGEN
    overheidnl_id = None
    # kamervragen have two url types at officielebekendmakingen, one starting with 'kv-tk' an old ones with 'kv-'
    # TODO: determine date at which this format is switched to reduce the number of requests
    for zaak in document.zaken:
        overheidnl_id = 'kv-tk-{}'.format(zaak.nummer)
        url = get_overheidnl_url_for_id(overheidnl_id)
        response = requests.get(url, timeout=60)
        if response.status_code == 404 or 'Errors/404.htm' in response.url and zaak.alias:
            overheidnl_id = 'kv-{}'.format(zaak.alias)
            url = get_overheidnl_url_for_id(overheidnl_id)
            response = requests.get(url, timeout=60)
        if response.status_code == 404 or 'Errors/404.htm' in response.url:
            overheidnl_id = None
    return overheidnl_id


def get_kamerantwoord_overheidnl_id(document: Document) -> str or None:
    assert document.soort in [DocumentSoort.ANTWOORD_SCHRIFTELIJKE_VRAGEN, DocumentSoort.MEDEDELING_UITSTEL_ANTWOORD]
    if not document.vergaderjaar or not document.aanhangselnummer:
        return None
    url_id = document.vergaderjaar.replace('-', '') + '-' + document.aanhangselnummer[-4:].lstrip('0')  # 20162017-11
    overheidnl_id = 'ah-tk-{}'.format(url_id)
    url = get_overheidnl_url_for_id(overheidnl_id)
    response = requests.get(url, timeout=60)
    if response.status_code == 404 or 'Errors/404.htm' in response.url:
        url = None
    return overheidnl_id
