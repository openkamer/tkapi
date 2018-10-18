import json
import datetime


def print_pretty(json_in):
    pretty_json = json.dumps(json_in, indent=4, sort_keys=True, ensure_ascii=False)
    print(pretty_json)


def datetime_to_odata(datetime_obj):
    return "datetime'" + datetime_obj.strftime('%Y-%m-%dT%H:%M:%S') + "'"


def odatedatetime_to_datetime(odate_datetime):
    return datetime.datetime.strptime(odate_datetime, '%Y-%m-%dT%H:%M:%S')


def create_api():
    try:
        from local_settings import USER, PASSWORD, API_ROOT_URL
        from .api import Api
        return Api(user=USER, password=PASSWORD, api_root=API_ROOT_URL, verbose=False)
    except ModuleNotFoundError as error:
        print("util.create_api(): No 'local_settings.py' found with USER and PASSWORD.")
        raise error
