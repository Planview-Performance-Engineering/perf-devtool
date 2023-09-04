import streamlit as st
from utils import helper


def get_run_params(default_config_index, selected_menu):
    config_ids_list = helper.get_config_ids_lst()

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

    host = st.text_input("Duration:", placeholder="Enter test duration")

    host = st.text_input("VUS", placeholder="Enter virtual users")