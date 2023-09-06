import http from 'k6/http';
import { fail } from "k6";
import { Rate, Trend } from "k6/metrics";
import { textSummary } from 'https://jslib.k6.io/k6-summary/0.0.1/index.js';


let passRate = new Rate(`APIPassRate`)
let loginResponseTime = new Rate(`APIRequestTimeoutRate`)
let responseTime = new Trend(`APIResponseTime`, true)

let loginPassRate = new Rate(`LoginPassRate`)
let requestTimeoutRate = new Rate(`LoginRequestTimeoutRate`)
let loginRequestTimeoutRate = new Trend(`LoginResponseTime`, true)

export function login(host, dsn, username, password, requestTimeout = '1m') {
    const LOGIN_URL = `${host}/planview/login/body.aspx`

    const payload = {
        DSN: dsn,
        Username: username,
        UserPass: password
    }
    const headers = {
        "content-type": "application/x-www-form-urlencoded",
        "referer": `${host}/planview/login/body.aspx`
    }

    const params = {
        headers: headers,
        timeout: requestTimeout
    }

    console.log('=============',JSON.stringify(payload))

    const response = http.post(LOGIN_URL, payload, params);

    const ADMIN_LOGIN_CERT = verifyLogin(response, username, requestTimeout)
    return ADMIN_LOGIN_CERT
}

export function getAccessToken(host, clientID, clientSecret){

    const url = `${host}/polaris/public-api/oauth/token`

    const requestBody = {
    client_id: clientID,
    client_secret: clientSecret,
    scope: NaN,
    grant_type : 'client_credentials'
    }

   const response = http.post(url, requestBody)
   const accessToken = verifyGetAccessToken(response)
   return accessToken

}

export function constructSummaryObj(CONFIG_ID, data, testData, logPath, requestTimeOut) {

    let endDateObj = new Date()
    let strEndTime = endDateObj.toISOString()
    let testDuration = data['state']['testRunDurationMs']
    let numVirtualUsers = data['metrics']['vus_max']['values']['max']
    let totalIterations = data['metrics']['iteration_duration']['values']['count']

    let strStartTime = endDateObj - testDuration
    let startDateObj = new Date(strStartTime)
    strStartTime = startDateObj.toISOString()

    let testDurationMin = Math.round(testDuration / 60000)

    let testSummary = {
        "StartTime": strStartTime,
        "EndTime": strEndTime,
        "TestDurationMin": testDurationMin,
        "VirtualUsers": numVirtualUsers,
        "testData": testData,
        "RequestTimeOut": requestTimeOut,
        "TotalIterations": totalIterations
    }

    data['TestSummary'] = testSummary

    const FILE_PATH = `${CONFIG_ID}_${strStartTime}`.replace(':', "_").replace('.', '_')

    let jsonPath = `${logPath}/${FILE_PATH}.json`

    let resultSummary = { 'stdout': textSummary(data, { indent: ' ', enableColors: true }) }

    resultSummary[jsonPath] = JSON.stringify(data)

    console.log(`****************** TEST SUMMARY REPORT ${FILE_PATH} IS GENERATED ******************`)
    return resultSummary
}

function verifyGetAccessToken(response){
    let accessToken;
    try {
        accessToken = response.json()['access_token']

    } finally {
        if (response.status == 200) {
            return accessToken
        }
        else {
            fail(`Token API failed with, ${response.body}`)
        }
    }
}


function verifyLogin(response, username, requestTimeout) {

    let adminLoginCert
    let vuJar = http.cookieJar()
    let cookiesForLoginURL = vuJar.cookiesForURL(response.url)

    let { vu, iter } = getVUandITER()

    if ('LoginCert' in cookiesForLoginURL) {
        adminLoginCert = cookiesForLoginURL.LoginCert[0]
        console.log(`[VU: ${vu}  Iter: ${iter}] User ${username} login Cert: ${adminLoginCert}`)

        if (adminLoginCert.length < 20) {
            loginPassRate.add(false, { action: "Login"})
            loginRequestTimeoutRate.add(false, { action: "Login", timeout: requestTimeout })
            fail(`[VU: ${vu}  Iter: ${iter}] Invalid login cert ${adminLoginCert} for user ${username}`)
        }
        else {
            loginPassRate.add(true, { action: "Login"})
            loginResponseTime.add(response.timings.duration, { action: "Login"})
            loginRequestTimeoutRate.add(false, { action: "Login", timeout: requestTimeout})
        }
    }
    else if (response.error.includes('request timeout')) {
        loginPassRate.add(false, { action: "Login"})
        loginRequestTimeoutRate.add(true, { action: "Login", timeout: requestTimeout})
        fail(`[VU: ${vu}  Iter: ${iter}] Request timeout exception occured at Login`)
    }
    else {
        loginPassRate.add(false, { action: "Login"})
        loginRequestTimeoutRate.add(false, { action: "Login", timeout: requestTimeout})
        fail(`[VU: ${vu}  Iter: ${iter}] Login Cert is not returned by Login API for user ${username}`)
    }
    return adminLoginCert
}


export function verifyResponseStatus(response, endPoint, apiAction, requestTimeout){
        if (response.status == 200) {
            passRate.add(true, { action: apiAction, endPoint: endPoint })
            requestTimeoutRate.add(false, { action: apiAction, timeout: requestTimeout, endPoint: endPoint })
            responseTime.add(response.timings.duration, { action: apiAction, endPoint: endPoint })
        }
        else if (response.error.includes('request timeout')) {
            passRate.add(false, { action: apiAction, endPoint: endPoint })
            requestTimeoutRate.add(true, { action: apiAction, timeout: requestTimeout, endPoint: endPoint })
            fail(`Request timeout exception occured while getting ${endPoint} attributes,API url is:${apiUrl}`)
        }
        else {
            passRate.add(false, { action: apiAction, endPoint: endPoint })
            requestTimeoutRate.add(false, { action: apiAction, timeout: requestTimeout, endPoint: endPoint })
            fail(`get ${endPoint} attributes API failed with, ${response.body}`)
        }
}

export function getVUandITER() {
    let vu, iter
    if (typeof __ITER === 'undefined') {
        iter = 'setup/teardown'
        vu = 'setup/teardown'
    }
    else {
        iter = __ITER
        vu = __VU
    }
    return { vu, iter }
}