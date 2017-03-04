import json


def print_pretty(json_in):
    pretty_json = json.dumps(json_in, indent=4, sort_keys=True, ensure_ascii=False).encode('utf8')
    print(pretty_json)


def datetime_to_odata(datetime_obj):
    return "datetime'" + datetime_obj.strftime('%Y-%m-%dT%H:%M:%S') + "'"