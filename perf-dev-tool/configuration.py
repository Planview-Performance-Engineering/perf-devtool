import streamlit as st
from utils import helper
from streamlit_modal import Modal

op_lst = ["GET", "POST", "PUT"]
auth_lst = ["Basic", "Bearer"]
menu_lst = ["Config", "Execution", "Results"]



def add_config_details(config_ids_list, default_config_index, selected_menu):

    m = st.markdown("""
    <style>
    div.stButton > button:first-child {
    background-color: #8fbc8f;
    color:#ffffff;
    }
    div.stButton > button:hover {
    background-color: #8fbc8f;
    color:#ff0000;
    }
    </style>""", unsafe_allow_html=True)
    payload = None
    payload_type = None
    payload_as_string = None
    dsn = ""
    user_name = ""
    password = ""
    token = ""

    config_id = st.selectbox(":blue[Select Config Name]", config_ids_list,
                             index=default_config_index, key="config_ids_list")

    st.session_state.config_id_selected = config_id

    st.experimental_set_query_params(config_id=config_id, menu=selected_menu)

    config_details = helper.get_config_details(config_id)
    left, right = st.columns(2)

    is_local_host = right.checkbox(":blue[Are you running on local host]", value=config_details["isLocalhost"])

    if is_local_host:

        host = left.text_input(":blue[Host URL]", value="http://host.docker.internal", placeholder="Enter host url", disabled=True)

    else:

        host = left.text_input(":blue[Host URL]", value=config_details["hostname"], placeholder="Enter host url")

    api_endpoint = left.text_input(":blue[Request End Point]", value=config_details['endpoint'],
                                   placeholder="Enter end point with query parameters")
    left.caption("Example: /planview/getAttributes")

    operation = right.selectbox(":blue[Select Operation]", op_lst,
                                index=op_lst.index(config_details['method']), key="select_operation")
    request_headers = left.text_area(":blue[Request Headers]",
                                     value=config_details["requestHeaders"] if config_details["requestHeaders"] else {},
                                     height=5)

    if request_headers:
        status = helper.validate_json(request_headers)
        if not status:
            st.error("Please provide valid JSON")

    if operation == "POST":
        payload = left.text_area(":blue[Request Payload]",
                                 value=config_details["payload"] if config_details["payload"] else {}, height=10)

        if payload:
            status = helper.validate_json(payload)
            if not status:
                st.error("Please provide valid JSON")
        payload_type = right.selectbox(":blue[Payload Type]",
                                       ("application/json", "application/x-www-form-urlencoded",
                                        "text/xml;charset=utf-8"))

        payload_as_string = right.checkbox(":blue[Payload as Sting]", value=config_details["payloadAsString"])

    auth_type = right.selectbox(":blue[Authorization]", auth_lst, index=auth_lst.index(config_details['auth']))

    if auth_type == "Basic":
        right.caption("Used for Portfolio service request. Use Portfolio dsn,username and password here")
        dsn = right.text_input(":blue[DSN]", placeholder="Enter DSN Name", value=config_details["dsn"])
        user_name = right.text_input(":blue[User Name]", placeholder="Enter User Name",
                                     value=config_details["username"])
        password = right.text_input(":blue[Password]", placeholder="Enter Password", value=config_details["password"])
    elif auth_type == "Bearer":
        token = right.text_input(":blue[Token]", placeholder="Enter token", value=config_details["token"])

    new_config_id = left.text_input(":blue[Config Name]", placeholder="Enter unique Name to save config details",
                                    value=config_id)
    left.caption("Provide unique config name for the test configuration")

    help_text = "Test runs multiple iterations in parallel with virtual users (VUs). " \
                "In general terms, more virtual users means more simulated traffic"
    duration = left.text_input(":blue[Duration in minutes]", placeholder="Enter duration in minutes",
                               value=config_details["duration"])
    vus = right.text_input(":blue[No of Concurrent Users]", placeholder="Enter duration in minutes",
                           value=config_details["vus"], help=help_text)

    def save_config():

        helper.save_config(new_config_id, host, api_endpoint, operation, is_local_host,
                           payload, request_headers, payload_type, payload_as_string, auth_type, dsn, user_name,
                           password, token, duration, vus)
        
    def display_popup(text):
        model = Modal(key="results-key",title=text)
        with model.container():
            #st.write(text)
            if st.button("OK"):
                st.experimental_rerun()


    button1_css = """
    <style>
    #custom-button-1>button {
        background-color: #17e84f;
        color: white;
        border-color: #17e84f;
    }
    </style>
    """

    button2_css = """
    <style>
    #custom-button-2>button {
        background-color: #e81717;
        color: white;
        border-color: #e81717;
    }
    </style>
    """

    button3_css = """
    <style>
     #custom-button-3>button {
         background-color: #17e84f;
         color: white;
         border-color: #17e84f;
     }
     </style>
     """
    left_column, center_column, right_column = st.columns([0.1, 0.1, 0.5])

    left_column.markdown(button1_css, unsafe_allow_html=True)
    right_column.markdown(button2_css, unsafe_allow_html=True)
    center_column.markdown(button3_css, unsafe_allow_html=True)

    if left_column.button("Save", key="custom-button-1"):
        if new_config_id in config_ids_list:
            st.error(f"Config with {new_config_id} can be updated with only new auth credentails. Save with new config name for updating other details.")
        else:
            save_config()
            st.experimental_set_query_params(config_id=new_config_id, menu=selected_menu)
            display_popup(f"Saved as new config {new_config_id}")
            #st.experimental_rerun()

    placeholder = right_column.empty()

    st.session_state.disabled = True

    if token != config_details['token'] or dsn != config_details['dsn'] or \
            user_name != config_details['username'] or password != config_details['password']:
        st.session_state.disabled = False

    update_button = placeholder.button('Update', disabled=st.session_state.get('disabled'), key='custom-button-2')

    if update_button:
        config_details['token'] = token
        config_details['dsn'] = dsn
        config_details['username'] = user_name
        config_details['password'] = password
        config_details['duration'] = duration
        config_details['vus'] = vus
        placeholder.button('Update', disabled=True)

        helper.update_config(config_id, config_details)
        st.success("Auth credentials are updated")

    if center_column.button("Delete", key="custom-button-3"):

        if config_id == 'default':
            st.error("Default config can't be deleted")
        else:
            helper.delete_config_details(config_id)
            config_ids_list = helper.get_config_ids_lst()
            st.experimental_set_query_params(config_id='default', menu=selected_menu)
            display_popup(f"Config {config_id} deleted")

            #st.experimental_rerun()
