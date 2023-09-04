import streamlit as st
import json

from utils import helper


def add_config_details():
    payload = None
    payload_type = None
    op_lst = ["GET", "POST"]
    auth_lst = ["Basic", "Bearer"]

    st.set_page_config(page_title="PerfDevTool", page_icon=None)
    config_ids_list = helper.get_config_ids_lst()

    query_params = st.experimental_get_query_params()
    default = query_params["config_id"][0] if "config_id" in query_params else None
    default_index = config_ids_list.index(default) if default else 0

    config_id = st.selectbox("Select Config:", config_ids_list,
                             index=default_index, key="config_ids_list")

    st.session_state.config_id_selected = config_id

    st.experimental_set_query_params(config_id=config_id)

    config_details = helper.get_config_details(config_id)
    left, right = st.columns(2)

    host = left.text_input("Host URL:", value=config_details["hostname"], placeholder="Enter host url")
    is_local_host = right.checkbox("Are you running on local host", value=config_details["isLocalhost"])
    api_endpoint = left.text_input("API End Point:", value=config_details['endpoint'],
                                   placeholder="Enter end point with query parameters")
    operation = right.selectbox("Select Operation:", op_lst,
                                index=op_lst.index(config_details['method']), key="select_operation")
    if operation == "POST":
        payload = left.text_area("Request Payload", value=config_details["payload"])
        if payload:
            status = helper.validate_json(payload)
            if not status:
                st.error("Please provide valid JSON")
        payload_type = right.selectbox("Payload Type",
                                       ("application/json", "application/x-www-form-urlencoded"))

    auth_type = right.selectbox("Authorization:", auth_lst, index=auth_lst.index(config_details['auth']))

    if auth_type == "Basic":
        right.text_input("DSN:", placeholder="Enter DSN Name")
        right.text_input("User Name:", placeholder="Enter User Name")
        right.text_input("Password:", placeholder="Enter Password")
    elif auth_type == "Bearer":
        right.text_input("Token:", placeholder="Bearer <token>")

    new_config_id = left.text_input("Config ID:", placeholder="Enter unique Name to save config details")

    if new_config_id:
        save_config(new_config_id, host, api_endpoint, operation, is_local_host, payload, payload_type, auth_type)

    if new_config_id and new_config_id in config_ids_list:
        st.error(f"Config ID {new_config_id} already exists please provide new id")


def save_config(config_id, host, api_endpoint, operation, is_local_host, payload, payload_type, auth_type):

    config_dct = {
        config_id: {
            "hostname": host,
            "endpoint": api_endpoint,
            "method": operation,
            "isLocalhost": is_local_host,
            "payload": payload,
            "payloadType": payload_type,
            "auth": auth_type
        }
    }
    config_file = open('.\\data\\config.json')

    config_json = json.load(config_file)
    config_json.update(config_dct)
    print('+++++++++++++++++++', config_json, config_dct)

    with open(".\\data\\config.json", "w") as jsonfile:
        json.dump(config_json, jsonfile)


add_config_details()
