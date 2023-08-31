import streamlit as st
import json


class AddConfig:
    def __init__(self, streamlit_obj):
        self.streamlit_obj = streamlit_obj
        self.operation = None
        self.host = None
        self.api_endpoint = None
        self.is_local_host = None
        self.payload = None
        self.auth_type = None
        self.payload_type = None

    def get_config_list(self):
        config_file = open('.\\data\\config.json')

        config_json = json.load(config_file)
        config_ids_lst = list(config_json.keys())
        return config_ids_lst

    def get_config_details(self):
        with self.streamlit_obj:
            config_list = self.get_config_list()
            option_selected = st.selectbox('Select Config:', config_list)
            self.left, self.right = st.columns(2)
            self.host = self.left.text_input('Host URL:', value="http://localhost", placeholder="Enter host url")
            self.is_local_host = self.right.checkbox("Are you running on local host", key='chk_Unique_item')
            self.api_endpoint = self.left.text_input("API End Point:", placeholder="Enter end point with query parameters")
            self.operation = self.right.selectbox('Select Operation:', ('GET', 'POST'))
            if self.operation == "POST":
                self.payload = self.left.text_area("Request Payload")
                self.payload_type = self.right.selectbox("Payload Type", ("application/json", "application/x-www-form-urlencoded", ))
            self.auth_type = self.right.selectbox("Authorization:", ('Basic', 'Bearer'))

            if self.auth_type == "Basic":
                self.api_endpoint = self.right.text_input("DSN:", placeholder="Enter DSN Name")
                self.api_endpoint = self.right.text_input("User Name:", placeholder="Enter User Name")
                self.api_endpoint = self.right.text_input("Password:", placeholder="Enter Password")
            elif self.auth_type == "Bearer":
                self.api_endpoint = self.right.text_input("Token:", placeholder="Bearer <token>")

            file_name = self.left.text_input("Config ID:", placeholder="Enter unique Name to save config details")
            if self.right.button("Save"):
                self.save_config(file_name)

    def save_config(self, file_name):
        config_dct = {
            file_name: {
                "hostname": self.host,
                "endpoint": self.api_endpoint,
                "method": self.operation,
                "isLocalhost": self.is_local_host,
                "payload": self.payload,
                "payloadType": self.payload_type,
                "auth": self.auth_type
            }
        }
        config_ids_lst = self.get_config_list()

        config_file = open('.\\data\\config.json')

        config_json = json.load(config_file)

        config_json.update(config_dct)

        with open(".\\data\\config.json", "w") as jsonfile:
            json.dump(config_json, jsonfile)


