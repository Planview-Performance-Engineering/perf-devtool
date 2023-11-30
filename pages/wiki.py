import streamlit as st
  
st.set_page_config(page_title = "Wiki Page") 


#Title
st.title("How to use the tool")
st.header("Getting Started")

#Config Page
st.subheader("Config Page")

st.caption("Each field in config page is explained here")

st.markdown(
"""
- **Select Config Name** : There will be a default config when tool installed initially. All saved config names will be listed here. Please use different configs for api/web end point,payload,concurrent user load combination. This helps in running same test again.
Eg: API_POST_PROJECT
""",
unsafe_allow_html=True
)

st.markdown(
"""
- **Host URL** : Pass the the hostname for the API/Web request inteded for testing. Make sure this can resolved from local machine with required VPN. No need to pass the url if the application running over the local machine. Need check :red[***Are you running on local host***] for that.                 
Eg : https://myhostname.com
""",
unsafe_allow_html=True
)

st.markdown(
"""
- **Request End Point** : This is URL for the API/Web request by excluding the host name. Pass the query string parameters also here if there are any. Eg : /project/work/1234
""",
unsafe_allow_html=True
)

st.markdown(
"""
- **Request headers** : Pass the required request headers as key value pair here.
""",
unsafe_allow_html=True
)

st.code({"cookie" : "LoginCert=abcd1234"})

st.markdown(
"""
- **Request Payload** : Pass the test payload here. This will be automatically disabled for **GET** requests.                                            
""",
unsafe_allow_html=True
)

st.code({"user1" : {"name" : "","id" : ""}})

st.markdown(
"""
- **Passing random string or numbers as payload** : Follow this example for passing random string(Alphanumeric characters) or numbers as values in the request payload. As of now it supports ***string(Alphanumeric characters)*** and ***numbers***. Pass length of the parameter inside parenthisis.                            
""",
unsafe_allow_html=True
)

st.code({"user1" : {"name" : "{{String(6)}}","id" : "{{Number(10)}}"}})

st.markdown(
"""
- **Config Name** : Pass a new config name here. Keep this as unique string to avoid duplicates.                                         
""",
unsafe_allow_html=True
)

st.markdown(
"""
- **Duration in minutes** : Mention how long test should get executed.                                      
""",
unsafe_allow_html=True
)

st.warning("Recommended test duration is 5-10minutes. This test will be using local system resources and system may get exhusated due to resource crunch. ")

st.markdown(
"""
- **Expected Response String** : Mention the expected response string here.                     
Eg : "response recieved",
"succeeded"                                 
""",
unsafe_allow_html=True
)

st.markdown(
"""
- **Select Operation** : Select the HTTP method here from drop down list.                                                      
""",
unsafe_allow_html=True
)

st.markdown(
"""
- **Authentication Type** : This tool supports 4 type of authentication. Portfolios login session, Adaptive work Login session***, Bearer token and any api key as custom header.              
***Portfolios login session*** Pass DSN name, User name and Password                
***Adaptive Work login session*** Pass version number, User name and Password                                             
""",
unsafe_allow_html=True
)

st.markdown(
"""
- **No of Concurrent Users** : User has to pass concurrent user count here. This is test how concurrency is handled.                                               
""",
unsafe_allow_html=True
)

st.warning("Recommended concocurrent user count is 5-10. This again to prevent resource throttling at local system")

st.markdown(
"""
- **No of Concurrent Users** : User has to pass concurrent user count here. This is to test how concurrency is handled.                                               
""",
unsafe_allow_html=True
)

st.button("Save")

st.markdown(
"""
- **Save Buttton** : This button is to save the newly created configuration. Configuration can be saved only once. It is not allowed to edit the configuration.                                            
""",
unsafe_allow_html=True
)

st.button("Delete")

st.markdown(
"""
- **Delete Buttton** : This button can be used to delete the config if it is no longer used.                                          
""",
unsafe_allow_html=True
)

st.button("Update")

st.markdown(
"""
- **Update Buttton** : Saved configuration can be only updated with new set of credentials. Update to end point,payload, method is not allowed. This is to enable user to update the credential data if the previous token is expired.          
This is to keep the test data intact for the result comparison.                                      
""",
unsafe_allow_html=True
)

