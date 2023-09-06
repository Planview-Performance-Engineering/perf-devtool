import json

import streamlit as st
import subprocess
import re
from utils import helper


def get_run_params(config_ids_list, default_config_index, selected_menu):
    session_state_config_id = st.session_state.config_id_selected if 'config_id_selected' in st.session_state else None
    selected_config_id = config_ids_list.index(session_state_config_id) if session_state_config_id else None

    if selected_config_id:
        default_value_index = selected_config_id
    elif default_config_index:
        default_value_index = default_config_index
    else:
        default_value_index = 0

    config_id = st.selectbox("Select Config:", config_ids_list, index=default_value_index,
                             key="config_iconfig_ids_listds_list")

    st.experimental_set_query_params(config_id=config_id, menu=selected_menu)
    config_details = helper.get_config_details(config_id)

    duration = st.text_input("Duration:", value=config_details['duration'], disabled=True)

    no_vus = st.text_input("VUS", value=config_details['vus'], disabled=True)
    submit = st.button("Run")

    if submit:
        process = run_subprocess(config_id, duration, no_vus)
        with st.spinner("Running Test...."):
            import time
            time.sleep((int(duration)*60))
            st.text("Completed........")


        # for line in process.stdout:
        #     st.write(line)
        #


def run_subprocess(config_id, duration, vus):
    config_details = helper.get_config_details(config_id)
    method = config_details['method']
    auth_type = config_details['auth']

    print('===============', config_details)

    command = None
    if auth_type == "Bearer" and method == "GET":
        command = f'k6 run .\\testGetAPI.js  -e configID={config_id} --duration={duration}m --vus={vus}'
    elif auth_type == "Bearer" and method == "POST":
        command = f'k6 run .\\testPostAPI.js  -e configID={config_id} --duration={duration}m --vus={vus}'
    elif auth_type == "Basic" and method == "GET":
        command = f"k6 run .\\testGetRequest.js -e configID={config_id} --duration={duration}m --vus={vus}"
    elif auth_type == "Basic" and method == "POST":
        command = f"k6 run .\\testPostRequest.js -e configID={config_id} --duration={duration}m --vus={vus}"

    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    # for line in process.stdout:
    #     # Parse the output to determine progress
    #     progress_match = re.search(r'Progress: (\d+)%', line)
    #     st.text(line)
    #     # if progress_match:
    #     #     progress = int(progress_match.group(1))
    #     #     st.progress(progress / 100)  # Update the progress bar
    #     # else:
    #     #     st.text(line)  # Display other output in the Streamlit interface
    #
    # process.wait()
    return process

