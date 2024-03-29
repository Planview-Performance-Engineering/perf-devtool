import json
import os
import shutil

CONFIG__FILE_PATH = os.path.abspath((os.path.join(os.path.dirname(__file__), r'../data/configuration/config.json')))


def read_config():
    config_file = open(CONFIG__FILE_PATH)
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

        files = os.listdir('.//data/resultLogs/' + config_id)

        for index, filename in enumerate(files):
            files[index] = filename.replace('.json', '')

        return files

    except:

        return None


def get_result_data(config_id, execution_id):
    metric_data = {}

    for execution in execution_id:
        result_file = open('./data/resultlogs/' + config_id + '/' + execution + '.json')

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

    results_file_path = os.path.abspath(
        (os.path.join(os.path.dirname(__file__), fr'../data/resultLogs/{config_id}/{execution_id}.json')))

    # result_file = open('./resultlogs/' + config_id + '/' + execution_id + '.json')
    result_file = open(results_file_path)

    try:
        result_json = json.load(result_file)
        metric_data["95th percentile response time in ms"] = round(
            result_json["metrics"]["RequestEndpointResponseTime"]["values"]["p(95)"], 2)
        metric_data["Average response time in ms"] = round(
            result_json["metrics"]["RequestEndpointResponseTime"]["values"]["avg"], 2)
        metric_data["Maximum response time in ms"] = round(
            result_json["metrics"]["RequestEndpointResponseTime"]["values"]["max"], 2)
        metric_data["Minimum response time in ms"] = round(
            result_json["metrics"]["RequestEndpointResponseTime"]["values"]["min"], 2)
        metric_data["Request timeout Rate in Percentage"] = \
            result_json["metrics"]["RequestEndpointRequestTimeoutRate"]["values"]["rate"] * 100
        metric_data["Pass Rate in Percentage"] = result_json["metrics"]["RequestEndpointPassRate"]["values"][
                                                     "rate"] * 100
        metric_data["Duration in min"] = result_json['TestSummary']['testData']['duration']
        metric_data["Concurrent Users"] = result_json["TestSummary"]["testData"]["vus"]
        metric_data['Iterations'] = result_json['metrics']['iterations']['values']['count']
    except:
        pass
    return metric_data


def update_config(config_id, config_details):
    config_dct = {
        config_id: config_details
    }
    config_file = open(CONFIG__FILE_PATH)

    config_json = json.load(config_file)
    config_json.update(config_dct)

    with open(CONFIG__FILE_PATH, "w") as jsonfile:
        json.dump(config_json, jsonfile)


def save_config(config_id, config_details):
    config_id = config_id.replace(" ", "_")
    update_config(config_id, config_details)


def delete_config_details(config_id):
    config_file = read_config()
    config_file.pop(config_id)

    with open(CONFIG__FILE_PATH, "w") as jsonfile:
        json.dump(config_file, jsonfile)

    file_path_to_delete = os.path.abspath(
        (os.path.join(os.path.dirname(__file__), fr'../data/resultLogs/{config_id}')))
    shutil.rmtree(file_path_to_delete)


def validate_json(json_data):
    try:
        json.loads(json_data)
    except ValueError as err:
        return False
    return True


def delete_result(config_id, execution_id):
    file_path_to_delete = os.path.abspath(
        (os.path.join(os.path.dirname(__file__), fr'../data/resultLogs/{config_id}/{execution_id}.json')))
    flag = os.remove(file_path_to_delete)

    return flag



