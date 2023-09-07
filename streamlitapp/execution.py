import streamlit as st
import subprocess
import os

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
        st.text("Running Test...")
        process = run_subprocess(config_id, duration, no_vus)
        status, results = verify_results(process)
        if status:
            st.success(f"Test Completed With Below Results: \n {results}")
        else:
            st.error(f"Test Failed with \n {results}")


def verify_results(process):
    results = ''
    status = True
    for line in process.stdout:
        if 'error' in line:
            status = False
            results += '\n' + line + '\n'
            process.kill()
        elif 'RequestEndpoint' in line:
            results += '\n' + line + '\n'
    return status, results


def run_subprocess(config_id, duration, vus):
    config_details = helper.get_config_details(config_id)
    method = config_details['method']
    auth_type = config_details['auth']

    if not os.path.isdir(f"./resultLogs/{config_id}"):
        os.mkdir(f"./resultLogs/{config_id}")

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
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=True,
    )

    return process

