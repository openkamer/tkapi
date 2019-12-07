import requests

from tkapi.document import Document
from tkapi.document import DocumentSoort


def get_kamervraag_overheidnl_url(document: Document):
    assert document.soort == DocumentSoort.SCHRIFTELIJKE_VRAGEN
    url = ''
    # kamervragen have two url types at officielebekendmakingen, one starting with 'kv-tk' an old ones with 'kv-'
    # TODO: determine date at which this format is switched to reduce the number of requests
    for zaak in document.zaken:
        url = 'https://zoek.officielebekendmakingen.nl/kv-tk-' + zaak.nummer
        response = requests.get(url, timeout=60)
        if response.status_code != 200:
            print('ERROR {} getting url {}'.format(response.status_code, url))
        if response.status_code == 404 or 'Errors/404.htm' in response.url and zaak.alias:
            url = 'https://zoek.officielebekendmakingen.nl/kv-' + zaak.alias
            response = requests.get(url, timeout=60)
        if response.status_code == 404 or 'Errors/404.htm' in response.url:
            url = ''
    return url


def get_kamerantwoord_overheidnl_url(document: Document):
    assert document.soort == DocumentSoort.ANTWOORD_SCHRIFTELIJKE_VRAGEN
    if not document.vergaderjaar:
        print('document.vergaderjaar is empty, early return')
        return ''
    if not document.aanhangselnummer:
        print('document.aanhangselnummer is empty, early return')
        return ''
    url_id = document.vergaderjaar.replace('-', '') + '-' + document.aanhangselnummer[-4:].lstrip('0')  # 20162017-11
    url = 'https://zoek.officielebekendmakingen.nl/ah-tk-' + url_id
    response = requests.get(url, timeout=60)
    if response.status_code == 404 or 'Errors/404.htm' in response.url:
        url = ''
    return url
