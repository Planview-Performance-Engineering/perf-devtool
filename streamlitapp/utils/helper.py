import json
import os

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

def get_execution_list(config_id):

    try:

        files = os.listdir('.//resultLogs/'+ config_id)
        return files

    except:

        return None

def get_result_data(config_id,execution_id):

    metric_data = {}

    for index in range(len(execution_id)):

        result_file = open('./resultlogs/'+config_id+'/'+execution_id[index])
        result_json = json.load(result_file)
        metric_data[execution_id[index]] = {"Percentile 95 response time in ms" : result_json["metrics"]["RequestEndpointResponseTime"]["values"]["p(95)"]}
        metric_data[execution_id[index]] ["Average response time in ms"] = result_json["metrics"]["RequestEndpointResponseTime"]["values"]["avg"]
        metric_data[execution_id[index]] ["Timeout Rate in Percentage"] = result_json["metrics"]["RequestEndpointRequestTimeoutRate"]["values"]["rate"]*100
        metric_data[execution_id[index]] ["Success Rate in Percentage"] = result_json["metrics"]["RequestEndpointPassRate"]["values"]["rate"]*100
        metric_data[execution_id[index]] ["Duration in min"] = result_json['TestSummary']['testData']['duration']
        metric_data[execution_id[index]] ["Virtual Users"] = result_json["TestSummary"]["testData"]["vus"]
    
    return metric_data


def save_config(config_id, host, api_endpoint, operation, is_local_host, payload, payload_type,
                auth_type, dsn, user_name, password, token, duration, vus):

    config_dct = {
        config_id: {
            "hostname": host,
            "endpoint": api_endpoint,
            "method": operation,
            "isLocalhost": is_local_host,
            "payload": payload,
            "payloadType": payload_type,
            "auth": auth_type,
            "dsn": dsn,
            "username": user_name,
            "password": password,
            "token": token,
            "duration": duration,
            "vus": vus

        }
    }
    config_file = open('.\\data\\config.json')

    config_json = json.load(config_file)
    config_json.update(config_dct)

    with open(".\\data\\config.json", "w") as jsonfile:
        json.dump(config_json, jsonfile)


def validate_json(json_data):
    try:
        json.loads(json_data)
    except ValueError as err:
        return False
    return True
