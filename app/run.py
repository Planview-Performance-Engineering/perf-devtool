import streamlit as st


from add_config import AddConfig

config_tab, execution, results = st.tabs(["Configuration", "Execution", "Results"])
obj = AddConfig(config_tab)
obj.get_config_details()