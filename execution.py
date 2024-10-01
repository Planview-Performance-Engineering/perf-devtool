import streamlit as st
from streamlit_modal import Modal
import subprocess
import os
import signal
import time,json
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

    st.query_params["config_id"] = config_id
    st.query_params["menu"] = selected_menu
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
                    # console_ctrl.send_ctrl_c(process.pid)
                    # os.kill(process.pid, signal.SIGKILL)
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
            # console_ctrl.send_ctrl_c(process.pid)
            # os.kill(process.pid, signal.SIGKILL)
        elif 'Request' in line or 'iterations...' in line:
            str_line = line.replace('âœ“', '').replace('âœ—', '')
            results += '\n' + str_line + '\n'
        elif 'Request' in line:
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
    build_k6Script(config_id)

    if not os.path.isdir(f"./data/resultLogs/{config_id}"):
        os.makedirs(f"./data/resultLogs/{config_id}")

    command = f'k6 run ./testScript_Instant.js -e configID={config_id} -e runName={run_name} --duration={duration}m --vus={vus}'

    # if method == "GET":
    #     command = f'k6 run ./testGet.js  -e configID={config_id} -e runName={run_name} --duration={duration}m --vus={vus}'
    # elif method == "POST":
    #     command = f'k6 run ./testPost.js  -e configID={config_id} -e runName={run_name} --duration={duration}m --vus={vus}'
    # elif method == "PATCH":
    #     command = f'k6 run ./testPatch.js  -e configID={config_id} -e runName={run_name} --duration={duration}m --vus={vus}'
    # elif method == "PUT":
    #     command = f'k6 run ./testPut.js  -e configID={config_id} -e runName={run_name} --duration={duration}m --vus={vus}'

    # if auth_type == "Bearer" and method == "GET":
    #     command = f'k6 run ./testGetAPI.js  -e configID={config_id} -e runName={run_name} --duration={duration}m --vus={vus}'
    # elif auth_type == "Bearer" and method == "POST":
    #     command = f'k6 run ./testPostAPI.js  -e configID={config_id} -e runName={run_name} --duration={duration}m --vus={vus}'
    # elif auth_type in ["Basic", "CustomAuth_ThroughHeader"] and method == "GET":
    #     command = f"k6 run ./testGetRequest.js -e configID={config_id} -e runName={run_name} --duration={duration}m --vus={vus}"
    # elif auth_type in ["Basic", "CustomAuth_ThroughHeader"] and method == "POST":
    #     command = f"k6 run ./testPostRequest.js -e configID={config_id} -e runName={run_name} --duration={duration}m --vus={vus}"

    process = subprocess.Popen(
        # "exec " + command,
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=True,
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

    return process

def build_k6Script(config_id):

    config_details = helper.get_config_details1(config_id)

    js_file_path = "testScript.js"

    responseValidation = """
                sleep({SLEEP_TIME})
                
                if (response.status == 200 && "{VERIFY_STRING}") {{
                    if (response.body.includes("{VERIFY_STRING}")) {{
                        {request}_PassRate.add(true)
                        {request}_TimeoutRate.add(false)
                        {request}_ResponseTime.add(response.timings.duration)
                    }}
                    else {{
                        {request}_PassRate.add(false)
                        fail(`Response Verification failed for endpoint "{REQUEST_URL}"`)
                    }}
                }}
                else if (response.status == 200){{
                    {request}_PassRate.add(true)
                    {request}_TimeoutRate.add(false)
                    {request}_ResponseTime.add(response.timings.duration)
                }}
                else if (response.error.includes('request timeout')) {{
                    {request}_PassRate.add(false)
                    {request}_TimeoutRate.add(true)
                    fail(`Request timeout exception occured while getting attributes,API url is {REQUEST_URL}`)
                }}
                else {{
                    {request}_PassRate.add(false)
                    fail(`{REQUEST_URL} endpoint failed with, ${{response.body}}`)
                }}
                
                """

    with open(js_file_path, "r") as js_file:
        js_code = js_file.readlines()

        request_string = ''

        init_string = """let response
let correlatedValue={}"""

        for request in config_details["RequestData"]:

            init_string += """
let {request}_PassRate = new Rate(`{request}_PassRate`)
let {request}_TimeoutRate = new Rate(`{request}_TimeoutRate`)
let {request}_ResponseTime = new Trend(`{request}_ResponseTime`, true)""".format(request=request)
            
            ITERATIONS_SLEEPTIME = config_details["iterations_sleepTime"]

            HEADER = config_details["RequestData"][request]["requestHeaders"]

            METHOD = config_details["RequestData"][request]["method"]

            REQUEST_TIME_OUT = '10m'

            HOST = config_details["RequestData"][request]["hostname"]

            REQUEST_URL = config_details["RequestData"][request]["endpoint"]

            REQUEST_PAYLOAD = config_details["RequestData"][request]["payload"]

            VERIFY_STRING = config_details["RequestData"][request]["verifyString"]

            LEFT_BOUNDARY = config_details["RequestData"][request]["left"]

            RIGHT_BOUNDARY = config_details["RequestData"][request]["right"]

            CAPTURED_VALUE = config_details["RequestData"][request]["nameOfCapturedValue"]

            SLEEP_TIME = config_details["RequestData"][request]["sleepTime"]

            if (config_details["RequestData"][request]["payloadAsString"]):

                REQUEST_PAYLOAD = "`"+ REQUEST_PAYLOAD + "`"

            
            if METHOD == "GET":


                request_string += """
                //Generated Script

                group('{request}:',
                function () {{
                
                    const params = {{
                        headers: {HEADER},
                        timeout : "10m",
                    }}
                    response = http.get("{HOST}{REQUEST_URL}", params)
                    
                }});""".format(HEADER=HEADER, request=request, HOST=HOST, REQUEST_URL=REQUEST_URL, REQUEST_TIME_OUT=REQUEST_TIME_OUT)

                if CAPTURED_VALUE:

                    request_string += """
                correlatedValue["{CAPTURED_VALUE}"]= findBetween(response.body, '{LEFT_BOUNDARY}', '{RIGHT_BOUNDARY}') 
                    """.format(CAPTURED_VALUE=CAPTURED_VALUE, LEFT_BOUNDARY=LEFT_BOUNDARY, RIGHT_BOUNDARY=RIGHT_BOUNDARY)

                request_string += responseValidation.format(request=request, REQUEST_URL=REQUEST_URL, VERIFY_STRING=VERIFY_STRING, SLEEP_TIME=SLEEP_TIME)
                

            elif METHOD ==  "POST" or "PATCH":

                httpMethod = METHOD.lower()

                request_string += """

                //Generated Script

                group('{request}:',
                function () {{
                
                    const params = {{
                    headers: {HEADER},
                    timeout : "10m",
                    }}

                    const payload = {REQUEST_PAYLOAD}
                
                    response = http.{httpMethod}('{HOST}{REQUEST_URL}', payload, params)

                    
                }});""".format(HEADER=HEADER, request=request, HOST=HOST, REQUEST_URL=REQUEST_URL, REQUEST_PAYLOAD=REQUEST_PAYLOAD, REQUEST_TIME_OUT=REQUEST_TIME_OUT, httpMethod=httpMethod)

                if CAPTURED_VALUE:

                    request_string += """
                    correlatedValue["{CAPTURED_VALUE}"]= findBetween(response.body, '{LEFT_BOUNDARY}', '{RIGHT_BOUNDARY}') 
                    """.format(CAPTURED_VALUE=CAPTURED_VALUE, LEFT_BOUNDARY=LEFT_BOUNDARY, RIGHT_BOUNDARY=RIGHT_BOUNDARY)

                request_string += responseValidation.format(request=request, REQUEST_URL=REQUEST_URL, VERIFY_STRING=VERIFY_STRING, SLEEP_TIME=SLEEP_TIME)
        
        request_string +="""sleep({ITERATIONS_SLEEPTIME})""".format( ITERATIONS_SLEEPTIME= ITERATIONS_SLEEPTIME)

        js_code[19] = request_string

        js_code[15] = init_string

        js_code_str = ''.join(js_code)

    with open("testScript_Instant.js", "w") as js_file:
        js_file.write(js_code_str)

