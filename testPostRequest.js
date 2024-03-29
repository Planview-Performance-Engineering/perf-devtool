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
const REQUEST_PAYLOAD = envData['payload']
const CONTENT_TYPE = envData['payloadType']
const DSN = envData['dsn']
const USERNAME = envData['username']
const PASSWORD = envData['password']
const PAYLOAD_AS_STRING = envData['payloadAsString']
const HEADERS = envData['requestHeaders']
const AUTH = envData['auth']

let adminLoginCert;


export default function main(){

    let vuJar = http.cookieJar();
    if (AUTH == "Basic") {
        group(`Login to ${HOST}`,
        function () {
            if (!adminLoginCert) {
                adminLoginCert = commonFunctions.login(HOST, DSN, USERNAME, PASSWORD, REQUEST_TIME_OUT)
            }
            vuJar.set(`${HOST}`, 'LoginCert', adminLoginCert)
            sleep(3)
        }
        );
    }

    group(`Request Endpoint:`,
    function () {
        let headers = {
            "content-type": CONTENT_TYPE,
            timeout : REQUEST_TIME_OUT
        }
        Object.assign(headers, JSON.parse(HEADERS))

        const params = {
            headers: headers,
            timeout : REQUEST_TIME_OUT
        }
        const payload = PAYLOAD_AS_STRING ? JSON.stringify(REQUEST_PAYLOAD) : REQUEST_PAYLOAD
        const response = http.post(`${HOST}${REQUEST_URL}`, payload, params)
        commonFunctions.verifyResponseStatus(response, REQUEST_URL, 'POSTAPI', REQUEST_TIME_OUT)
    }
    );
}

export function handleSummary(data) {
  let logPath = `./data/resultLogs`

  let summaryDetailsDct = commonFunctions.constructSummaryObj(CONFIG_ID, data, envData, logPath, REQUEST_TIME_OUT)
  return summaryDetailsDct
}