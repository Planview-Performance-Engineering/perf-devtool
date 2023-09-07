import json


import streamlit as st
from utils import helper


def get_result_data(config_ids_list, default_config_index, selected_menu):

    #config_ids_list = helper.get_config_ids_lst()

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

    result_details = helper.get_execution_list(config_id)

    st.subheader("Select results for comparison")

    left, right = st.columns(2)

    execution_id_1 = left.selectbox("Select Result 1", result_details, index = 0, key = "execution_id_1")

    execution_id_2 = right.selectbox("Select Result 2", result_details, index = 0, key = "execution_id_2")

    if st.button("Get Results"):
        helper.get_result_data(config_id, execution_id_1, execution_id_2)

    #left.metric("95th reponse time", "1s", delta=None, delta_color="normal", help=None, label_visibility="visible")

    #left.metric("response time", "1s", delta=None, delta_color="normal", help=None, label_visibility="visible")