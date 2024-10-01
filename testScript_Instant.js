import http from 'k6/http';
import { group, sleep } from "k6";
import { fail } from "k6";
import { Rate, Trend } from "k6/metrics";
import { findBetween } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js';

import * as commonFunctions from './commonFunctions.js'

// let testData = open("./data/configuration/config.json")
// testData = JSON.parse(testData)

const CONFIG_ID = __ENV['configID']

let testData = {}
let REQUEST_TIME_OUT = ''
let response
let correlatedValue={}
let Request_Token_PassRate = new Rate(`Request_Token_PassRate`)
let Request_Token_TimeoutRate = new Rate(`Request_Token_TimeoutRate`)
let Request_Token_ResponseTime = new Trend(`Request_Token_ResponseTime`, true)
let Request_GetWork_PassRate = new Rate(`Request_GetWork_PassRate`)
let Request_GetWork_TimeoutRate = new Rate(`Request_GetWork_TimeoutRate`)
let Request_GetWork_ResponseTime = new Trend(`Request_GetWork_ResponseTime`, true)
let Request_Work_Attributes_PassRate = new Rate(`Request_Work_Attributes_PassRate`)
let Request_Work_Attributes_TimeoutRate = new Rate(`Request_Work_Attributes_TimeoutRate`)
let Request_Work_Attributes_ResponseTime = new Trend(`Request_Work_Attributes_ResponseTime`, true)
let Request_Patch_Project_PassRate = new Rate(`Request_Patch_Project_PassRate`)
let Request_Patch_Project_TimeoutRate = new Rate(`Request_Patch_Project_TimeoutRate`)
let Request_Patch_Project_ResponseTime = new Trend(`Request_Patch_Project_ResponseTime`, true)

