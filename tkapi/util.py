import json
import requests

from local_settings import USER, PASSWORD, API_ROOT_URL


def get_json(url):
    params = {
        '$format': 'json',
    }
    r = requests.get(API_ROOT_URL + url, params=params, auth=(USER, PASSWORD))
    # print(r.url)
    if r.status_code != 200:
        print(r.text)
    assert r.status_code == 200
    return r.json()


def print_pretty(json_in):
    pretty_json = json.dumps(json_in, indent=4, sort_keys=True, ensure_ascii=False).encode('utf8')
    print(pretty_json)


def datetime_to_odata(datetime_obj):
    return "datetime'" + datetime_obj.strftime('%Y-%m-%dT%H:%M:%S') + "'"