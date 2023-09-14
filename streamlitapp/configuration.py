import streamlit as st
from utils import helper

op_lst = ["GET", "POST", "PUT"]
auth_lst = ["Basic", "Bearer"]
menu_lst = ["Config", "Execution", "Results"]


def add_config_details(config_ids_list, default_config_index, selected_menu):
    payload = None
    payload_type = None
    payload_as_string = None
    dsn = ""
    user_name = ""
    password = ""
    token = ""

    config_id = st.selectbox("Select Config:", config_ids_list,
                             index=default_config_index, key="config_ids_list")

    st.session_state.config_id_selected = config_id

    st.experimental_set_query_params(config_id=config_id, menu=selected_menu)

    config_details = helper.get_config_details(config_id)
    left, right = st.columns(2)

    is_local_host = right.checkbox("Are you running on local host", value=config_details["isLocalhost"])

    if is_local_host:

        host = left.text_input("Host URL:", value="http://localhost", placeholder="Enter host url", disabled=True)

    else:

        host = left.text_input("Host URL:", value=config_details["hostname"], placeholder="Enter host url")

    api_endpoint = left.text_input("API End Point:", value=config_details['endpoint'],
                                   placeholder="Enter end point with query parameters")
    left.caption("Example: /planview/getAttributes")

    operation = right.selectbox("Select Operation:", op_lst,
                                index=op_lst.index(config_details['method']), key="select_operation")
    if operation == "POST":
        payload = left.text_area("Request Payload", value=config_details["payload"])
        if payload:
            status = helper.validate_json(payload)
            if not status:
                st.error("Please provide valid JSON")
        payload_type = right.selectbox("Payload Type",
                                       ("application/json", "application/x-www-form-urlencoded",
                                        "text/xml;charset=utf-8"))
        payload_as_string = right.checkbox("Payload as String", value=config_details["payloadAsString"])

    auth_type = right.selectbox("Authorization:", auth_lst, index=auth_lst.index(config_details['auth']))

    if auth_type == "Basic":
        dsn = right.text_input("DSN:", placeholder="Enter DSN Name", value=config_details["dsn"])
        user_name = right.text_input("User Name:", placeholder="Enter User Name", value=config_details["username"])
        password = right.text_input("Password:", placeholder="Enter Password", value=config_details["password"])
    elif auth_type == "Bearer":
        token = right.text_input("Token:", placeholder="Enter token", value=config_details["token"])

    new_config_id = left.text_input("Config Name:", placeholder="Enter unique Name to save config details",
                                    value=config_id)

    left_column, right_column = st.columns(2)
    help_text = "Test runs multiple iterations in parallel with virtual users (VUs). " \
                "In general terms, more virtual users means more simulated traffic"
    duration = left.text_input("Duration in minutes :", placeholder="Enter duration in minutes",
                               value=config_details["duration"])
    vus = left.text_input("No of Concurrent Users :", placeholder="Enter duration in minutes",
                          value=config_details["vus"], help=help_text)

    def save_config():
        helper.save_config(new_config_id, host, api_endpoint, operation, is_local_host,
                           payload, payload_type, payload_as_string, auth_type, dsn, user_name, password, token,
                           duration, vus)

    if left_column.button('Save Config:'):
        if new_config_id in config_ids_list:
            st.error(f"Config with {new_config_id} name already exists please provide new id")
        else:
            save_config()

    placeholder = right_column.empty()

    st.session_state.disabled = True

    if token != config_details['token'] or dsn != config_details['dsn'] or user_name != config_details['username'] or \
            password != config_details['password'] or duration != config_details['duration'] or vus != config_details['vus']:
        st.session_state.disabled = False

    update_button = placeholder.button('Update Config:', disabled=st.session_state.get('disabled'), key=1)

    if update_button:
        config_details['token'] = token
        config_details['dsn'] = dsn
        config_details['username'] = user_name
        config_details['password'] = password
        config_details['duration'] = duration
        config_details['vus'] = vus
        placeholder.button('Update Config:', disabled=True, key=2)

        helper.update_config(config_id, config_details)
