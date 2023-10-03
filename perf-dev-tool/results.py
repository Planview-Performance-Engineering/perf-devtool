import pandas as pd
import plotly.express as px

import streamlit as st
from utils import helper


def display_results(left, results_data, execution_id, config_id):
    if results_data:
        for metric_name, metric_value in results_data.items():
            left.metric(metric_name, metric_value, delta=None, delta_color="normal", help=None,
                        label_visibility="visible")
    else:
        left.error("Test did not get initiated properly")

        if left.button("Delete the run " + execution_id, type="primary"):
            helper.delete_result(config_id, execution_id)
            st.experimental_rerun()


def get_result_data(config_ids_list, default_config_index, selected_menu):
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

    # config_details = helper.get_config_details(config_id)

    result_details = helper.get_execution_list(config_id)

    if result_details:

        no_of_results = len(result_details)

        st.write(":blue[Number of test executions]", no_of_results)

        left, right, last = st.columns([1, 1, 2.5])

        execution_id_1 = left.selectbox(":blue[Select results 1]", result_details, index=0, key="execution_id_0")

        test_a_results = helper.get_results(config_id, execution_id_1)
        display_results(left, test_a_results, execution_id_1, config_id)

        test_b_results = None
        #execution_2 = None

        if no_of_results > 1:
            execution_2 = right.selectbox(":blue[Select results 2]", result_details, index=1, key="execution_id_1")
            if execution_id_1 != execution_2:
                test_b_results = helper.get_results(config_id, execution_2)
                display_results(right, test_b_results, execution_2, config_id)

        if test_a_results and test_b_results:
            df = pd.DataFrame(
                [[execution_id_1 , test_a_results['95th percentile response time in ms'],
                  test_a_results['Average response time in ms']],
                 [execution_2 , test_b_results['95th percentile response time in ms'],
                  test_b_results['Average response time in ms']]],
                columns=["Test Results", "95th percentile response time in ms", "Average response time in ms"]
            )

            fig = px.bar(df, x="Test Results", y=["95th percentile response time in ms", "Average response time in ms"],
                         text_auto=True, barmode='group', height=400, labels={"variable": "Metrics"})

            fig.update_layout(
                yaxis=dict(
                    title='Response Time in MS',
                    titlefont_size=16,
                    tickfont_size=14,
                ),
                legend=dict(
                    bgcolor='rgba(255, 255, 255, 0)',
                    bordercolor='rgba(255, 255, 255, 0)'
                ),
                barmode='group',
                bargap=0.3,  # gap between bars of adjacent location coordinates.
                bargroupgap=0.05  # gap between bars of the same location coordinate.
            )
            last.dataframe(df)
            last.plotly_chart(fig)

    else:

        st.warning("No Execution exists for selected config!!")
