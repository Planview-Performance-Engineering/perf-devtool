import http from 'k6/http';

import * as commonFunctions from './commonFunctions.js'


let testData = open("./data/config.json")
testData = JSON.parse(testData)

const CONFIG_ID = __ENV['configID']

const envData = testData[CONFIG_ID]
const HOST = envData['hostname']
const REQUEST_URL = envData['endpoint']
const REQUEST_TIME_OUT = __ENV['timeout'] || '3m'
const TOKEN = envData['token']
const REQUEST_PAYLOAD = envData['payload']
const CONTENT_TYPE = envData['payloadType']


export default function main(){
    let headers = {
        "content-type": CONTENT_TYPE,
        "Authorization": `bearer ${TOKEN}`,
    }
    const params = {
        headers: headers,
        timeout : REQUEST_TIME_OUT
    }

    const response = http.post(`${HOST}/planview/${REQUEST_URL}`, REQUEST_PAYLOAD, params)
    
    commonFunctions.verifyResponseStatus(response, REQUEST_URL, 'POSTAPI', REQUEST_TIME_OUT)
    
}

export function handleSummary(data) {
  let logPath = `./resultLogs`

  let summaryDetailsDct = commonFunctions.constructSummaryObj(data, logPath, REQUEST_TIME_OUT)
  return summaryDetailsDct
}