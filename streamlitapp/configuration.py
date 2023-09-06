import streamlit as st
from utils import helper

op_lst = ["GET", "POST"]
auth_lst = ["Basic", "Bearer"]
menu_lst = ["Config", "Execution", "Results"]


def add_config_details(default_config_index, selected_menu):
    payload = None
    payload_type = None
    dsn = ""
    user_name = ""
    password = ""
    token = ""
    config_ids_list = helper.get_config_ids_lst()

    config_id = st.selectbox("Select Config:", config_ids_list,
                             index=default_config_index, key="config_ids_list")

    st.session_state.config_id_selected = config_id

    st.experimental_set_query_params(config_id=config_id, menu=selected_menu)

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
        dsn = right.text_input("DSN:", placeholder="Enter DSN Name", value=config_details["dsn"])
        user_name = right.text_input("User Name:", placeholder="Enter User Name", value=config_details["username"])
        password = right.text_input("Password:", placeholder="Enter Password", value=config_details["password"])
    elif auth_type == "Bearer":
        token = right.text_input("Token:", placeholder="Enter token", value=config_details["token"])

    new_config_id = left.text_input("Config ID:", placeholder="Enter unique Name to save config details",
                                    value=config_id)

    left_column, right_column = st.columns(2)

    def save_config():
        helper.save_config(new_config_id, host, api_endpoint, operation,  is_local_host,
                           payload, payload_type, auth_type, dsn, user_name, password, token)

    if left_column.button('Save Config:'):
        if new_config_id in config_ids_list:
            st.error(f"Config ID {new_config_id} already exists please provide new id")
        else:
            save_config()

    if right_column.button('Update Config:'):
        save_config()


