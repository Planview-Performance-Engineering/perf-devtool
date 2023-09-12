import json
import pandas as pd
import altair as alt

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

    # config_details = helper.get_config_details(config_id)

    result_details = helper.get_execution_list(config_id)

    if result_details:

        execution_id = list()

        no_of_results = len(result_details)

        st.write("Number of test executions :", no_of_results)

        left, right, last = st.columns([1, 1, 4])

        execution_id.append(left.selectbox("Select results : 1", result_details, index=0, key="execution_id_0"))

        if no_of_results > 1:
            execution_id.append(right.selectbox("Select results 2: ", result_details, index=1, key="execution_id_1"))

        metric_data = helper.get_result_data(config_id, execution_id)
            
        alignment = left

        for execid, metric in metric_data.items():

            if len(metric) is not 0:

                for metric_name, metric_value in metric.items():
                    alignment.metric(metric_name, metric_value, delta=None, delta_color="normal", help=None,
                                        label_visibility="visible")
            else:

                alignment.error("Test did not get initiated properly")

                if alignment.button("Delete the run "+execid, type = "primary"):
                    
                    helper.delete_result(config_id, execid)

                    st.experimental_rerun()

            alignment = right if alignment == left else left

        if (len(metric_data.keys()) > 1):

            last.markdown("<h2 style='text-align: center;'>Graphical Comparison</h2>", unsafe_allow_html=True)

            for (metric_label_1, metric_label_2) in zip(metric_data[execution_id[0]], metric_data[execution_id[1]]):

                source = pd.DataFrame({

                'Test Runs': [execution_id[0], execution_id[1]],
                metric_label_1: [metric_data[execution_id[0]][metric_label_1],
                                        metric_data[execution_id[1]][metric_label_2]]

                })

                bar_chart = alt.Chart(source).mark_bar().encode(y='Test Runs', x=metric_label_1, )

                last.altair_chart(bar_chart, use_container_width=True, theme="streamlit")
    else:

        st.warning("No Execution exists for selected config!!")
