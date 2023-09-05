import http from 'k6/http';

import * as commonFunctions from './commonFunctions.js'

const HOST = __ENV['host']
const REQUEST_URL = __ENV['endpoint']
const REQUEST_PAYLOAD = __ENV['payload']
const REQUEST_TIME_OUT = __ENV['timeout'] || '1m'
const TOKEN = __ENV['token']

export default function main(){
    let headers = {
        "content-type": "application/json",
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