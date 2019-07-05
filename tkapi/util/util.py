import json
import datetime
from dateutil import parser


def print_pretty(json_in):
    pretty_json = json.dumps(json_in, indent=4, sort_keys=True, ensure_ascii=False)
    print(pretty_json)


def datetime_to_odata(datetime_obj):
    return datetime_obj.strftime('%Y-%m-%dT%H:%M:%SZ')


def odatedatetime_to_datetime(odate_datetime):
    return parser.parse(odate_datetime)


def odatedate_to_date(odate_date):
    return datetime.datetime.strptime(odate_date, '%Y-%m-%d')


def odateyear_to_date(odate_date):
    return datetime.datetime.strptime(odate_date, '%Y')


def create_api(verbose=False):
    from tkapi.api import Api
    return Api(verbose=verbose)

