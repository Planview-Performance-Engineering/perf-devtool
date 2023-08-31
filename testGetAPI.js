import http from 'k6/http';

import * as commonFunctions from './commonFunctions.js'

const HOST = __ENV['host']
const REQUEST_URL = __ENV['endoint']
const REQUEST_TIME_OUT = __ENV['timeout'] || '1m'
const clientID = __ENV['clientID']
const clientSecret = __ENV['clientSecret']

export function setup() {
  const accessToken = commonFunctions.getAccessToken(HOST, clientID, clientSecret)
  return accessToken

}

export default function main(accessToken){
    let headers = {
        "content-type": "application/json",
        "Authorization": `bearer ${accessToken}`,
    }
    const params = {
        headers: headers,
        timeout : REQUEST_TIME_OUT
    }

    const response = http.get(`${HOST}/planview/${REQUEST_URL}`, params)
    
    commonFunctions.verifyResponseStatus(response, REQUEST_URL, 'GETAPI', REQUEST_TIME_OUT)
    
}

export function handleSummary(data) {
  let logPath = `./resultLogs`

  let summaryDetailsDct = commonFunctions.constructSummaryObj(data, logPath, REQUEST_TIME_OUT)
  return summaryDetailsDct
}