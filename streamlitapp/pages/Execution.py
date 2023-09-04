import streamlit as st
import json

# from streamlitapp.utils import helper


def read_config():
    config_file = open('.\\data\\config.json')
    config_json = json.load(config_file)
    return config_json


def get_config_ids_lst():
    config_json = read_config()
    config_ids_lst = list(config_json.keys())
    return config_ids_lst


def get_config_details(config_id):
    config_json = read_config()
    config_details = config_json[config_id]
    return config_details


def add_config_details():
    st.set_page_config(page_title="PerfDevTool", page_icon=None)
    config_ids_list = get_config_ids_lst()
    session_state_config_id = st.session_state.config_id_selected if 'config_id_selected' in st.session_state else None
    selected_config_id = config_ids_list.index(session_state_config_id) if session_state_config_id else None
    default_value_index = selected_config_id if selected_config_id else 0

    config_id = st.selectbox("Select Config:", config_ids_list, index=default_value_index,
                             key="config_iconfig_ids_listds_list")

    host = st.text_input("Duration:", placeholder="Enter test duration")

    host = st.text_input("VUS", placeholder="Enter virtual users")



add_config_details()