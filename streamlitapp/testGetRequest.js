import http from 'k6/http';

import * as commonFunctions from './commonFunctions.js'

const HOST = __ENV['host']
const REQUEST_URL = __ENV['endpoint']
const REQUEST_TIME_OUT = __ENV['timeout'] || '3m'
const DSN = __ENV['dsn']
const USERNAME = __ENV['username']
const PASSWORD = __ENV['password']

let adminLoginCert;


export default function main(){

    group(`Login to ${HOST}`,
    function () {
        if (!adminLoginCert) {
            adminLoginCert = commonFunctions.login(HOST, DSN, USERNAME, PASSWORD, REQUEST_TIME_OUT)
        }
        vuJar.set(`${HOST}`, 'LoginCert', adminLoginCert)
        sleep(3)
    }
    );

    group(`Request Endpoin ${REQUEST_URL}:`,
    function () {
        const params = {
            timeout : REQUEST_TIME_OUT
        }
    
        const response = http.get(`${HOST}/planview/${REQUEST_URL}`, params)
    
        commonFunctions.verifyResponseStatus(response, REQUEST_URL, 'GETREQUEST', REQUEST_TIME_OUT) 
    }
    );
}


export function handleSummary(data) {
  let logPath = `./resultLogs`

  let summaryDetailsDct = commonFunctions.constructSummaryObj(data, logPath, REQUEST_TIME_OUT)
  return summaryDetailsDct
}