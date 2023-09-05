import streamlit as st
import subprocess
import re
from utils import helper


def get_run_params(default_config_index, selected_menu):
    config_ids_list = helper.get_config_ids_lst()

    session_state_config_id = st.session_state.config_id_selected if 'config_id_selected' in st.session_state else None
    selected_config_id = config_ids_list.index(session_state_config_id) if session_state_config_id else None

    if selected_config_id:
        default_value_index = selected_config_id
    elif default_config_index:
        default_value_index = default_config_index
    else:
        default_value_index = 0
    with st.form(key='my_form'):
        config_id = st.selectbox("Select Config:", config_ids_list, index=default_value_index,
                                 key="config_iconfig_ids_listds_list")

        st.experimental_set_query_params(config_id=config_id, menu=selected_menu)

        duration = st.text_input("Duration:", placeholder="Enter test duration")

        no_vus = st.text_input("VUS", placeholder="Enter virtual users")
        submit = st.form_submit_button("Run")

        if submit:
            st.text("Running Test...")
            run_subprocess(config_id, duration, no_vus)
            st.text("Test completed.")


def run_subprocess(config_id, duration, vus):
    config_details = helper.get_config_details(config_id)
    host = config_details['hostname']
    endpoint = config_details['endpoint']
    method = config_details['method']
    payload = config_details['payload']
    auth_type = config_details['auth']
    dsn = config_details['dsn']
    username = config_details['username']
    password = config_details['password']
    token = config_details['token']
    command = None
    if auth_type == "Bearer" and method == "GET":
        command = f'k6 run .\\testGetAPI.js  -e host={host} -e endpoint={endpoint} -e token={token} ' \
                  f'--duration={duration}m --vus={vus}'
    elif auth_type == "" and method == "POST":
        command = f'k6 run .\\testPostAPI.js  -e host={host} -e endpoint={endpoint} -e token={token}' \
                  f' -e payload={payload} --duration={duration}m --vus={vus}'
    if auth_type == "Bearer" and method == "GET":
        pass
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=True,
    )

    for line in process.stdout:
        # Parse the output to determine progress
        progress_match = re.search(r'Progress: (\d+)%', line)
        if progress_match:
            progress = int(progress_match.group(1))
            st.progress(progress / 100)  # Update the progress bar
        else:
            st.text(line)  # Display other output in the Streamlit interface

    process.wait()