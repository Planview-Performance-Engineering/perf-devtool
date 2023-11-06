import streamlit as st
from streamlit_modal import Modal
import subprocess
import os
import signal
import time
#import console_ctrl

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

    config_id = st.selectbox(":blue[Select Config Name]", config_ids_list, index=default_value_index,
                             key="config_iconfig_ids_listds_list")

    st.experimental_set_query_params(config_id=config_id, menu=selected_menu)
    config_details = helper.get_config_details(config_id)

    duration = st.text_input(":blue[Duration]", value=config_details['duration'], disabled=True)

    no_vus = st.text_input(":blue[No of Concurrent Users]", value=config_details['vus'], disabled=True)

    run_name = st.text_input(":blue[Execution Name]", placeholder="Unique name to save results, if not provided"
                                                                  " results will be saved with timestamp")

    submit = st.button("Run", type="primary")

    if submit:
        model = Modal(key="results-key", title="Test Execution of "+config_id)
        with model.container():
            with st.spinner("Running Test...."):
                placeholder = st.empty()
                process = run_subprocess(config_id, duration, no_vus, run_name)
                if placeholder.button("Stop", key=1, type="primary"):
                    #console_ctrl.send_ctrl_c(process.pid)
                    os.kill(process.pid, signal.SIGKILL)
                    process.wait()
                    model.close()
                status, results = verify_results(process,duration)
                if status:
                    st.success(f"Test Completed With Below Results: \n {results}")
                else:
                    st.error(f"Test Failed with \n {results}")
                #asyncio.run(timer(duration,placeholder1))
                placeholder.button("OK", key=2, type="primary")


def verify_results(process,duration):

    # placeholder = st.empty()
    # stop = placeholder.button("Stop", key=1, type ="primary")
    placeholder1 = st.empty()
    start_time = time.time()    
    progress_text = "Test is initializing"
    progress_bar = st.progress(0, text=progress_text)
    results = ''
    status = True
    for line in process.stdout:
        # if stop:
        #     status = False
        #     results += '\n' + line + '\n'
        #     os.kill(process.pid, signal.SIGTERM)
        #     process.wait()
        if 'level=error' in line:
            status = False
            results += '\n' + line + '\n'
            #console_ctrl.send_ctrl_c(process.pid)
            os.kill(process.pid, signal.SIGKILL)
        elif 'RequestEndpoint' in line or 'iterations...' in line:
            str_line = line.replace('âœ“', '').replace('âœ—', '')
            results += '\n' + str_line + '\n'
        elif 'RequestEndpoint' in line:
            results += '\n' + line + '\n'

        current_time = time.time()
        elapsed_time = max(0, int(current_time - start_time)) 

        if elapsed_time < (int(duration)*60):
            placeholder1.write(f"Total Test duration {duration} minutes")
            progressed_time_weighted = round(elapsed_time*(100/(int(duration)*60)))  # To calculate percentage of complettion of out of 100
            progress_text = "Elapsed test duration " + str(elapsed_time) + " seconds"
            progress_bar.progress(progressed_time_weighted, text=progress_text)
        else:
            placeholder1.write(f"Result consolidation is in progress...")

    
    placeholder1.empty()
    progress_bar.empty()
    return status, results


def run_subprocess(config_id, duration, vus, run_name):
    config_details = helper.get_config_details(config_id)
    method = config_details['method']
    auth_type = config_details['auth']
    run_name = run_name.replace(" ", "_")

    if not os.path.isdir(f"./data/resultLogs/{config_id}"):
        os.makedirs(f"./data/resultLogs/{config_id}")

    command = None
    if auth_type == "Bearer" and method == "GET":
        command = f'k6 run ./testGetAPI.js  -e configID={config_id} -e runName={run_name} --duration={duration}m --vus={vus}'
    elif auth_type == "Bearer" and method == "POST":
        command = f'k6 run ./testPostAPI.js  -e configID={config_id} -e runName={run_name} --duration={duration}m --vus={vus}'
    elif auth_type in ["Basic", "CustomAuth_ThroughHeader"] and method == "GET":
        command = f"k6 run ./testGetRequest.js -e configID={config_id} -e runName={run_name} --duration={duration}m --vus={vus}"
    elif auth_type in ["Basic", "CustomAuth_ThroughHeader"] and method == "POST":
        command = f"k6 run ./testPostRequest.js -e configID={config_id} -e runName={run_name} --duration={duration}m --vus={vus}"

    process = subprocess.Popen(
       "exec " + command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=True,
        #creationflags=subprocess.CREATE_NEW_CONSOLE
    )

    return process