#######################################################################################################################
#Execution Page
st.subheader("Execution Page")

st.caption("Each field inside the execution page explained here")

st.markdown(
"""
- **Select Config name** : Select the config saved with payload and authentication from previous page.                                    
""",
unsafe_allow_html=True
)

st.markdown(
"""
- **Duration** : This field will be autopopulated from saved config. It is not possible to edit here to keep each execution duration identical for the selected config                                   
""",
unsafe_allow_html=True
)

st.markdown(
"""
- **No of Concurrent Users** : This field will be autopopulated from saved config. It is not possible to edit here to keep number of users identical for the selected config                                   
""",
unsafe_allow_html=True
)

st.markdown(
"""
- **Execution Name** : Provide unique execution name for each test run. This helps in identifieing each execution during result comparison. Time stamp will be considered if this field is not filled.                                
""",
unsafe_allow_html=True
)

st.button("Run", type="primary")

st.markdown(
"""
- **Run Button** : Start the execution by clicking the button. This will open a pop up with test execution tracking.                              
""",
unsafe_allow_html=True
)

st.markdown(
"""
- **Test Execution pop up** : Pop up will show the how long test is configured and remaining duration of test. Test can be killed in the middle.  
Basic result details will be displyed here after the test execution.                           
""",
unsafe_allow_html=True
)

#######################################################################################################################
#Result Page
st.subheader("Result Page")

st.checkbox("Do you want to compare 2 different configs ?")

st.markdown(
"""
- **Do you want to compare 2 different configs** : Each config defines a combination of end point, payload, concurrent users and test duration. If there is requirement to compare results from 2 different versions/confifurations, user has to check this box and list of configs get's displyed and user can pick 1 result from both the configs.                           
""",
unsafe_allow_html=True
)

st.markdown(
"""
- **Select Config Name** : There will be list of configs user has saved. Select one among them and list of results will be displayed for selected config.                   
""",
unsafe_allow_html=True
)


st.markdown(
"""
- **Compared two results** : By default 2 set of results get's displyed if the selected config has multiple executions.                   
""",
unsafe_allow_html=True
)

st.caption("Result metrics and details")

st.markdown(
"""
- **95th percentile response time in ms** : This is 95th percetile value of response time in milli seconds. 95th percent of time of response time observed below this number.               
""",
unsafe_allow_html=True
)

st.markdown(
"""
- **Average response time in ms** : Average request response time in milli seconds.                
""",
unsafe_allow_html=True
)

st.markdown(
"""
- **Maximum response time in ms** : Maximum amount time request took respond back. This is highest response time among all.              
""",
unsafe_allow_html=True
)

st.markdown(
"""
- **Minimum response time in ms** : Minimum amount time request took respond back. This is minimum response time among all.              
""",
unsafe_allow_html=True
)

st.markdown(
"""
- **Request timeout Rate in Percentage** : Percentage of response failure observed among all requests.     
""",
unsafe_allow_html=True
)

st.markdown(
"""
- **Pass Rate in Percentage** : How many requests have successfully processed and returned valid response. 
""",
unsafe_allow_html=True
)

st.markdown(
"""
- **Duration in min** : How long test was executed. This is in minutes.
""",
unsafe_allow_html=True
)

st.markdown(
"""
- **Concurrent Users** : How many concurrent users are used during the test or in the selected config. This can reffered as concurrent threads also. 
""",
unsafe_allow_html=True
)

st.markdown(
"""
- **Iterations** : How many times given request was executed during the test window. 
""",
unsafe_allow_html=True
)

st.button("Delete the run test1",type="primary")

st.markdown(
"""
- **Delete the run** : To delete the execution record from the database. 
""",
unsafe_allow_html=True
)

st.subheader("Setting expectations about the tool")

st.markdown(
"""
- This tool is designed for only performance comparison of the pre and post code changes and 2 different versions of API/Web requests.
- This is tool will not help in deciding Performance of API/Web request or deciding the capacity of the requests.
- This tool designed to test single web/api request. Tool will not accommodate set of requests.
- This tool will be using resources from local system. Network bandwidth, number of applications running in the docker will have impact on the results. Make sure the number of docker applications running and network bandwidth is identical if you are comparing two results. 
""",
unsafe_allow_html=True
)






