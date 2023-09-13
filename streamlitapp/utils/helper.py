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

        files = os.listdir('.//resultLogs/' + config_id)

        for index, filename in enumerate(files):
            files[index] = filename.replace('.json', '')

        return files

    except:

        return None


def get_result_data(config_id, execution_id):
    metric_data = {}

    for execution in execution_id:
        result_file = open('./resultlogs/' + config_id + '/' + execution + '.json')

        try:

            result_json = json.load(result_file)

            metric_data[execution] = {"95th percentile response time in ms": round(
                result_json["metrics"]["RequestEndpointResponseTime"]["values"]["p(95)"], 2)}
            metric_data[execution]["Average response time in ms"] = round(
                result_json["metrics"]["RequestEndpointResponseTime"]["values"]["avg"], 2)
            metric_data[execution]["Request timeout Rate in Percentage"] = \
                result_json["metrics"]["RequestEndpointRequestTimeoutRate"]["values"]["rate"] * 100
            metric_data[execution]["Pass Rate in Percentage"] = \
                result_json["metrics"]["RequestEndpointPassRate"]["values"]["rate"] * 100
            metric_data[execution]["Duration in min"] = result_json['TestSummary']['testData']['duration']
            metric_data[execution]["Concurrent Users"] = result_json["TestSummary"]["testData"]["vus"]

        except:

            metric_data[execution] = {}

    return metric_data


def get_results(config_id, execution_id):
    metric_data = {}

    result_file = open('./resultlogs/' + config_id + '/' + execution_id + '.json')
    try:
        result_json = json.load(result_file)
        metric_data["95th percentile response time in ms"] = round(result_json["metrics"]["RequestEndpointResponseTime"]["values"]["p(95)"], 2)
        metric_data["Average response time in ms"] = round(result_json["metrics"]["RequestEndpointResponseTime"]["values"]["avg"], 2)
        metric_data["Request timeout Rate in Percentage"] = result_json["metrics"]["RequestEndpointRequestTimeoutRate"]["values"]["rate"] * 100
        metric_data["Pass Rate in Percentage"] = result_json["metrics"]["RequestEndpointPassRate"]["values"]["rate"] * 100
        metric_data["Duration in min"] = result_json['TestSummary']['testData']['duration']
        metric_data["Concurrent Users"] = result_json["TestSummary"]["testData"]["vus"]
    except:
        metric_data[execution_id] = {}

    return metric_data


def update_config(config_id, config_details):
    config_dct = {
        config_id: config_details
    }
    config_file = open('.\\data\\config.json')

    config_json = json.load(config_file)
    config_json.update(config_dct)

    with open(".\\data\\config.json", "w") as jsonfile:
        json.dump(config_json, jsonfile)


def save_config(config_id, host, api_endpoint, operation, is_local_host, payload, payload_type, payload_as_string,
                auth_type, dsn, user_name, password, token, duration, vus):
    config_details = {
        "hostname": host,
        "endpoint": api_endpoint,
        "method": operation,
        "isLocalhost": is_local_host,
        "payload": payload,
        "payloadType": payload_type,
        "payloadAsString": payload_as_string,
        "auth": auth_type,
        "dsn": dsn,
        "username": user_name,
        "password": password,
        "token": token,
        "duration": duration,
        "vus": vus

    }
    update_config(config_id, config_details)


def validate_json(json_data):
    try:
        json.loads(json_data)
    except ValueError as err:
        return False
    return True


def delete_result(config_id, execid):
    flag = os.remove('./resultlogs/' + config_id + '/' + execid + '.json')

    return flag
