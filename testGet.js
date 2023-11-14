import http from 'k6/http';
import { group, sleep } from "k6";

import * as commonFunctions from './commonFunctions.js'

let testData = open("./data/configuration/config.json")
testData = JSON.parse(testData)

const CONFIG_ID = __ENV['configID']

const envData = testData[CONFIG_ID]
const HOST = envData['hostname']
const REQUEST_URL = envData['endpoint']
const REQUEST_TIME_OUT = __ENV['timeout'] || '3m'
const TOKEN = envData['token']
const REQUEST_HEADERS = envData['requestHeaders']
const VERIFY_STRING = envData['verifyString']
const DSN = envData['dsn']
const USERNAME = envData['username']
const PASSWORD = envData['password']
const AWUSERNAME = envData['awUsername']
const AWPASSWORD = envData['awPassword']
const AWVERSION = envData ['awVersion']
const AUTH = envData['auth']

let headers = {}

let adminLoginCert;

export default function main(){
    let vuJar = http.cookieJar();

    if (AUTH == "PortfoliosLogin") {
        if (!adminLoginCert) {
            adminLoginCert = commonFunctions.login(HOST, DSN, USERNAME, PASSWORD, REQUEST_TIME_OUT)
        }
        vuJar.set(`${HOST}`, 'LoginCert', adminLoginCert)
        sleep(3)
    }   
    else if(AUTH == "AWLogin"){
        commonFunctions.awLogin(HOST, AWVERSION, AWUSERNAME, AWPASSWORD, REQUEST_TIME_OUT)
    }
    else if(AUTH == "Bearer Token/Session ID"){
        Object.assign(headers, {"Authorization": TOKEN})
    }

    if(REQUEST_HEADERS){
        Object.assign(headers, JSON.parse(REQUEST_HEADERS))
    }

    const params = {
        headers: headers,
        timeout : REQUEST_TIME_OUT
    }

    group(`Request Endpoint:`,
    function () {
        const response = http.get(`${HOST}${REQUEST_URL}`, params)
        commonFunctions.verifyResponseStatus(response, REQUEST_URL, 'GETAPI', VERIFY_STRING, REQUEST_TIME_OUT)
    }
    );
    
}

export function handleSummary(data) {
  let logPath = `./data/resultLogs`

  let summaryDetailsDct = commonFunctions.constructSummaryObj(CONFIG_ID, data, envData, logPath, REQUEST_TIME_OUT)
  return summaryDetailsDct
}