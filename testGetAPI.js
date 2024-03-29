import http from 'k6/http';
import { group } from "k6";

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

export default function main(){
    let headers = {
        "content-type": "application/json",
        "Authorization": `${TOKEN}`,
    }
    
    Object.assign(headers, JSON.parse(REQUEST_HEADERS))

    const params = {
        headers: headers,
        timeout : REQUEST_TIME_OUT
    }

    group(`Request Endpoint:`,
    function () {
        const response = http.get(`${HOST}${REQUEST_URL}`, params)
        commonFunctions.verifyResponseStatus(response, REQUEST_URL, 'GETAPI', REQUEST_TIME_OUT)
    }
    );
    
}

export function handleSummary(data) {
  let logPath = `./data/resultLogs`

  let summaryDetailsDct = commonFunctions.constructSummaryObj(CONFIG_ID, data, envData, logPath, REQUEST_TIME_OUT)
  return summaryDetailsDct
}