export default function main(){


                //Generated Script

                group('Request_Token:',
                function () {
                
                    const params = {
                    headers: {},
                    timeout : "10m",
                    }

                    const payload = {"client_id":"SL1FOjXpVH2V03nBGqzHSMOaaXyU6_Qg6e2x9","client_secret":"1818d9fb-7987-4e60-9527-762bc025b909","grant_type":"client_credentials"}
                
                    response = http.post('https://perftestfr101.pvcloud.com/polaris/public-api/v1/oauth/token', payload, params)

                    
                });
                    correlatedValue["accessToken"]= findBetween(response.body, 'access_token":"', '",') 
                    
                sleep(1)
                
                if (response.status == 200 && "access_token") {
                    if (response.body.includes("access_token")) {
                        Request_Token_PassRate.add(true)
                        Request_Token_TimeoutRate.add(false)
                        Request_Token_ResponseTime.add(response.timings.duration)
                    }
                    else {
                        Request_Token_PassRate.add(false)
                        fail(`Response Verification failed for endpoint "/polaris/public-api/v1/oauth/token"`)
                    }
                }
                else if (response.status == 200){
                    Request_Token_PassRate.add(true)
                    Request_Token_TimeoutRate.add(false)
                    Request_Token_ResponseTime.add(response.timings.duration)
                }
                else if (response.error.includes('request timeout')) {
                    Request_Token_PassRate.add(false)
                    Request_Token_TimeoutRate.add(true)
                    fail(`Request timeout exception occured while getting attributes,API url is /polaris/public-api/v1/oauth/token`)
                }
                else {
                    Request_Token_PassRate.add(false)
                    fail(`/polaris/public-api/v1/oauth/token endpoint failed with, ${response.body}`)
                }
                
                
                //Generated Script

                group('Request_GetWork:',
                function () {
                
                    const params = {
                        headers: {"Authorization": `Bearer ${correlatedValue["accessToken"]}`},
                        timeout : "10m",
                    }
                    response = http.get("https://perftestfr101.pvcloud.com/polaris/public-api/v1/work/3787", params)
                    
                });
                correlatedValue["depth"]= findBetween(response.body, '"depth":', ',') 
                    
                sleep(1)
                
                if (response.status == 200 && "structureCode") {
                    if (response.body.includes("structureCode")) {
                        Request_GetWork_PassRate.add(true)
                        Request_GetWork_TimeoutRate.add(false)
                        Request_GetWork_ResponseTime.add(response.timings.duration)
                    }
                    else {
                        Request_GetWork_PassRate.add(false)
                        fail(`Response Verification failed for endpoint "/polaris/public-api/v1/work/3787"`)
                    }
                }
                else if (response.status == 200){
                    Request_GetWork_PassRate.add(true)
                    Request_GetWork_TimeoutRate.add(false)
                    Request_GetWork_ResponseTime.add(response.timings.duration)
                }
                else if (response.error.includes('request timeout')) {
                    Request_GetWork_PassRate.add(false)
                    Request_GetWork_TimeoutRate.add(true)
                    fail(`Request timeout exception occured while getting attributes,API url is /polaris/public-api/v1/work/3787`)
                }
                else {
                    Request_GetWork_PassRate.add(false)
                    fail(`/polaris/public-api/v1/work/3787 endpoint failed with, ${response.body}`)
                }
                
                

                //Generated Script

                group('Request_Work_Attributes:',
                function () {
                
                    const params = {
                    headers: {"Content-Type": "application/json","Authorization": `Bearer ${correlatedValue["accessToken"]}`},
                    timeout : "10m",
                    }

                    const payload = `["AC_DUR", "AC_FINISH"]`
                
                    response = http.post('https://perftestfr101.pvcloud.com/polaris/public-api/v1/work/3787/attributes', payload, params)

                    
                });
                sleep(1)
                
                if (response.status == 200 && "structureCode") {
                    if (response.body.includes("structureCode")) {
                        Request_Work_Attributes_PassRate.add(true)
                        Request_Work_Attributes_TimeoutRate.add(false)
                        Request_Work_Attributes_ResponseTime.add(response.timings.duration)
                    }
                    else {
                        Request_Work_Attributes_PassRate.add(false)
                        fail(`Response Verification failed for endpoint "/polaris/public-api/v1/work/3787/attributes"`)
                    }
                }
                else if (response.status == 200){
                    Request_Work_Attributes_PassRate.add(true)
                    Request_Work_Attributes_TimeoutRate.add(false)
                    Request_Work_Attributes_ResponseTime.add(response.timings.duration)
                }
                else if (response.error.includes('request timeout')) {
                    Request_Work_Attributes_PassRate.add(false)
                    Request_Work_Attributes_TimeoutRate.add(true)
                    fail(`Request timeout exception occured while getting attributes,API url is /polaris/public-api/v1/work/3787/attributes`)
                }
                else {
                    Request_Work_Attributes_PassRate.add(false)
                    fail(`/polaris/public-api/v1/work/3787/attributes endpoint failed with, ${response.body}`)
                }
                
                

                //Generated Script

                group('Request_Patch_Project:',
                function () {
                
                    const params = {
                    headers: {"Content-Type": "application/json","Authorization": `Bearer ${correlatedValue["accessToken"]}`},
                    timeout : "10m",
                    }

                    const payload = `{"calendar": {"structureCode": "STANDARD", "description": "Standard"}}`
                
                    response = http.patch('https://perftestfr101.pvcloud.com/polaris/public-api/v1/projects/3816', payload, params)

                    
                });
                sleep(1)
                
                if (response.status == 200 && "John Rogers - pm1") {
                    if (response.body.includes("John Rogers - pm1")) {
                        Request_Patch_Project_PassRate.add(true)
                        Request_Patch_Project_TimeoutRate.add(false)
                        Request_Patch_Project_ResponseTime.add(response.timings.duration)
                    }
                    else {
                        Request_Patch_Project_PassRate.add(false)
                        fail(`Response Verification failed for endpoint "/polaris/public-api/v1/projects/3816"`)
                    }
                }
                else if (response.status == 200){
                    Request_Patch_Project_PassRate.add(true)
                    Request_Patch_Project_TimeoutRate.add(false)
                    Request_Patch_Project_ResponseTime.add(response.timings.duration)
                }
                else if (response.error.includes('request timeout')) {
                    Request_Patch_Project_PassRate.add(false)
                    Request_Patch_Project_TimeoutRate.add(true)
                    fail(`Request timeout exception occured while getting attributes,API url is /polaris/public-api/v1/projects/3816`)
                }
                else {
                    Request_Patch_Project_PassRate.add(false)
                    fail(`/polaris/public-api/v1/projects/3816 endpoint failed with, ${response.body}`)
                }
                
                sleep(1)    
}

export function handleSummary(data) {
  let logPath = `./data/resultLogs`

  let summaryDetailsDct = commonFunctions.constructSummaryObj(CONFIG_ID, data, testData, logPath, REQUEST_TIME_OUT)
  return summaryDetailsDct
}