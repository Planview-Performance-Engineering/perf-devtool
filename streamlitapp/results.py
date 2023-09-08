import json

import streamlit as st
from utils import helper



def get_result_data(config_ids_list, default_config_index, selected_menu):

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

    #config_details = helper.get_config_details(config_id)

    result_details = helper.get_execution_list(config_id)


    if result_details:

        execution_id = list()

        #st.subheader("Select results for comparison")

        st.write("Number of test executions :",len(result_details))

        left, right = st.columns(2)

        alignment = left

        for val in range(1 if len(result_details)<2 else 2):
                
            execution_id.append(alignment.selectbox("Select results : "+str(val+1), result_details, index = val, key = "execution_id_"+str(val)))

            alignment = right if alignment==left else left


        metric_data = helper.get_result_data(config_id, execution_id)

        alignment = left
        
        for execid,metric in metric_data.items():

            for metric_name,metric_value in metric.items():

                    alignment.metric(metric_name, metric_value, delta=None, delta_color="normal", help=None, label_visibility="visible")

            alignment = right if alignment==left else left

    else:

        st.warning("No Execution exists for this config. Please execute test !!!")