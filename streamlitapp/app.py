import streamlit as st
from streamlit_option_menu import option_menu

from utils import helper
import configuration, execution, results

menu_lst = ["Config", "Execution", "Results"]

st.set_page_config(page_title="PerfDevTool",
                   page_icon="data:image/png;base64,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",
                   layout="wide")


class MyApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):

        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):

        query_params = st.experimental_get_query_params()

        config_ids_list = helper.get_config_ids_lst()
        default_config_id = query_params["config_id"][0] if "config_id" in query_params else None
        default_config_index = config_ids_list.index(default_config_id) if default_config_id else 0

        default_menu = query_params["menu"][0] if "menu" in query_params else None
        default_menu_index = menu_lst.index(default_menu) if default_menu else 0

        selected_menu = option_menu(None, menu_lst, icons=['gear-fill', 'play-circle', "check2-circle"], key='mymenu',
                                    menu_icon="cast", default_index=default_menu_index, orientation="horizontal",
                                    styles={
                                        "container": {"padding": "0!important", "background-color": "#fafafa"},
                                        "icon": {"color": "orange", "font-size": "20px"},
                                        "nav-link": {"font-size": "20px", "text-align": "left", "margin": "0px",
                                                     "--hover-color": "#eee"},
                                        "nav-link-selected": {"background-color": "#8fbc8f"},
                                    }
                                    )
        selected_menu

        if selected_menu == "Config":
            configuration.add_config_details(config_ids_list, default_config_index, selected_menu)

        if selected_menu == "Execution":
            execution.get_run_params(config_ids_list, default_config_index, selected_menu)

        if selected_menu == "Results":
            results.get_result_data(config_ids_list, default_config_index, selected_menu)


MyApp().run()
