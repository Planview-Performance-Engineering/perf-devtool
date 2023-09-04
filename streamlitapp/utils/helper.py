import json


def read_config():
    config_file = open('.\\data\\config.json')
    config_json = json.load(config_file)
    return config_json


def get_config_ids_lst():
    config_json = read_config()
    config_ids_lst = list(config_json.keys())
    return config_ids_lst


def get_config_details(config_id):
    config_json = read_config()
    config_details = config_json[config_id]
    return config_details


def validate_json(json_data):
    try:
        json.loads(json_data)
    except ValueError as err:
        return False
    return True
