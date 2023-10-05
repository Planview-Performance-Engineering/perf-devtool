import streamlit as st
from streamlit_modal import Modal
import subprocess
import os
import signal
import asyncio
import console_ctrl
import multiprocessing, time

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
                #placeholder1 = st.empty()
                process = run_subprocess(config_id, duration, no_vus, run_name)
                # if placeholder.button("Stop", key=1, type="primary"):
                #     console_ctrl.send_ctrl_c(process.pid)
                #     #os.kill(process.pid, signal.SIGKILL)
                #     model.close()
                status, results = verify_results(process)
                if status:
                    st.success(f"Test Completed With Below Results: \n {results}")
                else:
                    st.error(f"Test Failed with \n {results}")
                #asyncio.run(timer(duration,placeholder1))
                placeholder.text("Test Completed!! Proceed towards results")
                #placeholder.button("Stop", disabled=True, key=2)


def verify_results(process):

    stop = st.button("Stop", key=1, type="primary")

    results = ''
    status = True
    for line in process.stdout:
        if stop:
            status = False
            results = 'Test Terminated'
            console_ctrl.send_ctrl_c(process.pid)
        elif 'level=error' in line:
            status = False
            results += '\n' + line + '\n'
            console_ctrl.send_ctrl_c(process.pid)
            #os.kill(process.pid, signal.SIGKILL)
        elif 'RequestEndpoint' in line or 'iterations...' in line:
            str_line = line.replace('âœ“', '').replace('âœ—', '')
            results += '\n' + str_line + '\n'
            #console_ctrl.send_ctrl_c(process.pid)
        elif 'RequestEndpoint' in line:
            results += '\n' + line + '\n'
    
    return status, results


def run_subprocess(config_id, duration, vus, run_name):
    config_details = helper.get_config_details(config_id)
    method = config_details['method']
    auth_type = config_details['auth']

    if not os.path.isdir(f"./resultLogs/{config_id}"):
        os.mkdir(f"./resultLogs/{config_id}")

    command = None
    if auth_type == "Bearer" and method == "GET":
        command = f'k6 run ./testGetAPI.js  -e configID={config_id} -e runName={run_name} --duration={duration}m --vus={vus}'
    elif auth_type == "Bearer" and method == "POST":
        command = f'k6 run ./testPostAPI.js  -e configID={config_id} -e runName={run_name} --duration={duration}m --vus={vus}'
    elif auth_type == "Basic" and method == "GET":
        command = f"k6 run ./testGetRequest.js -e configID={config_id} -e runName={run_name} --duration={duration}m --vus={vus}"
    elif auth_type == "Basic" and method == "POST":
        command = f"k6 run ./testPostRequest.js -e configID={config_id} -e runName={run_name} --duration={duration}m --vus={vus}"

    process = subprocess.Popen(
        #"exec " + command,
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=True,
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

    return process

async def timer(duration,placeholder):
    N = int(duration)*60
    for secs in range(N,0,-1):
        mm, ss = secs//60, secs%60
        placeholder.metric("Test duration remaining in min::sec", f"{mm:02d}:{ss:02d}")
        await asyncio.sleep(1)
    placeholder.metric("Test duration remaining",value="", label_visibility="hidden")
