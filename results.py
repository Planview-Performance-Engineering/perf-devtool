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


def plot_graphs(execution1, testResult1, execution2, testResult2, position):
    df = pd.DataFrame(
        [[execution1, testResult1['95th percentile response time in ms'],
          testResult1['Average response time in ms']],
         [execution2, testResult2['95th percentile response time in ms'],
          testResult2['Average response time in ms']]],
        columns=["Test Results", "95th percentile response time in ms", "Average response time in ms"]
    )

    fig = px.bar(df, x="Test Results", y=["95th percentile response time in ms", "Average response time in ms"],
                 text_auto=True, barmode='group', height=400, labels={"variable": "Metrics"})

    fig.update_layout(
        yaxis=dict(
            title='Response time in milli seconds',
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
    position.dataframe(df)
    position.plotly_chart(fig)


def compare_results_diff_configs(config_id1, config_id2):
    # result_details1 = helper.get_execution_list(config_id1)
    # result_details2 = helper.get_execution_list(config_id2)

    result_details = [helper.get_execution_list(config_id1), helper.get_execution_list(config_id2)]

    left, right, last = st.columns([1, 1, 2.5])

    position = left

    config_id = [config_id1, config_id2]

    execution_context = []

    for result, config in zip(result_details, config_id):
        if result:
            execution_id = position.selectbox(config, result, key=config)
            test_results = helper.get_results(config, execution_id)
            display_results(position, test_results, execution_id, config)

            execution_context.append(execution_id)
            execution_context.append(test_results)

        else:
            position.warning("No Execution exists for selected config!! " + config)

        position = right

    if len(execution_context) == 4:
        plot_graphs(execution_context[0], execution_context[1], execution_context[2], execution_context[3], last)


def compare_results(config_id):
    result_details = helper.get_execution_list(config_id)

    if result_details:

        no_of_results = len(result_details)

        st.write(":blue[Number of test executions]", no_of_results)

        left, right, last = st.columns([1, 1, 2.5])

        execution_id_1 = left.selectbox(":blue[Select results 1]", result_details, index=0, key="execution_id_0")

        test_a_results = helper.get_results(config_id, execution_id_1)
        display_results(left, test_a_results, execution_id_1, config_id)

        test_b_results = None
        execution_2 = None

        if no_of_results > 1:
            execution_2 = right.selectbox(":blue[Select results 2]", result_details, index=1, key="execution_id_1")
            if execution_id_1 != execution_2:
                test_b_results = helper.get_results(config_id, execution_2)
                display_results(right, test_b_results, execution_2, config_id)

        if test_a_results and test_b_results:
            plot_graphs(execution_id_1, test_a_results, execution_2, test_b_results, last)
    else:
        st.warning("No Execution exists for selected config!!")


def get_result_data(config_ids_list, default_config_index, selected_menu):
    session_state_config_id = st.session_state.config_id_selected if 'config_id_selected' in st.session_state else None
    selected_config_id = config_ids_list.index(session_state_config_id) if session_state_config_id else None

    if selected_config_id:
        default_value_index = selected_config_id
    elif default_config_index:
        default_value_index = default_config_index
    else:
        default_value_index = 0

    compare_multiple = st.checkbox("Do you want to compare 2 different configs ?")

    if compare_multiple:

        column1, column2 = st.columns(2)

        config1 = column1.selectbox(":blue[Select first config Name]", config_ids_list, index=0,
                                    key="config_iconfig_ids_listds_list")

        config2 = column2.selectbox(":blue[Select second config Name]", config_ids_list, index=1,
                                    key="config_iconfig_ids_listds_list_1")
        st.experimental_set_query_params(config_id1=config1, config_id2=config2, menu=selected_menu)
        compare_results_diff_configs(config1, config2)

    else:

        config_id = st.selectbox(":blue[Select Config Name]", config_ids_list, index=default_value_index,
                                 key="config_iconfig_ids_listds_list")
        st.experimental_set_query_params(config_id=config_id, menu=selected_menu)

        compare_results(config_id)
